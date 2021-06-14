from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from pyzbar import pyzbar
from threading import Thread


class CarVision(Thread):
    is_search_qr = False
    qr_search = "none"
    next_qr_search = ""
    stop_car = False

    def __init__(self, arduino_module, socket):
        super().__init__()

        self.arduino_module = arduino_module
        self.socket = socket

        self.running = True

        print("[INFO] loading AI model...")
        self.net = cv2.dnn.readNetFromCaffe('carvision/model/Mode.prototxt.txt', 'carvision/model/Mode.caffemodel')

    def run(self):
        print("[INFO] Starting vision module...")
        self.running = True

        cap = VideoStream(src=0).start()
        # cap = VideoStream(usePiCamera=True).start()

        time.sleep(2.0)
        while self.running:
            frame = cap.read()
            frame = imutils.resize(frame, width=600)

            if not self.stop_car:
                self.check_for_object(frame)
                if self.is_search_qr:
                    self.check_for_code(frame)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        print("[INFO] Stopping vision module...")
        cap.stop()
        cv2.destroyAllWindows()
        self.running = False

    def check_for_object(self, frame):
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections = self.net.forward()

        (h, w) = frame.shape[:2]

        stat = 2
        color = (255, 0, 0)
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if (endY - startY) / h < 0.95 and (endX - startX) / w < 0.95:
                    if endY / h > 0.6 and (startX / w < 0.8 and endX / w > 0.2):
                        stat = 0
                        color = (0, 0, 255)
                    elif endY / h > 0.4 and stat > 1:
                        stat = 1
                        color = (0, 255, 255)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        if not self.stop_car:
            self.arduino_module.send(stat)

    def check_for_code(self, frame):
        codes = pyzbar.decode(frame)
        for code in codes:
            if self.qr_search == code.data.decode("utf-8"):
                self.is_search_qr = False
                self.stop_car = True
                self.arduino_module.send(0)
                self.socket.send_notification(self.qr_search)
                self.qr_search = "none"

                print('[VISION_MODULE] ', self.qr_search, ' code found...')
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def set_qr_search(self, qr):
        print('[VISION_MODULE] Searching ', qr.split(':')[0], ' code...')
        self.qr_search = qr.split(':')[0]
        self.next_qr_search = qr.split(':')[1]
        self.is_search_qr = True

    def find_next_qr_search(self):
        print('[VISION_MODULE] Searching ', self.next_qr_search, ' code...')
        self.qr_search = self.qr_search
        self.next_qr_search = ""
        self.is_search_qr = True
        self.stop_car = False

    def set_stop_car(self, is_stop):
        self.stop_car = is_stop

    def finish(self):
        self.running = False
