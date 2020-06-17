import sys
import time
import wiringpi as pi

import Adafruit_MPR121.MPR121 as MPR121

# 各変数初期化
cap = MPR121.MPR121()
cap2 = MPR121.MPR121()

# 初期化
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

if not cap2.begin(0x5B):

    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

'''
touchpad1 0000 0000 0000 1111 1111 1111
touchpad2 1111 1111 1111 0000 0000 0000
no touch  0000 0000 0000 0000 0000 0000
'''

while True:
    # 現在のタッチ状態を取得
    current_touched = cap.touched() << 1 # 一番端もスライド判定できるように端に論理的隙間を作る
    current_touched2 = cap2.touched() << 13 # 連続したビットにするために13ビットシフトする
    current_touch_all = current_touched | current_touched2 # 何かしらのビットが立っていれば触っている判定になる

    # 判定の開始
    if current_touch_all:
        print("\r",format(current_touch_all,"024b"))

    time.sleep(1)



LED_PIN=14

pi.wiringPiSetupGpio()
pi.pinMode (LED_PIN, pi.OUTPUT)
pi.digitalWrite( LED_PIN, pi.LOW)
