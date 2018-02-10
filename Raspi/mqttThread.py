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
    def __init__(self,eventMap):
        threading.Thread.__init__(self)
        logging.info("Started MQTT thread")
        self.eventMap = eventMap
        self.killThread = threading.Event()

    def decodeEvent(self,msg):
        if msg in self.eventMap.keys():
            logger.info("Event %s recieved and emmitted",msg)
            self.eventMap[msg].set()
        else:
            logger.error("Did not recognise event: %s  :when decoding",msg)


    def music_message(self,mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #     message = msg.payload
        
        if msg == "play" or msg=="pause" or msg == "next" or msg == "previous":
            self.decodeEvent(msg)
        else:
            logger.warn("MQTT message not recognised, msg: %s",msg)



    def run(self):
        logging.info("Setting up MQTT subscribe")

        music_client = mqtt.Client("music_Stream")
        music_client.connect("localhost")
        music_client.subscribe("helpp")
        music_client.on_message = self.music_message
        
        while not self.killThread.is_set():
            pass
        logger.info("Kill thread Recieved, thread %s is shutting down", __name__)