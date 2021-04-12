import time
import board
import adafruit_dht
from digitalio import DigitalInOut, Direction
import threading
import collections


class PakiController(object):

    def __init__(self):
        self.temp_init()
        self.rele_init()
        self.start_threads()
        self.run_app()

    def temp_init(self):
        self.dhtDevice1 = adafruit_dht.DHT22(board.D21)
        self.dhtDevice2 = adafruit_dht.DHT22(board.D20)
        self.t1, self.h1 = 0, 0
        self.t2, self.h2 = 0, 0
        self.t1_queue = collections.deque(maxlen=1000)
        self.t2_queue = collections.deque(maxlen=1000)
        self.h1_queue = collections.deque(maxlen=1000)
        self.h2_queue = collections.deque(maxlen=1000)

    def log_queue(self):
        self.t1_queue.append(self.t1)
        self.t2_queue.append(self.t2)
        self.h1_queue.append(self.h1)
        self.h2_queue.append(self.h2)

    def rele_init(self):
        rele1           = DigitalInOut(board.D23)
        rele1.direction = Direction.OUTPUT
        rele1.value     = False
        rele2           = DigitalInOut(board.D24)
        rele2.direction = Direction.OUTPUT
        rele2.value     = False
        rele3           = DigitalInOut(board.D27)
        rele3.direction = Direction.OUTPUT
        rele3.value     = False
        rele4           = DigitalInOut(board.D18)
        rele4.direction = Direction.OUTPUT
        rele4.value     = False

    def temp_thread(self):
        while True:
            try:
                self.t1 = self.dhtDevice1.temperature
                self.h1 = self.dhtDevice1.humidity
                self.t2 = self.dhtDevice2.temperature
                self.h2 = self.dhtDevice2.humidity
                self.log_queue()
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error

    def start_threads(self):
        temp_th_idx = threading.Thread(target=self.temp_thread)
        temp_th_idx.start()
        return True

    def run_app(self):
        while True:
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t1, self.h1))
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t2, self.h2))
            time.sleep(1)
        
 


