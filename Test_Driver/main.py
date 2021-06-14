from apiconnection.socketclient import Client
from driverconnection.arduino_connector import ArduinoConnector
from wifitriangulation.wifi_triangulation import WifiTriangulation
from carvision.qr_object_detection import CarVision

# QT_X11_NO_MITSHM=1 python main.py


@Client.sio.event
def notification(data):
    vision_module.set_qr_search(data)
    print('[INFO] Notification: ', data)


@Client.sio.event
def message(data):
    print('[INFO] Message: ', data)


@Client.sio.event
def bad_status(data):
    print('[ERROR] Bad status:', data)


@Client.sio.event
def bad_notify(data):
    print('[ERROR] Bad notify:', data)


@Client.sio.event
def connect():
    socket.isConnected = True
    socket.send('id', socket.id)
    print("[INFO] Connected!")


@Client.sio.event
def connect_error():
    print("[ERROR] The connection failed!")


@Client.sio.event
def disconnect():
    socket.isConnected = False
    print("[INFO] Disconnected!")


socket = Client()

# Wifi interface mode monitor
wifi_module = WifiTriangulation("wlx00c0ca665094", socket)
wifi_module.setDaemon(True)
wifi_module.start()

arduino_module = ArduinoConnector()

vision_module = CarVision(arduino_module, socket)
vision_module.start()


while vision_module.running:
    option = input('[Info] pres q to exit')
    if option == 'q':
        print('[INFO] Exit')
        vision_module.finish()
    elif option == 'r':
        rute = input('[Info] Enter rute')
        # rute -> 12342:12341  source:destination
        vision_module.set_qr_search(rute)
    elif option == 's':
        vision_module.set_stop_car(False)


wifi_module.finish()
vision_module.join()
wifi_module.join()
socket.disconnect()

print('END')

