#!/usr/bin/python
# RPi GPIO connected button for reboot and shutdown + LED Indicator

import RPi.GPIO as GPIO
from time import sleep
import os

# set BUTTON & LED GPIO numbers
BUTTON=23  # button PIN
LED=24     # LED PIN
numF=5     # number of fast blinks
sF=0.2     # speed of fast blinks
numS=3     # number of slow blinks
sS=0.5     # speed of slow blinks

# set GPIO's
GPIO.setmode(GPIO.BCM)                                 # BCM numbering
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # BUTTON set as input with pullup resistor
GPIO.setup(LED, GPIO.OUT)                              # LED PIN set as output
GPIO.output(LED, GPIO.HIGH)                            # initial state of LED set to be on

# def of fast blinking LED
def Blink_f(LED):
    for i in range(0, numF):
        print("LED blinking fast")
        GPIO.output(LED, GPIO.HIGH)
        sleep(sF)
        GPIO.output(LED, GPIO.LOW)
        sleep(sF)
    else:
        GPIO.output(LED, GPIO.HIGH)

# def of slow blinking LED
def Blink_s(LED):
    for i in range(0, numS):
        print("LED blinking slow")
        GPIO.output(LED, GPIO.HIGH)
        sleep(sS)
        GPIO.output(LED, GPIO.LOW)
        sleep(sS)
    else:
        GPIO.output(LED, GPIO.HIGH)

# def of main system action 
def system_action(BUTTON):
    print("Button pressed = PIN  %s"%BUTTON)         # print while testing 
    button_T = 0                                     # button press timer set to 0

    while True:                                      # while true -- loop

        if (GPIO.input(BUTTON) == False) :           # while button is still pressed down
            button_T += 1                            # counting for how long button is pressed [(( 1=0.1s )) sleep time]

        else:                                        # if button is released

            if (button_T > 40) :                                       # pressed for > 4 seconds
                print "long press > 4s : ", button_T                   # print while testing
                print "system going for shutdown now"
                Blink_f(LED)                                           # fast blink of LED indication for shutdown 
#                os.system("sudo shutdown -h now")                      # shutdown uncomment while in operation

            elif (button_T > 10) :                                     # pressed for more than 1s - less than 4 seconds
                print "short press > 1s < 4s : ", button_T             # print while testing
                print "system going for reboot now"
                Blink_s(LED)                                           # slow blink of LED indication for reboot
#                os.system("sudo shutdown -r now")                      # reboot uncomment while in operation

            button_T = 0                             # reset timer back to 0 
        sleep(0.1)                                   # counter sleep in while loop

# GPIO BUTTON pressed detection which calls for main system action
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=system_action, bouncetime=200)

try:
    while True:
       # main loop 
       # actions to be added while waiting for BUTTON press detection
        sleep (0.1)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on keyboard interuption
GPIO.cleanup()
