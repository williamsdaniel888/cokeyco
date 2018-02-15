import machine


class PIR(object):
    def __init__(self):
        PIRPin = machine.Pin(0,machine.Pin.IN)
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