import sys
import time
import wiringpi as pi

import Adafruit_MPR121.MPR121 as MPR121

# 各変数初期化
cap = MPR121.MPR121()
cap2 = MPR121.MPR121()
touch_count = 1
now_touch = 0b000000000000000000000000
before_touch = 0b0
touch_ave = 0
touch_ave_size = 0
touch_ave2 = 0
touch_ave_size2 = 0
pin_bit = 0b1

IPpoint1 = 0
IPpoint2 = 0
IPpoint1_vector = 0
IPpoint2_vector = 0

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
    current_touched = cap.touched() << 1 # 一番端もスライド判定できるように端に論理的隙間を作る
    current_touched2 = cap2.touched() << 13 # 連続したビットにするために13ビットシフトする
    current_touch_all = current_touched | current_touched2 # 何かしらのビットが立っていれば触っている判定になる


    if current_touch_all:
        i = 1
        while i < 25:
            if current_touch_all & pin_bit:
                if touch_ave > 0:
                    while current_touch_all & pin_bit:
                        # 2つめの判定
                        touch_ave2 = touch_ave2 + i
                        touch_ave_size2 = touch_ave_size2 + 1
                        pin_bit = pin_bit << 1
                        i = i + 1
                        print("while", i)

                else:

                    while current_touch_all & pin_bit:
                        # 1つめの判定
                        touch_ave = touch_ave + i
                        touch_ave_size = touch_ave_size + 1
                        pin_bit = pin_bit << 1
                        i = i + 1
                        print("while", i)

                pin_bit = pin_bit >> 1
                i = i - 1

            pin_bit = pin_bit << 1
            if touch_ave2 > 0:
                i = 24

            i = i + 1

        if touch_ave_size != 0:
            touch_ave = touch_ave / touch_ave_size
        else:
            touch_ave = 0

        if touch_ave_size2 != 0:
            touch_ave2 = touch_ave2 / touch_ave_size2
        else:
            touch_ave2 = 0

        # 前回判定チェック
        if last_touch_ave > 0:
            if touch_ave2 > 0 and touch_ave2 == 0:
                if abs(last_touch_ave - touch_ave) > 5:
                    last_touch_ave = last_touch_ave2
                    last_touch_ave2 = 0

            elif last_touch_ave2 == 0 and touch_ave2 > 0:
                if abs(last_touch_ave - touch_ave) > 5:
                    touch_ave = touch_ave2
                    touch_ave2 = 0

            if last_touch_ave > 0 and touch_ave:
                IPpoint1 = last_touch_ave - touch_ave

            if last_touch_ave2 > 0 and touch_ave2:
                IPpoint2 - last_touch_ave2 - touch_ave2


            if IPpoint1 > 0:
                IPpoint1_vector = 1

            elif IPpoint1 < 0:
                IPpoint1_vector = -1

            if IPpoint2 > 0:
                IPpoint2_vector = 1

            elif IPpoint2 < 0:
                IPpoint2_vector = -1

            now_input = last_input

        print("IPPoint1:", IPpoint1, "IPpoint2:", IPpoint2)
        print("IPPointvector", IPpoint1_vector)
        print("IPPointvecto2r", IPpoint2_vector)
        last_touch_ave = touch_ave
        last_touch_ave2 = touch_ave2

    else:

        last_touch_ave = touch_ave
        last_touch_ave2 = touch_ave2
        IPpoint1 = 0
        IPpoint2 = 0
        IPpoint1_vector = 0
        IPpoint2_vector = 0
        touch_ave_size = 0
        touch_ave_size2 = 0


    time.sleep(1)



LED_PIN=14

pi.wiringPiSetupGpio()
pi.pinMode (LED_PIN, pi.OUTPUT)
pi.digitalWrite( LED_PIN, pi.LOW)
