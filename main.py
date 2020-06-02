import sys
import time
import wiringpi as pi

import Adafruit_MPR121.MPR121 as MPR121


cap = MPR121.MPR121()
cap2 = MPR121.MPR121()
touch_count = 1
now_touch = 0b000000000000000000000000
before_touch = 0b0

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
    current_touched = cap.touched()
    current_touched2 = cap2.touched() << 12 # 連続したビットにするために12ビットシフトする
    current_touch_all = current_touched | current_touched2 # 何かしらのビットが立っていれば触っている判定になる


    if current_touch_all:

        for i in range(24):

            # 1個めのタッチ判定を求める処理
            pin_bit = 1 << i # スキャン位置

            '''
            今触っているところと判定しようとしているところが同じ
            かつ前回と一緒じゃない場合に方向を調整
            '''
            if current_touch_all & pin_bit and not before_touch & pin_bit:
                now_touch = pin_bit # 今タッチされているところを保存
                before_touch = pin_bit

            print(format(now_touch, '024b'))
            
            if now_touch - before_touch > 0:
                print("<-")
            elif now_touch - before_touch < 0:
                print("->")
            else:
                print("--")



            # 2個めのタッチ判定を求める処理
            
    else:
        # 何も入力がなくなったら使った各変数の初期化
        touch_count = 0
        before_touch = now_touch
        last_touched = current_touched
        last_touched2 = current_touched2
        



    time.sleep(0.1)



LED_PIN=14

pi.wiringPiSetupGpio()
pi.pinMode (LED_PIN, pi.OUTPUT)
pi.digitalWrite( LED_PIN, pi.LOW)
