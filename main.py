from time import sleep
import serial
import os
import vision
import cv2
import RPi.GPIO as GPIO
from queue import Queue, Empty
import OCServo
import vision
GPIO.setmode(GPIO.BOARD)
MAIN_SERVO_RESET = 0
MAIN_SERVO_STEP = 51.43

PIN_BUTTON_1 = 37
PIN_BUTTON_2 = 36
GPIO.setup(PIN_BUTTON_1, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BUTTON_2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
cur_deg = MAIN_SERVO_RESET
if os.name == 'nt':
        ser = serial.Serial('COM5', 1000000, timeout=1)
else:
    ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=1)

main_servo = OCServo.OCServo301()
main_servo.connect(ser,1)
main_servo.setMode("servo")

def set_cup(cup_num):
    global cur_deg
    cup_num = cup_num % 7
    deg = (MAIN_SERVO_STEP*cup_num+MAIN_SERVO_RESET)%360
    if (deg ==0) and (cur_deg > 180):
        deg = 359.9
    cur_deg = deg
    main_servo.setDegrees(cur_deg,speed=4095)


PIN_OPTIC_PAIR_1 = 3
PIN_OPTIC_PAIR_2 = 5

GPIO.setup(PIN_OPTIC_PAIR_1, GPIO.IN)
GPIO.setup(PIN_OPTIC_PAIR_2, GPIO.IN)
queue_brick_detect = Queue()
queue_buttons = Queue()
GPIO.add_event_detect(PIN_OPTIC_PAIR_1, GPIO.FALLING, queue_brick_detect.put)
GPIO.add_event_detect(PIN_OPTIC_PAIR_2, GPIO.FALLING, queue_brick_detect.put)

GPIO.add_event_detect(PIN_BUTTON_1, GPIO.FALLING, queue_buttons.put)
GPIO.add_event_detect(PIN_BUTTON_2, GPIO.FALLING, queue_buttons.put)


i = 0
set_cup(0)
while True:
    #GPIO.cleanup()
    #
    cur_deg = MAIN_SERVO_RESET
    set_cup(0)
    but_num = queue_buttons.get()
    if but_num == PIN_BUTTON_1:
        os.system('libcamera-jpeg -o main1080.jpg -t 1 --width 2592  --height 1944')
        img1 = cv2.imread("main1080.jpg")
        queue_brics = vision.to_qeue(img1)
        vision.test_trash(img1)
    else:
        queue_brics = [0,1,2,3,4,5,6,7]
    #GPIO.wait_for_edge(PIN_BUTTON_START, GPIO.FALLING)
    queue_brick_detect.queue.clear()
    for i in range(6):
        try:
            event = queue_brick_detect.get()
            print("detect "+str(i))
            i+=1
            set_cup(queue_brics[i])
            sleep(0.3)
            queue_brick_detect.queue.clear()
        except KeyboardInterrupt:
            #GPIO.cleanup()
            exit()
    queue_buttons.queue.clear()
    sleep(2)
    
