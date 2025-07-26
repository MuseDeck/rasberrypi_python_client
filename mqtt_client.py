import os
import ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

broker_url = os.getenv("MQTT_BROKER_URL")
broker_port = int(os.getenv("MQTT_BROKER_PORT"))
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

assert broker_url is not None
assert broker_port is not None
assert mqtt_username is not None
assert mqtt_password is not None


class MQTT_Client:
    def __init__(self, inspiration_action, settings_action):
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.tls_set(
            ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED
        )
        self.inspiration_action = inspiration_action
        self.settings_action = settings_action
        self.settings_topic = "sui-lan/config/update"
        self.inspiration_topic = "sui-lan/inspiration/new"

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("😀successfully connected to broker")
            self.client.subscribe(self.settings_topic)
            self.client.subscribe(self.inspiration_topic)
        else:
            logging.info(f"🤡connection failed with result code {rc}")

    def on_message(self, client, userdata, msg):
        if msg.topic == self.settings_topic:
            logging.info(f"settings updated")
            self.settings_action()
        elif msg.topic == self.inspiration_topic:
            logging.info(f"inspiration received")
            self.inspiration_action()

    def publish_message(self, topic, message):
        self.client.publish(topic, message)
        logging.info(f"🧙pulished message [{topic}]: {message}")

    def run(self):
        logging.info("starting mqtt client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_url, broker_port, 60)
        self.client.loop_forever()


if __name__ == "__main__":
    # simple test
    mqtt_client = MQTT_Client(
        inspiration_action=lambda: logging.info("inspiration"),
        settings_action=lambda: logging.info("settings"),
    )
    mqtt_client.run()
