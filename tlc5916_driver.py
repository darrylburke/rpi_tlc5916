"""
title: tcl5916 Driver
author: Darryl Burke - 2015
Desc:  Driver for TLC5916in Chip Support up to 4 chips in series
"""
import time
import RPi.GPIO as GPIO

#defaults
NumOfChips=4
MaxChips=4
LEDOutputs=8
DataOutPin=11
ClockPin=12
LatchPin=13
OEPin=15
Offset=0

debug=False
info=False
pwmFreq=200
pwmLoad=100
pwm=0
TMPLEDS=[]

# Init Pins
#Initialize all the pins
def init():
    global pwm
    global GPIO
   
    GPIO.setwarnings(debug)
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
#Set all the LEDs based on an array of which leds to turn on
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

    print ("Array with Set Values")
    printarray(TMPLEDS,info)
    send_arrays()
    toggleLatch()
#create an empty array for populating with LEDs to turn on
def create_empty_array():
    global TMPLEDS
    if debug:
       print ("Creating %d Arrays of %d" % (MaxChips,LEDOutputs))
    TMPLEDS=[[0 for x in range(LEDOutputs)] for x in range(MaxChips)]
    #if debug:
    #   printarray(TMPLEDS)
    for x in range(MaxChips):
        for y in range(LEDOutputs):
            TMPLEDS[x][y]=0
    if debug:
        printarray(TMPLEDS)
    if debug:
      print ("Done Creating Empty Array")

# print the array for diagnostics
def printarray(myarray,force=False):
    show=debug
    if force:
      show=True
    if show:
        print ("Printing Array")
    #for i in range(MaxChips):
    #    print("sending %d = %s" % (i, ','.join(str(x) for x in array[i])))
    if show:
        print ("Array:")
    for x in range(MaxChips):
        output='  '
        output+=str(x)
        output+=':'
        for y in range(LEDOutputs):
            val = myarray[x][y]
            output += str(val)
            output += ":"
        if show:
            print (output)

#set the pins for Data, Clock, Latch and OE        
def set_pins(p1,p2,p3,p4):
    global DataOutPin
    global ClockPin
    global LatchPin
    global OEPin
    DataOutPin=p1
    ClockPin=p2
    LatchPin=p3
    OEPin=p4
#toggle the latch to move the data from the temporary store to the leds
def toggleLatch():
    global GPIO
    GPIO.output(LatchPin,True)
    GPIO.output(LatchPin,False)
# turn off all leds
def turn_off():
     set_pwm(0)
#turn on all leds 100% by default unless specified
def turn_on(load=100):
    set_pwm(load)
# light the LEDS according to whats in TMPLED array
def send_arrays(forceall=False):
   global GPIO
   forceboards = NumOfChips
   if forceall:
     forceboards = MaxChips
   for j in range (forceboards):
      rawboard=(forceboards-1)
      rawboard-=j
      board=(forceboards-1)
      board-=j
      if Offset==0:
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
#clear all LEDs
def all_leds_on():
    global TMPLEDS
    global ledarray
    print "ALL LEDS ON"
    create_empty_array()
    for x in range (MaxChips):
       for y in range (LEDOutputs):
             TMPLEDS[x][y]=1
    printarray(TMPLEDS,info)
    send_arrays(True)
    toggleLatch()
 
def clear_leds():
    global TMPLEDS
    create_empty_array()
    send_arrays(True)
    toggleLatch()
def clear_all_leds():
   for j in range (MaxChips):
       setleds([])

#set the number of chips in series you are using
def set_chips(chips):
    global NumOfChips
    NumOfChips = chips
#set the debug flag on/off
def set_info( dbg):
    global info
    print ("Setting Info to %s" % str(dbg))
    info=dbg
def set_debug( dbg):
    global debug
    print ("Setting Debug to %s" % str(dbg))
    debug=dbg
# set the pwm brightness
def set_pwm(newpwm):
    global pwm
    pwm.ChangeDutyCycle(pwmLoad-newpwm)
# set the board offset if you are using 1 chip but want to display what should be on 1-4. for diagnostics only
def set_offset(value):
    global Offset
    Offset=value;
# test function
def test():
    turn_off()
    print("Running test sequence")
    print("clearing LEDs")
    print("Chips:%d" %NumOfChips)
    clear_leds()
    clear_leds()
    clear_leds()
    clear_leds()
    time.sleep (5);
    if debug:
      print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-")
    for y in range (10):
      turn_on()
      all_leds_on()
      time.sleep(5)
      clear_leds()
     
      for i in range(1,NumOfChips*LEDOutputs+1):
         print("LED:%s" % i)
        # setleds([i,i+8,i+16,i+24])
         setleds([i])
         time.sleep(1)
      #for i in range(1,NumOfChips*LEDOutputs+1):
      #   print("LED:%s" % i)
      #   setleds([i])
      #   time.sleep(1)
      turn_off()
      clear_leds()
      time.sleep(5)
    GPIO.cleanup()
