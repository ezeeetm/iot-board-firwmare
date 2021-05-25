import machine
from utils import get_config
from sensor import SensorDevice

# config
config_file = "./config.json"


if __name__ == "__main__":
    try:
        config = get_config(config_file)
        device = SensorDevice(config)
    except Exception as e:
        print("ERROR readig config/initializing Device:")
        print(e)
        machine.reset()

    device.run()