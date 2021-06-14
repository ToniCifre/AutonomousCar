import serial


class ArduinoConnector:

    def __init__(self):
        print("[INFO] Starting arduino connector module ...")
        self.actual_code = 0
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        except serial.serialutil.SerialException:
            print('[ERROR] connection to arduino')

    def send(self, code):
        if code != self.actual_code:
            if code == 0:
                print(0)
                # self.arduino.write('s')  # Stop
            elif code == 1:
                print(0)
                # self.arduino.write('m')  # Stop
            elif code == 2:
                print(2)
                # self.arduino.write('f')  # Full
            else:
                print('[WARNING] Bad Code')
            self.actual_code = code

    def close(self):
        print("[INFO] Stopping arduino connector module ...")
        self.arduino.close()
