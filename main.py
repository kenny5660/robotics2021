from time import sleep
import serial
import os
import vision
import cv2
import RPi.GPIO as GPIO
from queue import Queue, Empty
import OCServo

if os.name == 'nt':
        ser = serial.Serial('COM5', 1000000, timeout=1)
else:
    ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=1)

main_servo = OCServo.OCServo301()
main_servo.connect(ser,1)
MAIN_SERVO_RESET = 0
MAIN_SERVO_STEP = 51.43

def set_cup(cup_num):
    main_servo.setDegrees((MAIN_SERVO_STEP*cup_num+MAIN_SERVO_RESET)%360)


PIN_OPTIC_PAIR_1 = 3
PIN_OPTIC_PAIR_2 = 5
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_OPTIC_PAIR_1, GPIO.IN)
GPIO.setup(PIN_OPTIC_PAIR_2, GPIO.IN)

queue_brick_detect = Queue()
GPIO.add_event_detect(PIN_OPTIC_PAIR_1, GPIO.FALLING, queue_brick_detect.put)
GPIO.add_event_detect(PIN_OPTIC_PAIR_2, GPIO.FALLING, queue_brick_detect.put)


i = 0
set_cup(0)
while True:
    try:
        event = queue_brick_detect.get()
        print("detect "+str(i))
        i+=1
        set_cup(i)
        queue_brick_detect.queue.clear()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
    
