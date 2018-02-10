import logging
import threading

import paho.mqtt.client as mqtt
#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


class MQTT(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logging.info("Started MQTT thread")

    def music_message(self,mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #     message = msg.payload



    def run(self):
        logging.info("Setting up MQTT subscribe")

        music_client = mqtt.Client("music_Stream")
        music_client.connect("localhost")
        music_client.subscribe("helpp")
        music_client.on_message = self.music_message
        
        music_client.loop_forever()
