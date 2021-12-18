import cv2
import os
os.system('libcamera-jpeg -o main1080.jpg -t 10 --width 1920 --height 1080')

img = cv2.imread("main1080.jpg")

cv2.imwrite('test.jpg', img)

