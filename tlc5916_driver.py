
"""
title: tcl5916 Driver
author: Darryl Burke - 2015
Desc:  Driver for TLC5916in Chip Support up to 4 chips in series

"""
import time
import RPi.GPIO as GPIO

#default pins
NumofChips=1
MaxChips=4
LEDOutputs=8
ClearOnSet=True
DataOutPin=11
ClockPin=12
LAtchPin=13
OEPin=15

debug=True
pwmFreq=200
pwmLoad=100
#define which segments are on/off for each digit
#last element is for the point
# LEDs = [
#  [ 0,0,0,0,0,0,0,0 ], # 0
#  [ 1,0,0,0,0,0,0,0 ], # 1
#  [ 0,1,0,0,0,0,0,0 ], # 2
#  [ 0,0,1,0,0,0,0,0 ], # 3
#  [ 0,0,0,1,0,0,0,0 ], # 4
#  [ 0,0,0,0,1,0,0,0 ], # 5
#  [ 0,0,0,0,0,1,0,0 ], # 6
#  [ 0,0,0,0,0,0,1,0 ], # 7
#  [ 0,0,0,0,0,0,0,1 ] # 8
# ]
LEDS=[]
TMPLEDS=[]

# Init Pins


class tlc5916:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(OEPin, GPIO.OUT)
        GPIO.setup(LatchPin, GPIO.OUT)
        GPIO.setup(ClockPin, GPIO.OUT)
        GPIO.setup(DataOutPin, GPIO.OUT)
       #Reset Clock, Latch and Turn Off LEDS
        GPIO.output(OEPin, True)
        GPIO.output(LatchPin,False)
        GPIO.output(ClockPin,False)
        self.pwm = GPIO.PWM(OEPin, pwmFreq)
        self.pwm.start(pwmLoad)


    def setleds(self,ledarray):
        self.send_digit(number,False)
        self.toggleLatch()

    def create_empty_array(self):
        TMPLEDS=[]
        for x in range(MaxChips)
             _arr=[]
            for y in range(LEDOutputs)
                _arr = _arr.append(0)
            TMPLEDS = TMPLEDS.append(_arr)
        if debug:
            print ("Created Blank Array",
            for x in range(MaxChips)
                print("sending %d = %s" % (number, ','.join(str(x) for x in TMPLEDS[x])))


    def toggleLatch(self):
        GPIO.output(LatchPin,True)
        GPIO.output(LatchPin,False)

    def turn_off(self):
         GPIO.output(OEPin, True)

    def turn_on(self):
        GPIO.output(OEPin, False)

    #send a char, with optional point
    def send_digit(self,number):
        #set the point bit
        if self.debug:
            print("sending %d = %s" % (number, ','.join(str(x) for x in letters[number])))
        #8 clock pulses

        if raspi:
            for i in range(8):
                GPIO.output(clk,False)
                #data
                if letters[number][7-i]:
                    GPIO.output(sdo,True)
                else:
                    GPIO.output(sdo,False)
                GPIO.output(clk,True)


    def reset_digits(self):
        for x in range(NumofChips)
             GPIO.send_digit(0)

    def set_chips(self,chips):
        self.NumofChips = chips

    def set_debug(self, dbg):
          self.dbg=bool

    def set_pwm(self,pwm):
        self.pwm.ChangeDutyCycle(100-pwm)

    def cleanup(self):
        self.set_pwm(0)
        GPIO.cleanup()


    def test(self):
        self.set_pwm(20)
        print("running test sequence")
        # for x in range(5):
        #     for i in range(8):
        #         string = "%2d" % (i)
        #         print("sending %s" % string)
        #         self.setleds(i)
        #         time.sleep(0.1)
        self.update(1)
        time.sleep(1)
        self.update(0)

