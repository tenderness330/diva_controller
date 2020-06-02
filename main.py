import sys
import time
import wiringpi as pi

import Adafruit_MPR121.MPR121 as MPR121


cap = MPR121.MPR121()
cap2 = MPR121.MPR121()

# 初期化
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

if not cap2.begin(0x5B):
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

last_touched = cap.touched()   # 0000 0000 0000 1111 1111 1111
last_touched2 = cap2.touched() # 1111 1111 1111 0000 0000 0000

while True:
    current_touched = cap.touched()
    current_touched2 = cap2.touched() << 12 # 連続したビットにするために12ビットシフトする
    touched_all = current_touched | current_touched2 # 何かしらのビットが立っていれば触っている判定になる

    if touched_all: # なにかタッチがされていたら判定を始める

    for i in range(24):
        pin_bit = 1 << i # スキャン位置

        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))

        if current_touched2 & pin_bit and not last_touched2 & pin_bit:
            print('{0} touched!'.format(i))

        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))

        if not current_touched2 & pin_bit and last_touched2 & pin_bit:
            print('{0} released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    last_touched2 = current_touched2
    time.sleep(0.1)



LED_PIN=14

pi.wiringPiSetupGpio()
pi.pinMode (LED_PIN, pi.OUTPUT)
pi.digitalWrite( LED_PIN, pi.LOW)
