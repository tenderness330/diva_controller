import sys
import time
import wiringpi as pi

import Adafruit_MPR121.MPR121 as MPR121


cap = MPR121.MPR121()

if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

LED_PIN=14

pi.wiringPiSetupGpio()
pi.pinMode (LED_PIN, pi.OUTPUT)
pi.digitalWrite( LED_PIN, pi.LOW)
