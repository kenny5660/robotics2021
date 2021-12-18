import numpy as np
class OCServo:
    def __init__(self) -> None:
        self.serial = None
        self.SERVO_D_INSTRUCTION_WRITE = int("0x03", base=16)
        self.SERVO_D_LEAD_MID = 100.0 
        self.SERVO_D_INSTRUCTION_PING =int("0x01",base=16)
        self.SERVO_D_INSTRUCTION_READ =int("0x02",base=16)
        self.SERVO_D_INSTRUCTION_WRITE =int("0x03",base=16)
        self.SERVO_D_INSTRUCTION_REG_WRITE =int("0x04",base=16)
        self.SERVO_D_INSTRUCTION_ACTION =int("0x05",base=16)
        self.SERVO_D_INSTRUCTION_SYNC_WRITE =int("0x83",base=16)
        self.SERVO_D_INSTRUCTION_RESET =int("0x06",base=16)
        self.SERVO_D_PACKET_ID =int("2",base=10)
        self.SERVO_D_PACKET_LENGTH =int("3",base=10)
        self.SERVO_D_PACKET_INSTRUCTION =int("4",base=10)
        self.SERVO_D_PACKET_PARAMS =int("5",base=10)
        self.SERVO_D_PACKET_STATE =int("4",base=10)
        self.SERVO_D_BROADCAST_ID =int("0xFE",base=16)
        self.SERVO_D_ADDR_TORQUE_SWITCH =int("0x28",base=16)
        self.SERVO_D_ADDR_GOAL_POSITION =int("0x2A",base=16)   
        self.SERVO_D_ADDR_OPERATION_SPEED =int("0x2E",base=16)   
        self.SERVO_D_ADDR_OPERATION_TIME =int("0x2C",base=16)   
        self.SERVO_D_ADDR_CURRENT_LEAD =int("0x3C",base=16)     
        self.SERVO_D_ADDR_CURRENT_TEMP =int("0x3F",base=16)
        self.SERVO_D_ADDR_CURRENT_POSITION =int("0x38",base=16) 

    def connect(self,serial,id):
        self.serial = serial
        self.id = id
    def setDegrees(self,deg,isWait,time_ms):
        pass
    def getDegrees(self):
        pass
    def enable(self):
        pass
    def disable(self):
        pass
    def sendData(self,addr,data):
        size = len(data)
        check_sum = np.uint8(0)
        check_sum = (self.id + 3 + size + self.SERVO_D_INSTRUCTION_WRITE + addr)
        data_packet = [i for i in range(size+7)]
        for i in range(size):
            data_packet[self.SERVO_D_PACKET_PARAMS + 1 + i] = data[i]
            check_sum += data[i]

        check_sum = np.uint8(~(check_sum))
        data_packet[0] = int("0xff",base=16)
        data_packet[1] = int("0xff",base=16)
        data_packet[self.SERVO_D_PACKET_ID] = self.id
        data_packet[self.SERVO_D_PACKET_LENGTH] = 3 + size
        data_packet[self.SERVO_D_PACKET_INSTRUCTION] = self.SERVO_D_INSTRUCTION_WRITE
        data_packet[self.SERVO_D_PACKET_PARAMS] = addr
        data_packet[3 + data_packet[self.SERVO_D_PACKET_LENGTH]] = check_sum

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.serial.write(data_packet)
        self.serial.flush()
        return_pucket = [i for i in range(6)]
        #return_pucket = self.serial.read(6)
        return return_pucket[self.SERVO_D_PACKET_STATE]

    def readData(addr):
        pass

class OCServo301(OCServo):
    def __init__(self) -> None:
        super().__init__()
        self.serial = None
        self.SERVO_D_301_DEGREE_COEF = 0.0879120879120879
        self.kMaxServoDeg = 4095;  
        self.kMinServoDeg = 0; 
    def setDegrees(self, deg, isWait=False, time_ms=0,speed=-1):
        data = [i for i in range(6)]
        servo_deg = int(deg / self.SERVO_D_301_DEGREE_COEF)%self.kMaxServoDeg
        servo_deg_bytes = servo_deg.to_bytes(2, byteorder='little')
        time_ms_bytes = time_ms.to_bytes(2, byteorder='little')
        if speed == -1:
            speed = 4095
        speed_bytes = speed.to_bytes(2, byteorder='little')
        data[1] = servo_deg_bytes[1]
        data[0] = servo_deg_bytes[0]
        data[2] = time_ms_bytes[0]
        data[3] = time_ms_bytes[1]
        data[4] = speed_bytes[0]
        data[5] = speed_bytes[1]
        self.sendData(self.SERVO_D_ADDR_GOAL_POSITION, data)
        if isWait:
            pass
    def setMode(self,str_mode):
        if str_mode == "motor":
            self.sendData(int("0x23",base=16), [1])
        else:
            self.sendData(int("0x23",base=16), [0])
    def setSpeed(self, speed):
        data = [i for i in range(2)]
        if speed == -1:
            speed = 4095
        speed_bytes = speed.to_bytes(2, byteorder='little')
        data[0] = speed_bytes[0]
        data[1] = speed_bytes[1]
        self.sendData(int("0x2E",base=16), data)

if __name__ == "__main__":
    import os
    import serial
    from time import sleep
    if os.name == 'nt':
        ser = serial.Serial('COM5', 1000000, timeout=1)
    else:
        ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=1)
    main_servo = OCServo301()
    main_servo.connect(ser,1)
    main_servo.setMode("servo")
    sleep(1)
    main_servo.setDegrees(200,speed=1000)
    sleep(1)
    main_servo.setMode("motor")
    sleep(1)
    main_servo.setSpeed(0)
    main_servo.setSpeed(33000)
