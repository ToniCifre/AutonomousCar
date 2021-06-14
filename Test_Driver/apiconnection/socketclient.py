import socketio  # pip install "python-socketio[client]"


class Client:
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3003')
    except socketio.exceptions.ConnectionError:
        print('[ERROR] Server is off')

    def __init__(self):
        self.isConnected = False
        self.id = '654456'
        self.sio.emit('id', self.id)

    def update_position(self, lat, lon):
        print('pos: ', lat, lon)
        # self.sio.emit('position', (str(lat), str(lon)))

    def update_status(self, status):
        self.sio.emit('status', status)

    def send_notification(self, notify):
        print('Notificació: ', notify)
        # self.sio.emit('notification', notify)

    def send(self, key, msg):
        self.sio.emit(key, msg)

    def disconnect(self):
        self.sio.disconnect()
#
#
# @Client.sio.event
# def notification(data):
#     print('[INFO] Notification: ', data)
#
#
# @Client.sio.event
# def message(data):
#     print('[INFO] Message: ', data)
#
#
# @Client.sio.event
# def bad_status(data):
#     print('[ERROR] Bad status:', data)
#
#
# @Client.sio.event
# def bad_notify(data):
#     print('[ERROR] Bad notify:', data)
#
#
# @Client.sio.event
# def connect():
#     socket.isConnected = True
#     socket.send('id', socket.id)
#     print("[INFO] Connected!")
#
#
# @Client.sio.event
# def connect_error():
#     print("[ERROR] The connection failed!")
#
#
# @Client.sio.event
# def disconnect():
#     socket.isConnected = False
#     print("[INFO] Disconnected!")
#
#
# socket = Client()
