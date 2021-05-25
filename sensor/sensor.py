from time import sleep
from machine import I2C, Pin
from device import Device
from VL53L0X import VL53L0X
from TCS34725 import TCS34725
from TMP007 import TMP007, CFG_1SAMPLE, CFG_4SAMPLE


class SensorDevice(Device):
    def __init__(self, config):
        super(SensorDevice, self).__init__(config)

        # Hardware/sensors
        self._i2c           = I2C(-1, Pin(32), Pin(33))
        self._color_i2c     = I2C(-1, Pin(18), Pin(19))
        self._range_sensor  = VL53L0X(self._i2c)
        self._temp_sensor   = TMP007(self._i2c, samplerate = CFG_4SAMPLE)
        self._color_sensor  = TCS34725(self._color_i2c)

    @property
    def range(self):
        r = self._range_sensor.range
        #return None if r > 8000 else r
        return r

    @property 
    def color(self):
        return self._color_sensor.getRawData()[:3]

    @property
    def temperature(self):
        return self._temp_sensor.temperature
    
    @property
    def ambient_temperature(self):
        return self._temp_sensor.die_temperature


    def run(self):
        self.client.connect()
        self.log (
            level = 50,
            msg = "Device reset event detected",
            log_mqtt=True
        )

        while True:
            try:
                """TCS34725.getRawData() returns 16bit values,
                >> 8 bit RGB (0-255) required.
                """
                data = {
                    'temperature': self.temperature,
                    'distance': self.range,
                    'color': dict(zip('rgb', (i >> 8 for i in self.color)))
                }
                self.publish(
                    topic = self.config['mqtt']['topic'],
                    msg = data
                )
                sleep(self.config['mqtt']['publish_rate'])
                
            except Exception as e:
                try:
                    self.log (
                        level = 50,
                        msg = "Error: %s" % e,
                        log_mqtt=True
                    )
                    self.client.disconnect()
                except:
                    """TODO: log last exception to filesystem here.
                    Publish and delete last exception, when it exists, on next successful reset.
                    This will ensure error msgs are eventuall captured in the log topic,
                    even when errors are caused by network/mqtt issues.
                    """
                    pass
                machine.reset()