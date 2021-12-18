import cv2
import subprocess as sp
import numpy

command = "gst-launch-1.0 libcamerasrc ! video/x-raw ! fdsink"
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

cap = cv2.VideoCapture(stream_cmd)
while True:
    # Capture frame-by-frame
    raw_image = pipe.stdout.read(640*480*3)
    # transform the byte read into a numpy array
    image =  numpy.fromstring(raw_image, dtype='uint8')
    image = image.reshape((480,640,3))          # Notice how height is specified first and then width
    if image is not None:
        cv2.imwrite('test.jpg', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pipe.stdout.flush()

cv2.destroyAllWindows()


