# rpi_tlc5916
Rasberry Pi Library for the TLC5916 LED Driver Chip

Library for driving LEDS on the Texas Instruments TLC5916 8 Channel Constant Current LED Sink Driver

Instructions:

Wire the chips up as per the manufacturer specs (http://www.ti.com/lit/ds/symlink/tlc5916.pdf)

Use 4 GPIO pins (default are 11,12,13,15), they can be changed via the method set_pins(data, clock, latch, oe)

Run the test script.

**Note: If the test reports errors of locaked ports or does not light up the LEDs, then you need to install the wiringPi library (http://wiringpi.com/download-and-install/)

