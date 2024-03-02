import paho.mqtt.client as mqtt
import constants
import subscriber_dependencies
import json
from time import sleep

mqttBroker = 'test.mosquitto.org'

def on_connect(self, client, userData, flags, rc):
    topics = [(constants.MQTT_VID_FEED_TOPIC, 0), (constants.MQTT_COORDINATES_TOPIC, 1)]
    self.subscribe(topics)

def on_message(client, userdata, message):
    dataDict = json.loads(message.payload)
    if message.topic == constants.MQTT_COORDINATES_TOPIC:
        print('coordrec')
        subscriber_dependencies.receivedCoords(dataDict)
    elif message.topic == constants.MQTT_VID_FEED_TOPIC:
        print('vidrec')
        subscriber_dependencies.receivedFeed(dataDict)
    

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='FTC/SERVER', clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttBroker, 1883)

client.loop_forever()
print('Listening for connection...')
