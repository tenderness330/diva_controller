import sys
import Adafruit_MPR121.MPR121 as MPR121
import time
import wiringpi as pi

cap = MPR121.MPR121()
cap2 = MPR121.MPR121()
before1 = 0b0
before2 = 0b0

R1_PIN = 4
R2_PIN = 17
L1_PIN = 27
L2_PIN = 22

pi.wiringPiSetupGpio()
pi.pinMode (R1_PIN, pi.OUTPUT)
pi.pinMode (R2_PIN, pi.OUTPUT)
pi.pinMode (L1_PIN, pi.OUTPUT)
pi.pinMode (L2_PIN, pi.OUTPUT)



if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

if not cap2.begin(0x5B):
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)


while True:
    touch1 = cap.touched() << 1
    touch2 = cap2.touched() << 1
    
    touch1 = touch1 & -touch1
    touch2 = touch2 & -touch2


    #if touch1 and touch1 & before1:
    if touch1:

        # サーチ開始
        for i in range(13):
            pin_bit = 1 << i

            if touch1 & pin_bit:
                current1 = pin_bit

                # 前回タッチ位置が何もなかった場合
                if not before1:
                    before1 = pin_bit
                    continue

                if not current1 & before1:

                    if current1 - before1 > 0:
                        touch1_input = "touch1: <-"
                        touch1_in = -1
                        before1 = current1

                    elif current1 - before1 <= 0: 
                        touch1_input = "touch1: ->"
                        touch1_in = 1
                        before1 = current1

            '''
            elif touch1 & pin_bit and pin_bit & before1:
            elif touch1 & pin_bit and pin_bit & before1:
                before1 = current1
            '''

    else:
        current1 = 0
        touch1_in = 0
        before1 = 0b0
        touch1_input = "touch1: --"

    #if touch2 and touch2 & before2:
    if touch2:
        for i in range(13):
            pin_bit = 1 << i

            if touch2 & pin_bit and not pin_bit & before2:
                current2 = pin_bit

                # 前回タッチ位置が何もなかった場合
                if not before2:
                    before2 = pin_bit
                    continue

                if current2 - before2 > 0:
                    touch2_input = "touch2: <-"
                    touch2_in = -1
                elif current2 - before2 < 0: 
                    touch2_input = "touch2: ->"
                    touch2_in = 1
                before2 = current2
                continue

            elif touch2 & pin_bit and pin_bit & before2:
                before2 = current2

        before2 = current2

    else:
        current2 = 0
        touch2_in = 0
        before2 = 0b0
        touch2_input = "touch2: --"


    if touch1_in == -1:
        pi.digitalWrite(L1_PIN, pi.HIGH)
    elif touch1_in == 1:
        pi.digitalWrite(R1_PIN, pi.HIGH)
    else:
        pi.digitalWrite(L1_PIN, pi.LOW)
        pi.digitalWrite(R1_PIN, pi.LOW)

    if touch2_in == -1:
        pi.digitalWrite(L2_PIN, pi.HIGH)
    elif touch2_in == 1:
        pi.digitalWrite(R2_PIN, pi.HIGH)
    else:
        pi.digitalWrite(L2_PIN, pi.LOW)
        pi.digitalWrite(R2_PIN, pi.LOW)

    
    print("\r",format(touch1,"012b") ,format(current1,"012b") ,touch1_input, touch2_input, format(current2,"012b"), format(touch2,"012b"), end="")
    #print(format(touch1,"012d") ,touch1_input, touch2_input, format(touch2,"012d"))
