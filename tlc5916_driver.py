
"""
title: tcl5916 Driver
author: Darryl Burke - 2015
Desc:  Driver for TLC5916in Chip Support up to 4 chips in series

"""
import time
import RPi.GPIO as GPIO

#default pins
NumOfChips=1
MaxChips=4
LEDOutputs=8
ClearOnSet=True
DataOutPin=11
ClockPin=12
LatchPin=13
OEPin=15

debug=False
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

def init():
    global pwm
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
    pwm = GPIO.PWM(OEPin, pwmFreq)
    pwm.start(pwmLoad)

def setleds(ledarray):
    global TMPLEDS
    create_empty_array()

    for led in ledarray:
       print ("LED: %d" % (led))
       for x in range (NumOfChips):
          for y in range (LEDOutputs):
             position = x * LEDOutputs + y
             if (led-1) == position:
                 print ("Setting %d : %d -> %d" % (x,y,1))
                 TMPLEDS[x][y]=1

    printarray(TMPLEDS)
    send_arrays()
    #send_digit(number,False)
    toggleLatch()

def create_empty_array():
    global TMPLEDS
    print ("Creating %d Arrays of %d" % (MaxChips,LEDOutputs))
    TMPLEDS=[[0 for x in range(LEDOutputs)] for x in range(MaxChips)]
    printarray(TMPLEDS)
    for x in range(MaxChips):
        #_arr=[]
        for y in range(LEDOutputs):
            TMPLEDS[x][y]=0
            #_arr.append(0)
        #TMPLEDS.append(_arr)
    if debug:
        printarray(TMPLEDS)

def printarray(myarray):
    print ("Created Blank Array")
    #for i in range(MaxChips):
    #    print("sending %d = %s" % (i, ','.join(str(x) for x in array[i])))
    print ("Array:")
    for x in range(MaxChips):
        output='  '
        output+=str(x)
        output+=':'
        for y in range(LEDOutputs):
            val = myarray[x][y]
            output += str(val)
            output += ":"
        print (output)

def toggleLatch():
    GPIO.output(LatchPin,True)
    GPIO.output(LatchPin,False)

def turn_off():
     set_pwm(0)
     #GPIO.output(OEPin, True)

def turn_on():
    set_pwm(100)
    #GPIO.output(OEPin, False)

def send_arrays():
   for j in range (MaxChips):
      for i in range(LEDOutputs):
          GPIO.output(ClockPin,False)
          #data
          if TMPLEDS[j][7-i]==1:
              print ("ON: %d : %d" % (j,i))
              GPIO.output(DataOutPin,True)
          else:
              GPIO.output(DataOutPin,False)
          GPIO.output(ClockPin,True)
def send_digit(number):
    #set the point bit
    if debug:
        print("sending %d = %s" % (number, ','.join(str(x) for x in letters[number])))
    #8 clock pulses

    for i in range(8):
        GPIO.output(clk,False)
        #data
        if letters[number][7-i]:
            GPIO.output(sdo,True)
        else:
            GPIO.output(sdo,False)
        GPIO.output(clk,True)


def reset_digits():
    for x in range(NumofChips):
         GPIO.send_digit(0)

def set_chips(chips):
    NumofChips = chips

def set_debug( dbg):
    print ("Setting Debug to %s" % str(dbg))
    debug=dbg

def set_pwm(newpwm):
    pwm.ChangeDutyCycle(100-newpwm)

def cleanup():
    set_pwm(0)
    GPIO.cleanup()


def test():
    set_pwm(20)
    print("running test sequence")
    # for x in range(5):
    #     for i in range(8):
    #         string = "%2d" % (i)
    #         print("sending %s" % string)
    #         setleds(i)
    #         time.sleep(0.1)
    turn_on()
    setleds([1,2,3])
    time.sleep(5)
    setleds([])
