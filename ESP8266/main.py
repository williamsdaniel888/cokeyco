#import the necessary modules
import time
import math
import machine
from machine import Pin, I2C
import network
import ujson
from umqtt.simple import MQTTClient
import ubinascii
import PIR.PIR as PIR

movingAverageSampleSize=16

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


#create the i2cport
i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
#send initialization command 1: 1 sample per output; 15 Hz
i2cport.writeto(0x1E, bytearray([0x00, 0x10]))
#send initialization command 2: gain 1090LSbit per Gauss = 0.92 mG per LSbit
i2cport.writeto(0x1E, bytearray([0x01, 0xE0]))

#Data Buffer to hold samples from magnetometer
dataBuffer = []

#Prevent repeat play/pause messages being picked up 
Activation_Hold_Off_Counter=0

#Generic Program counter that increments with each loop
Program_Counter = 0


Pir = PIR()

#Converts the 16 bit raw readings to singed intergers
def convert_mag_readings_to_int(byteArray):
    data = int.from_bytes(byteArray, 'big', False)
    if(data & 0x8000):
        data = (data - 2**16)
    else:
        pass
    return data

#function that averages the last x Results
def moving_average_filter(dataX,dataY,dataZ):
    global dataBuffer
    ls = {"dataX": dataX,"dataY":dataY,"dataZ":dataZ}
    dataBuffer.append(ls)
    tot_X = 0
    tot_Y = 0
    tot_Z = 0
    for i in dataBuffer:
        tot_X += i["dataX"]
        tot_Y += i["dataY"]
        tot_Z += i["dataZ"]

    #Removes Earlyist Occurence from buffer when data buffer is full
    if len(dataBuffer)>movingAverageSampleSize:
        dataBuffer.pop(0)
    return [tot_X,tot_Y,tot_Z]




while True:
    #send the command for single-measurement mode
    i2cport.writeto(0x1E, bytearray([0x02, 0x01]))
    #Wait 6ms for readings to occur
    time.sleep_ms(7)


    data = i2cport.readfrom(0x1E, 0x06)


    #convert the six bytes to three ints
    dataX = convert_mag_readings_to_int(bytearray([data[0],data[1]]))   
    dataZ = convert_mag_readings_to_int(bytearray([data[2],data[3]]))
    dataY = convert_mag_readings_to_int(bytearray([data[4],data[5]]))



    

    #Moving Average Filter
    average = moving_average_filter(dataX,dataY,dataZ)
    dataX  = average[0]
    dataY  = average[1]
    dataZ  = average[2]
    #print("Average is", average)


    sjson = "{{'dataX':{0},'dataY':{1},'dataZ':{2}}}".format(dataX,dataY,dataZ)
    # Publishes magnetic readings to mqtt for debugging
    #client.publish("magReadings",bytes(sjson,'utf-8'))


    #Publish on Topic if PIR Is Triggered
    trig = PIR.IsTriggered(Program_Counter)
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
            print("Previous Activated")
            Activation_Hold_Off_Counter = 0

        elif dataX> 800 and dataY< -800:
            client.publish("musicControl",bytes("pause",'utf-8'))
            print("Previous Activated")
            Activation_Hold_Off_Counter = 0
    
    Activation_Hold_Off_Counter+=1
    Program_Counter+=1
    time.sleep(0.1)
