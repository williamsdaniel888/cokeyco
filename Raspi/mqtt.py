# import network
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect('<essid>', '<password>')


import paho.mqtt.client as mqtt
import os
import simpleaudio as sa
from pathlib import Path
import logging
import time
import music
import mqttThread
#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

th1 = music.MusicPlayer()
th2 = mqttThread.MQTT()

def main():
    th1.start()
    th2.start()
    while True:
        pass

#def music_message(mosq, obj, msg):
#     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     message = msg.payload


# music_client = mqtt.Client("music_Stream")
# music_client.connect("localhost")
# music_client.subscribe("helpp")
# music_client.on_message = music_message

# music_client.loop_forever()


if __name__=="__main__":
    main()