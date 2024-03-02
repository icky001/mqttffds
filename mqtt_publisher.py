import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
from mss import mss
from json import dumps
from time import sleep
import constants

mqttBroker = 'test.mosquitto.org'
deviceId = 1
deviceRef = 'xxxxxx'



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='FTC/Drone', clean_session=False)
client.connect(mqttBroker, 1883)

# We shall use our own screen to fake drone capture data using MSS
bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()


# We shall also fake device coordinates
longitude = 8.1
latitude = 9.11
azimuth = 1.0

iter = 60
while True:
	# Video feed transfer every second
	_, buffer = cv2.imencode('.jpg', np.array(sct.grab(bounding_box)))
	dataDict = {
		'deviceId': deviceId,
		'deviceRef': deviceRef,
		'feedFrame': base64.b64encode(buffer).decode('utf-8')
    }
	client.publish(constants.MQTT_VID_FEED_TOPIC, dumps(dataDict))
	
    # Coordinates transfer every minute
	if iter == 60:
		dataDict = {
			'deviceId': deviceId,
			'deviceRef': deviceRef,
			'longitude': longitude,
			'latitude': latitude,
			'azimuth': azimuth
        }
		client.publish(constants.MQTT_COORDINATES_TOPIC, str(dumps(dataDict)))
		iter = 0
	else:
		iter += 1
	sleep(5)