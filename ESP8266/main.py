#import the necessary modules
import time
import math
import machine
from machine import Pin, I2C
import network
import ujson
from umqtt.simple import MQTTClient
import ubinascii


movingAverageSampleSize=16

#networking
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
sta_if= network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('EEERover', 'exhibition')
if sta_if.isconnected():
    print("Connected to Wifi")

#MQTT
counter = 0
client = MQTTClient("test", "192.168.0.10")
time.sleep(5)
client.connect()
# while True:
#     payload = ujson.dumps({'YOLO':'{0} Is the message'.format(counter)})
#     client.publish("home",bytes(payload,'utf-8'))
#     counter +=1
#     time.sleep(5)
# #to observe channel, type the following into Powershell: mosquitto_sub -t "home" -h 192.168.0.10

#create the i2cport
i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
#send initialization command 1: 1 sample per output; 15 Hz
i2cport.writeto(0x1E, bytearray([0x00, 0x10]))
#send initialization command 2: gain 1090LSbit per Gauss = 0.92 mG per LSbit
i2cport.writeto(0x1E, bytearray([0x01, 0xE0]))

dataBuffer = []
Activation_Hold_Off_Counter=0
Program_Counter = 0


def convert_mag_readings_to_int(byteArray):
    data = int.from_bytes(byteArray, 'big', False)
    if(data & 0x8000):
        data = (data - 2**16)
    else:
        pass
    return data

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
    #removes First Occurence
    if len(dataBuffer)>4:
        dataBuffer.pop(0)
    return [tot_X,tot_Y,tot_Z]


while True:
    #send the command for single-measurement mode
    # TODO: Do we need to do this for each reading?
    i2cport.writeto(0x1E, bytearray([0x02, 0x01]))
    #Wait 6ms
    #TODO: Why do we need to do this? Synchronisation?
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
    client.publish("magReadings",bytes(sjson,'utf-8'))

    if Program_Counter %16==0:
        print(sjson)

    if Activation_Hold_Off_Counter>200:
        ####TODO: DO DSP HERE
        if dataX >800 and dataY >800:
            #When in Quadrant x
            client.publish("musicControl",bytes("next",'utf-8'))
            print("Next Activated")
            Activation_Hold_Off_Counter = 0
        elif dataX<-800 and dataY <-800:
            client.publish("musicControl",bytes("previous",'utf-8'))
            print("Previous Activated")
            Activation_Hold_Off_Counter = 0

    Activation_Hold_Off_Counter+=1
    Program_Counter+=1
    #time.sleep(1)
