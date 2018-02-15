import machine
from machine import Pin,I2C
import time

movingAverageSampleSize=16



class PIR(object):
    def __init__(self):
        PIRPin = machine.Pin(7,machine.Pin.IN)
        PIRPin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.Callback)
        self.Triggered = False
        self.Program_Counter_When_Last_Triggered = 0

    #Minismise ISR code
    def Callback(self):
        self.Triggered = True


    def IsTriggered(self, program_Counter):
        if self.IsTriggered:
            #The program counter time since the last trigger
            timeSince = program_Counter - self.Program_Counter_When_Last_Triggered
            self.Program_Counter_When_Last_Triggered = program_Counter
            self.Triggered = False
            return (True,timeSince)
        else:
            return (False,0)



class Magnetometer(object):
    def __init__(self):
        #create the i2cport
        self.i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
        #send initialization command 1: 1 sample per output; 15 Hz
        self.i2cport.writeto(0x1E, bytearray([0x00, 0x10]))
        #send initialization command 2: gain 1090LSbit per Gauss = 0.92 mG per LSbit
        self.i2cport.writeto(0x1E, bytearray([0x01, 0xE0]))

        #Data Buffer to hold samples from magnetometer
        self.dataBuffer = []

        #Converts the 16 bit raw readings to singed intergers
    def convert_mag_readings_to_int(self,byteArray):
        data = int.from_bytes(byteArray, 'big', False)
        if(data & 0x8000):
            data = (data - 2**16)
        else:
            pass
        return data

    #function that averages the last x Results
    def moving_average_filter(self,dataX,dataY,dataZ):
        ls = {"dataX": dataX,"dataY":dataY,"dataZ":dataZ}
        self.dataBuffer.append(ls)
        tot_X = 0
        tot_Y = 0
        tot_Z = 0
        for i in self.dataBuffer:
            tot_X += i["dataX"]
            tot_Y += i["dataY"]
            tot_Z += i["dataZ"]

        #Removes Earlyist Occurence from buffer when data buffer is full
        if len(self.dataBuffer)>movingAverageSampleSize:
            self.dataBuffer.pop(0)
        return [tot_X,tot_Y,tot_Z]



    def GetAReading(self):
        #send the command for single-measurement mode
        self.i2cport.writeto(0x1E, bytearray([0x02, 0x01]))
        #Wait 6ms for readings to occur
        time.sleep_ms(7)

        #Read data from the I2C port
        data = self.i2cport.readfrom(0x1E, 0x06)


        #convert the six bytes to three ints
        dataX = self.convert_mag_readings_to_int(bytearray([data[0],data[1]]))   
        dataZ = self.convert_mag_readings_to_int(bytearray([data[2],data[3]]))
        dataY = self.convert_mag_readings_to_int(bytearray([data[4],data[5]]))


        average = self.moving_average_filter(dataX,dataY,dataZ)
        return average