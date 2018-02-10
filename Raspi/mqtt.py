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

#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def getHomeDir():
    homeDir = str(Path.home())
    logger.info("Home Directory found to be : %s",homeDir)
    return homeDir

def getMusicPathList(musicDir):
    list_of_songs = os.listdir(musicDir)
    ouptut = []
    for i in list_of_songs:
        if i.endswith(".wav"):
            p = Path(musicDir+i)
            ouptut.append(p)
    return ouptut

def main():
    musicDir = getHomeDir()+ "/music/"
    print("Esists" + str(os.path.exists ("Hello wolrd.txt")))
    if not os.path.exists(musicDir):
        logger.error("Music Dir Path does not exist: %s", musicDir)
    music_list = getMusicPathList(musicDir)
    print(music_list)

    wave_obj = sa.WaveObject.from_wave_file(str(music_list[0]))
    play_obj = wave_obj.play()
    counter =0
    while play_obj.is_playing():
        time.sleep(0.05)
        counter+=1
        if counter>200:
            play_obj.stop()
# def music_message(mosq, obj, msg):
#     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     message = msg.payload


# music_client = mqtt.Client("music_Stream")
# music_client.connect("localhost")
# music_client.subscribe("helpp")
# music_client.on_message = music_message

# music_client.loop_forever()


if __name__=="__main__":
    main()