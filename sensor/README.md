# Sensor

## Required on filesystem:
```
.
├── your.cert.crt
├── your.private.key
├── TCS34725.py
├── TMP007.py
├── VL53L0X.py
├── boot.py
├── config.json
├── device.py
├── logging.py
├── main.py
└── sensor.py
```

**boot.py**

Handles ESP32/uPy system level functionality: WiFi, Access Point, and webREPL, all enabled/disabled and configured in config.

**main.py**

Instantiates a Sensor device from config values, and runs the device.

**device.py**

Superclass to implement common/shared components:

 - MQTT client
 - MQTT pub/sub methods
 - logging, with optional logging to MQTT

**sensor.py**

Subclass implements functionality specific to the Sensor device, and the device's main run() loop.

**logging.py**

Standard logging library from [micropython-lib](https://github.com/micropython/micropython-lib/tree/master/logging), modified to support optional MQTT logging.

**.cert/.key**

TLS certificates for MQTT.  Leave .crt and .key file extensions unchanged for autodetection.

**TCS34725.py**

Color sensor lib

**TMP007.py**

Temp sensor lib

**VL53L0X.py**

Distance sensor lib

**utils.py**

Collection of utility/helper functions that are re-used in several places.

**config.json**

Shared config to modify all configurarable device behavior.  Some notes:

 - Multiple network configs are supported.
 - Device will intelligently skip any networks not in range.
 - AP password must be at least 8 characters.
 - A blank "" webREPL password _is_ supported.
 - `mqtt.thing_id` here must match a `thing_id` provisioned in AWS/GGC.
 - .cert/.key (in filesystem list above) must be correctly associated with the AWS `thing_id` defined here.
 - Log levels are detailed in `./device/py`

```json
{
	"network": {
		"enable_wifi": true,
		"wlans": [{
				"friendly_name": "",
				"essid": "",
				"passwd": ""
			}
		],
		"timeout_seconds": 10,
		"enable_ap": false,
		"ap_essid": "iotanium-kiosk-sensor",
		"ap_pw": "iotanium",
		"enable_webrepl": true,
		"webrepl_pw": ""
	},
	"mqtt": {
		"thing_id": "IoTaniumKiosk_Input",
		"endpoint": "ec2-34-214-106-36.us-west-2.compute.amazonaws.com",
		"topic": "iotanium/kiosk/message",
		"publish_rate": 1
	},
	"logging": {
		"level": 10,
		"topic": "iotanium/kiosk/IoTaniumKiosk_Input/logs"
	}
}
```


