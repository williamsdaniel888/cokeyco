#import the necessary modules
import time
from machine import Pin, I2C
#create the i2cport
i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
#send initialization command 1: 1 sample per output; 15 Hz
i2cport.writeto(0x1E, bytearray([0x00, 0x10]))
#send initialization command 2: gain 1090LSbit per Gauss = 0.92 mG per LSbit
i2cport.writeto(0x1E, bytearray([0x01, 0x20]))

for i in range(0,10):
    #send the command for single-measurement mode
    i2cport.writeto(0x1E, bytearray([0x02, 0x01]))
    #Wait 6ms
    time.sleep_ms(7)
    #read six bytes of data 
    dataX = i2cport.readfrom(0x1E, 0x02)
    dataY = i2cport.readfrom(0x1E, 0x02)
    dataZ = i2cport.readfrom(0x1E, 0x02)
    #convert the six bytes to an int
    dataXn = int.from_bytes(dataX,'little',True)
    dataYn = int.from_bytes(dataY,'little',True)
    dataZn = int.from_bytes(dataZ,'little',True)
    #print output
    print("X field: " + str(dataXn)) 
    print("Y field: " + str(dataYn))
    print("Z field: " + str(dataZn)) 
