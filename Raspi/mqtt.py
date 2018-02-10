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
import threading
#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)



def main():
    #Setup the music Events
    eventMap = {}
    for i in ["play","pause","next","previous"]:
        eventMap[i] = threading.Event()
        eventMap[i].clear()
   
    #create the neccessary threads

    th1 = music.MusicPlayer(eventMap)
    th2 = mqttThread.MQTT(eventMap)

    #Start the events
    th1.start()
    th2.start()
    while True:
        pass



if __name__=="__main__":
    main()