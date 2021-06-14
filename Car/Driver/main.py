import socketio

from socketclient import Client
from arduino_connector import ArduinoConnector
from qr_object_detection import CarVision
from wifi_triangulation import WifiTriangulation
import time
# QT_X11_NO_MITSHM=1 python main.py


sio = None
try:
    sio = socketio.Client()
    # sio.connect('http://localhost:3003/')
    sio.connect('http://craaxcloud.epsevg.upc.edu:35302/')
    print('[INFO] Connected to socket')
except socketio.exceptions.ConnectionError:
    print('[ERROR] Server is off')


@sio.event
def notification(data):
    print('[INFO] Notification: ', data)
    socket.update_status(2)
    vision_module.set_qr_search(data)


@sio.event
def message(data):
    print('[INFO] Message: ', data)


@sio.event
def bad_status(data):
    print('[ERROR] Bad status:', data)


@sio.event
def bad_notify(data):
    print('[ERROR] Bad notify:', data)


@sio.event
def connect():
    print("[INFO] Connected!")
    socket.send('id', socket.id)


@sio.event
def connect_error():
    print("[ERROR] The connection failed!")


@sio.event
def disconnect():
    print("[INFO] Disconnected!")


socket = Client(sio, "CH0002")
time.sleep(10)
arduino_module = ArduinoConnector()

vision_module = CarVision(arduino_module, socket)
vision_module.start()

wifi_tri = WifiTriangulation(socket, vision_module)
wifi_tri.start()

while vision_module.running:
    option = input('[Info] pres q to exit')
    if option == 'q':
        print('[INFO] ...')
        vision_module.finish()
    elif option == 'n':
        vision_module.set_qr_search("12343:12345")
    elif option == 'r':
        vision_module.find_next_qr_search()
    elif option == 's':
        vision_module.set_stop_car(False)
    elif option == 'x':
        vision_module.set_stop_car(True)

vision_module.join()
wifi_tri.join()
socket.disconnect()
arduino_module.close()

print('END')
