from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from threading import Thread
import matplotlib.pyplot as plt
import time
import math


def triangulate(points):
    ws = sum((p[2]) for p in points.values())
    if ws == 0:
        return [0, 0, 1]
    points = tuple((x, y, (signal / ws)) for (x, y, signal) in points.values())

    return [sum(p[0] * p[2] for p in points),  # x
            sum(p[1] * p[2] for p in points),  # y
            1]


def calc_distance(signalLevelInDb, freqInMHz):
    # distance = 10 ^ ((27.55 - (20 * log10(frequencyInMHz)) + signalLevelInDb)/20)
    exp = (27.55 - (20 * (math.log10(freqInMHz))) + abs(signalLevelInDb)) / 20.0
    return 10 ** exp


def read_csv():
    dict_poss = {}
    import csv
    with open('wifitriangulation/wifi_dictionary.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dict_poss[row[0]] = [int(num) for num in row[1:]]
    return dict_poss


class WifiTriangulation(Thread):
    running = True
    dict_wifi = {}
    dict_poss = read_csv()
    img = plt.imread("wifitriangulation/terminal2posicionament.png")

    def __init__(self, interface, socket):
        super().__init__()
        self.interface = interface
        self.socket = socket

    def run(self):
        print("[INFO] Starting wifi module ...")

        print("[WIFI_MODULE] Configuring wifi tu mode monitor ...")
        # os.system("ifconfig "+self.interface+" down")
        # time.sleep(1)
        # os.system("iwconfig "+self.interface+" mode monitor")
        # time.sleep(1)
        # os.system("ifconfig "+self.interface+" up")
        # time.sleep(3)

        # start the channel changer
        channel_changer = Thread(target=self.change_channel)
        channel_changer.daemon = True
        channel_changer.start()

        # start sniffing
        channel_changr = Thread(target=self.snif)
        channel_changr.daemon = True
        channel_changr.start()

        print("[WIFI_MODULE] Starting triangulation ...")
        self.triangulating()

        os.system("ifconfig " + self.interface + " down")
        os.system("ifconfig " + self.interface + " up")
        print("[INFO] Wifi module finished")

    def triangulating(self):
        time.sleep(8)
        while self.running:
            for k in self.dict_poss.keys():
                if k in self.dict_wifi:
                    self.dict_poss[k][2] = pow((75 + self.dict_wifi[k][1]), 3)
                else:
                    self.dict_poss[k][2] = 0
            self.dict_poss["cotxe"] = triangulate(self.dict_poss)

            self.generate_plot()

            self.socket.update_position(self.dict_poss["cotxe"][0], self.dict_poss["cotxe"][1])

            self.dict_wifi.clear()
            time.sleep(8)
        print("[WIFI_MODULE] Stoping wifi module...")

    def change_channel(self):
        ch = 1
        while self.running:
            os.system(f"iwconfig {self.interface} channel {ch}")
            ch = ch % 14 + 1
            time.sleep(0.5)

    def snif(self):
        sniff(prn=self.callback, iface=self.interface)

    def callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            channel = packet[Dot11Beacon].network_stats().get("channel")
            frequency = packet[0][RadioTap].Channel
            try:
                dbm_signal = packet.dBm_AntSignal
                distance = calc_distance(dbm_signal, frequency)
            except Exception:
                dbm_signal = -75
                distance = 9999
            self.dict_wifi[bssid] = [ssid, dbm_signal, channel, frequency, distance]

    def generate_plot(self):
        x_axis = []
        y_axis = []
        for (x, y, signal) in self.dict_poss.values():
            if signal > 0:
                x_axis.append(x)
                y_axis.append(y)

        color = list('Blue' for i in range(len(x_axis) - 1))
        color.append('Green')

        plt.imshow(self.img)

        plt.plot(x_axis[-1], y_axis[-1], 'go')
        # plt.scatter(x_axis, y_axis, color=color)

        for i in range(len(x_axis) - 1):
            plt.plot([x_axis[i], x_axis[-1]], [y_axis[i], y_axis[-1]], 'r-')

        plt.draw()
        plt.pause(0.001)
        plt.clf()

    def finish(self):
        self.running = False
