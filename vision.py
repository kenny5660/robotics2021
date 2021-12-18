import cv2
import numpy as np

low = np.array((0,0,0), np.uint8)
high = np.array((180,255,255), np.uint8)

def low_change_h(x):
    low[0] = x

def low_change_s(x):
    low[1] = x

def low_change_v(x):
    low[2] = x

def high_change_h(x):
    high[0] = x

def high_change_s(x):
    high[1] = x

def high_change_v(x):
    high[2] = x


def fun():
    cv2.namedWindow("test")
    cap = cv2.VideoCapture(0)
    cv2.createTrackbar("l_h","test", 0, 180, low_change_h)
    cv2.createTrackbar("l_s","test", 0, 255, low_change_s)
    cv2.createTrackbar("l_v","test", 0, 255, low_change_v)
    cv2.createTrackbar("h_h","test", 180, 180, high_change_h)
    cv2.createTrackbar("h_s","test", 255, 255, high_change_s)
    cv2.createTrackbar("h_v","test", 255, 255, high_change_v)
    
    while True:
        flag, img = cap.read()
        
        try:
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv,low,high) 
            
            cv2.imshow('test',mask)
        except:
            cap.release()
            raise
        ch = cv2.waitKey(5)
        if (ch == 27):
            break
        if (ch == ord('a')):
            low[0]+= 5;
    cap.release()
    cv2.destroyAllWindows()
