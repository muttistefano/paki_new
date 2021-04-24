import time
import board
import Adafruit_DHT
from digitalio import DigitalInOut, Direction
import threading
import collections
from datetime import datetime



class PakiController(object):

    def __init__(self):
        self.log_file = open("log.csv","a")

        self.temp_init()
        # self.rele_init()
        self.start_threads()
        self.run_app()

    def temp_init(self):
        self.t1, self.h1 = 0, 0
        self.t2, self.h2 = 0, 0
        self.t3, self.h3 = 0, 0
        self.t1_queue = collections.deque(maxlen=10)
        self.h1_queue = collections.deque(maxlen=10)
        self.t2_queue = collections.deque(maxlen=10)
        self.h2_queue = collections.deque(maxlen=10)
        self.t3_queue = collections.deque(maxlen=10)
        self.h3_queue = collections.deque(maxlen=10)

    def log_queue(self):
        self.t1_queue.append(self.t1)
        self.t2_queue.append(self.t2)
        self.h1_queue.append(self.h1)
        self.h2_queue.append(self.h2)
        self.t3_queue.append(self.t3)
        self.h3_queue.append(self.h3)
        now = datetime.now()
        s1 = now.strftime("%m-%d-%Y-%H:%M:%S")
        str_log = s1 + " " + str(self.t1) + " " + str(self.h1) + " " + str(self.t2) + " " + str(self.h2) + " " + str(self.t3) + " " + str(self.h3) + "1 1 \n" 
        self.log_file.write(str_log)

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
                self.h1 , self.t1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 21)
                # self.h2 , self.t2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 20)
                # self.h3 , self.t3 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 16)
                self.log_queue()
                time.sleep(2)
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                print(error.args[0])
                print("MegaPD")
                continue

    def start_threads(self):
        temp_th_idx = threading.Thread(target=self.temp_thread)
        temp_th_idx.start()
        return True

    def run_app(self):
        while True:
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t1, self.h1))
            # print("Temp: {:.1f} C    Humidity: {}% ".format( self.t2, self.h2))
            time.sleep(1)
        


if __name__ == "__main__":
    PakiController()
 


