import serial
import os
import vision
if os.name == 'nt':
    ser = serial.Serial('COM5', 19200, timeout=1)
else:
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)


vision.fun()
