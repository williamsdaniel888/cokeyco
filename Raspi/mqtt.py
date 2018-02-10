# import network
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect('<essid>', '<password>')


import paho.mqtt.client as mqtt
import pyglet
import os

from pathlib import Path
home = str(Path.home())
# def music_message(mosq, obj, msg):
#     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     message = msg.payload


# music_client = mqtt.Client("music_Stream")
# music_client.connect("localhost")
# music_client.subscribe("helpp")
# music_client.on_message = music_message

# music_client.loop_forever()


# print(os.chdir(home+"/music"))
musicDir = home+"/music/"
list_of_songs = os.listdir(musicDir)
source1 = pyglet.media.load(musicDir+list_of_songs[1])
player = pyglet.media.Player()
player.queue(source1)
while True:
    player.play()
    print(player.time)