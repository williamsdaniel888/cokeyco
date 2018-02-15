#import the necessary modules
import time
import math
import machine
from machine import Pin, I2C
import network
import ujson
from umqtt.simple import MQTTClient
import ubinascii
import Sensor



WIRELESS_AP_SSID = "pomelo"
WIRELESS_AP_PASSWORD = "joskweraski"


#Wireless etworking
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
sta_if= network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIRELESS_AP_SSID,WIRELESS_AP_PASSWORD)
if sta_if.isconnected():
    print("Connected to Wifi")
else:
    print("Failed to connect to WIFI network")

#MQTT
counter = 0
client = MQTTClient("test", "192.168.0.10")
time.sleep(5)
client.connect()


#Prevent repeat play/pause messages being picked up 
Activation_Hold_Off_Counter=0

#Generic Program counter that increments with each loop
Program_Counter = 0

#Sets up the inital PIR Sensor
Pir = Sensor.PIR()

#Sets up the magentormeter
Magnet = Sensor.Magnetometer()


while True:

    #Moving Average Filter
    average = Magnet.GetAReading()
    dataX  = average[0]
    dataY  = average[1]
    dataZ  = average[2]
    #print("Average is", average)


    sjson = "{{'dataX':{0},'dataY':{1},'dataZ':{2}}}".format(dataX,dataY,dataZ)
    # Publishes magnetic readings to mqtt for debugging
    #client.publish("magReadings",bytes(sjson,'utf-8'))


    #Publish on Topic if PIR Is Triggered
    trig = Pir.IsTriggered(Program_Counter)
    if trig[0]==True and trig[1]>200:
        client.publish("showerMate/PIR",bytes("Triggered",'utf-8'))


    #Ocasionally print the data to serial output
    if Program_Counter %16==0:
        print(sjson)

    if Activation_Hold_Off_Counter>200:
        # Check whether readings are above threshold
        if dataX >800 and dataY >800:
            #When in Quadrant x
            client.publish("musicControl",bytes("next",'utf-8'))
            print("Next Activated")

            #Reset Activation hold off to prevent multiple quick triggers
            Activation_Hold_Off_Counter = 0

        elif dataX<-800 and dataY <-800:
            client.publish("musicControl",bytes("previous",'utf-8'))
            print("Previous Activated")
            Activation_Hold_Off_Counter = 0
            
        elif dataX< -800 and dataY> 800:
            client.publish("musicControl",bytes("play",'utf-8'))
            print("play Activated")
            Activation_Hold_Off_Counter = 0

        elif dataX> 800 and dataY< -800:
            client.publish("musicControl",bytes("pause",'utf-8'))
            print("pause Activated")
            Activation_Hold_Off_Counter = 0
    
    Activation_Hold_Off_Counter+=1
    Program_Counter+=1
    time.sleep(0.1)
