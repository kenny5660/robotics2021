import cv2
import subprocess as sp
import numpy
from time import sleep
import os
import sys
command = "/usr/bin/gst-launch-1.0 libcamerasrc ! video/x-raw,width=1920,height=1080! ! fdsink"
#pipe = sp.Popen(["/usr/bin/gst-launch-1.0", "libcamerasrc","! video/x-raw,width=2592,height=1944","! videoconvert","! fdsink"], stdout = sp.PIPE, bufsize=10**8)

cap = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    #raw_image = sys.stdin.buffer.read(1920*1080*3)
    # transform the byte read into a numpy array
    #image =  numpy.frombuffer(raw_image, dtype='uint8')
    #image = image.reshape((1080,1920,3))          # Notice how height is specified first and then width
    ret, image = cap.read()
    if image is not None:
        cv2.imwrite('test.jpg', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sys.stdin.flush()