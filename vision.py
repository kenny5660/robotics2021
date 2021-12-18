import cv2
import numpy as np


def fun():
    cv2.namedWindow("test")
    cap = cv2.VideoCapture(0)

    low = np.array((10,70,70), np.uint8)
    high = np.array((150,255,255), np.uint8)
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
    cap.release()
    cv2.destroyAllWindows()
