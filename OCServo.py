class OCServo:
    def __init__(self) -> None:
        self.serial = None
    def connect(self,serial):
        self.serial = serial
    def setDegrees(deg,isWait,time_ms):
        pass
    def getDegrees():
        pass
    def enable():
        pass
    def disable():
        pass
    def sendData(addr,data):
        pass
    def readData(addr):
        pass

class OCServo301(OCServo):
    def __init__(self) -> None:
        self.serial = None
