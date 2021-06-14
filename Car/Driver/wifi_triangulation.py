import csv
import time
from threading import Thread
from random import randrange


class WifiTriangulation(Thread):

    def __init__(self, socket, vision):
        super().__init__()

        self.cami = list(csv.reader(open('cami.csv', 'r')))
        self.socket = socket
        self.vision = vision

    def run(self):
        print("[INFO] Starting triangulation module...")
        pos = randrange(469)
        while pos < len(self.cami) and self.vision.running:
            row = self.cami[pos]
            self.socket.update_position(int(row[0]), int(row[1][1:]))
            time.sleep(3)
            if not self.vision.stop_car:
                pos += 2

        pos = 1
        while pos < len(self.cami) and self.vision.running:
            row = self.cami[pos]
            self.socket.update_position(int(row[0]), int(row[1][1:]))
            time.sleep(3)
            if not self.vision.stop_car:
                pos += 2
        print("[INFO] Stopping triangulation module...")
