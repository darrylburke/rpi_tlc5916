"""
title: tcl5916 Driver
author: Darryl Burke - 2015
Desc:  Driver for TLC5916in Chip Support up to 4 chips in series

"""
import time
import RPi.GPIO as GPIO

#default pins
NumOfChips=4
MaxChips=4
LEDOutputs=8
DataOutPin=11
ClockPin=12
LatchPin=13
OEPin=15
Offset=0

debug=False
pwmFreq=200
pwmLoad=100
pwm=0
TMPLEDS=[]

# Init Pins

def init():
    global pwm
    global GPIO
    GPIO.setwarnings(True)
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
       if debug:
          print ("LED: %d" % (led))
       for x in range (MaxChips):
          for y in range (LEDOutputs):
             position = x * LEDOutputs + y
             if (led-1) == position:
                 if debug:
                    print ("Setting %d : %d -> %d" % (x,y,1))
                 TMPLEDS[x][y]=1

    printarray(TMPLEDS)
    send_arrays()
    toggleLatch()

def create_empty_array():
    global TMPLEDS
    if debug:
       print ("Creating %d Arrays of %d" % (MaxChips,LEDOutputs))
    TMPLEDS=[[0 for x in range(LEDOutputs)] for x in range(MaxChips)]
    if debug:
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
    global GPIO
    GPIO.output(LatchPin,True)
    GPIO.output(LatchPin,False)

def turn_off():
     set_pwm(0)
     #GPIO.output(OEPin, True)

def turn_on(load=100):
    set_pwm(load)
    #GPIO.output(OEPin, False)

def send_arrays():
   global GPIO
   for j in range (NumOfChips):
      rawboard=(NumOfChips-1)
      rawboard-=j
      board=(NumOfChips-1)
      board-=j
      board+=Offset
      if debug:
         print ("Offset: %d Old: %d New: %d" % (Offset, rawboard, board))
      for i in range(LEDOutputs):
          #data
          GPIO.output(ClockPin,False)
          if TMPLEDS[board][7-i]==1:
              if debug:
                 print ("ON: %d : %d" % (j,i))
              GPIO.output(DataOutPin,True)
          else:
              if debug:
                 print ("OFF: %d : %d" % (j,i))
              GPIO.output(DataOutPin,False)
          GPIO.output(ClockPin,True)

def clear_leds():
   for j in range (NumOfChips):
       setleds([])

def clear_all_leds():
   for j in range (MaxChips):
       setleds([])


def set_chips(chips):
    global NumOfChips
    NumOfChips = chips

def set_debug( dbg):
    global debug
    print ("Setting Debug to %s" % str(dbg))
    debug=dbg

def set_pwm(newpwm):
    global pwm
    pwm.ChangeDutyCycle(pwmLoad-newpwm)

def cleanup():
    global GPIO
    set_pwm(0)
    GPIO.cleanup()

def set_offset(value):
    global Offset
    Offset=value;

def test():
    print("running test sequence")
    turn_on(1)
    setleds([1,2,11,12,21,22,31,32])
    #setleds([1,2])
    #setleds([1])
    time.sleep(5)
    setleds([])
