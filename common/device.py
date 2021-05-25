import json
import umqtt.simple as mqtt
from logging import Logger


class Device:
    """Base Device class, implements MQTT client, pub/sub,  and logging.
    Args:
        config (dict): JSON dict of args to customize this class.
    Attributes:
        config (dict): config attribute
        client (MQTTClient object): client for MQTT pub/sub.
        logger (Logger object): standard micropython-lib logging,
            modified to implement optional logging over MQTT.
    """
    def __init__(self, config):
        # Device config
        self.config = config
        if self.config['logging']['level'] <= 10:
            print("Device config:")
            print(self.config)

        # MQTT client
        self.client = mqtt.MQTTClient(
            client_id   = self.config['mqtt']['thing_id'],
            server      = self.config['mqtt']['endpoint'],
            ssl         = True,
            ssl_params  = {
                'key': self.config['mqtt']['key'],
                'cert': self.config['mqtt']['cert']
            }
        )

        # Logging
        self.logger = Logger(name = self.config['mqtt']['thing_id']) #recycling thing_id for logger name, required.
        self.logger.setLevel(self.config['logging']['level'])

    def publish (self, topic, msg):
        """Publish an MQTT message.
        Args:
            topic (str): MQTT topic to which to publish
            msg (dict): Message to publish, JSON dict
        Returns:
            None
        """
        #connect/publish/disconnect safer, but _very_ slow.
        #self.client.connect() 
        self.client.publish(topic, json.dumps(msg))
        #self.client.disconnect()
        self.log(
            level = 20,
            msg = "published to %s: %s" % (topic, msg),
            log_mqtt=False
        )

    def log (self, level, msg, log_mqtt=False):
        """Log messages to console and, optionally, an MQTT log topic.
        Args:
            level (int): Log level for this message, set in config.
            msg (str): Message to log
            log_mqtt (bool): Toggles logging this msg to MQTT logging endpoint,
                defaults to False.
        Log Levels:
            Description     Level   Displays As
            -----------     -----   -----------
            CRITICAL        50      CRIT
            ERROR           40      ERROR
            WARNING         30      WARN
            INFO            20      INFO
            DEBUG           10      DEBUG
        Returns:
            None
        """
        msg = self.logger.log(level, msg)
        if log_mqtt and level >= self.logger.level:
            msgs = msg.split(':')
            self.publish(
                self.config['logging']['topic'],
                {
                    "level": msgs[0],
                    "thing_id": msgs[1],
                    "message": msgs[2]
                }
            )