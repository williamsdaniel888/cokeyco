#import the necessary modules
import time
import math
from machine import Pin, I2C

#constants
deg2rad = math.pi / 180.00
declination_angle_deg = -0.433
declination_angle_rad = declination_angle_deg * deg2rad
#create the i2cport
i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
#send initialization command 1: 1 sample per output; 15 Hz
i2cport.writeto(0x1E, bytearray([0x00, 0x10]))
#send initialization command 2: gain 1090LSbit per Gauss = 0.92 mG per LSbit
i2cport.writeto(0x1E, bytearray([0x01, 0x20]))

while True:
    #send the command for single-measurement mode
    i2cport.writeto(0x1E, bytearray([0x02, 0x01]))
    #Wait 6ms
    time.sleep_ms(7)
    data = i2cport.readfrom(0x1E, 0x06)
    #convert the six bytes to three ints
    dataX = int.from_bytes(bytearray([data[0],data[1]]), 'big', True)
    dataZ = int.from_bytes(bytearray([data[2],data[3]]), 'big', True)
    dataY = int.from_bytes(bytearray([data[4],data[5]]), 'big', True)
    #cast to floats and scale by gain factor
    magnetic_X = float(dataX)*0.92E-3
    magnetic_Y = float(dataY)*0.92E-3
    magnetic_Z = float(dataZ)*0.92E-3
    #calculate raw bearing, assuming sensor in X,Y plane
    bearing = math.atan2(magnetic_X,magnetic_Y)
    #compensate with declination angle; mod 2PI; convert to radians; cast to integer
    bearing += declination_angle_rad
    bearing = bearing % (2*math.pi)
    bearing = bearing * 180 / math.pi
    bearing = math.floor(bearing)
    #print output
    print("X field: " + str(magnetic_X) + "mG")
    print("Y field: " + str(magnetic_Y) + "mG")
    print("Z field: " + str(magnetic_Z) + "mG")
    print("Bearing from True North: " + str(bearing) + "°")
    time.sleep(1)
