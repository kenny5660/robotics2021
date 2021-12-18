import serial
import os
import vision
import cv2
import RPi.GPIO as GPIO
from queue import Queue, Empty




PIN_OPTIC_PAIR_1 = 3
PIN_OPTIC_PAIR_2 = 5
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_OPTIC_PAIR_1, GPIO.IN)
GPIO.setup(PIN_OPTIC_PAIR_2, GPIO.IN)

queue_brick_detect = Queue()
GPIO.add_event_detect(PIN_OPTIC_PAIR_1, GPIO.RISING, queue_brick_detect.put)
GPIO.add_event_detect(PIN_OPTIC_PAIR_2, GPIO.RISING, queue_brick_detect.put)


i = 0
while True:
    try:
        event = queue_brick_detect.get()
        print("detect "+str(i))
        i+=1
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
    
