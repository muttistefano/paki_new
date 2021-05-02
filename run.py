import schedule
import time
import board
import Adafruit_DHT
from digitalio import DigitalInOut, Direction
import threading
import collections
from datetime import datetime
from statistics import mean
from schedule import every, repeat, run_pending


class PakiController(object):

    def __init__(self):
        
        self.temp_init()
        # self.rele_init()
        self.start_threads()
        self.run_app()

    def Light1On(self):
        print("Turning light 1 On")
        self.rele1.value = True
        time.sleep(0.5)

    def Light1Off(self):
        print("Turning light 1 Off")
        self.rele1.value = False
        time.sleep(0.5)

    def Light2On(self):
        print("Turning light 2 On")
        self.rele2.value = True
        time.sleep(0.5)

    def Light2Off(self):
        print("Turning light 2 Off")
        self.rele2.value = False
        time.sleep(0.5)

    def log_to_file(self):
        print("Logging data to file")
        now = datetime.now()
        s1 = now.strftime("%Y-%d-%m-%H:%M:%S")
        str_log = s1 + " " + str(mean(self.t1_queue)) + " " + str(mean(self.h1_queue)) + " " + str(mean(self.t2_queue)) + " " + str(mean(self.h2_queue)) + " " + str(mean(self.t3_queue))  + " " + str(mean(self.h3_queue)) + " 1 1 1 1 1 1\n" 
        
        with open("log.csv", "a") as f:
            f.write(str(str_log))

    def log_queue(self):
        print("Reading data from sensors")
        self.temp_read()
        self.t1_queue.append(self.t1)
        self.t2_queue.append(self.t2)
        self.h1_queue.append(self.h1)
        self.h2_queue.append(self.h2)
        self.t3_queue.append(self.t3)
        self.h3_queue.append(self.h3)
        
    def temp_init(self):
        self.t1, self.h1 = 0, 0
        self.t2, self.h2 = 0, 0
        self.t3, self.h3 = 0, 0
        self.t1_queue = collections.deque(maxlen=30)
        self.h1_queue = collections.deque(maxlen=30)
        self.t2_queue = collections.deque(maxlen=30)
        self.h2_queue = collections.deque(maxlen=30)
        self.t3_queue = collections.deque(maxlen=30)
        self.h3_queue = collections.deque(maxlen=30)

    def rele_init(self):
        self.rele1           = DigitalInOut(board.D23)
        self.rele1.direction = Direction.OUTPUT
        self.rele1.value     = False
        self.rele2           = DigitalInOut(board.D24)
        self.rele2.direction = Direction.OUTPUT
        self.rele2.value     = False
        self.rele3           = DigitalInOut(board.D27)
        self.rele3.direction = Direction.OUTPUT
        self.rele3.value     = False
        self.rele4           = DigitalInOut(board.D18)
        self.rele4.direction = Direction.OUTPUT
        self.rele4.value     = False

    def temp_read(self):
        while True:
            try:
                self.h1 , self.t1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 21)
                self.h2 , self.t2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 20)
                self.h3 , self.t3 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 16)
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

    def temp_check(self):
        pass

    def start_threads(self):
        temp_th_idx  = threading.Thread(target=self.temp_check)
        temp_th_idx.start()
        temp_th_idx2 = threading.Thread(target=self.temp_read)
        temp_th_idx2.start()
        return True

    def run_app(self):
        while True:
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t1, self.h1))
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t2, self.h2))
            print("Temp: {:.1f} C    Humidity: {}% ".format( self.t3, self.h3))
            time.sleep(1)
        


if __name__ == "__main__":
    PakiController()
 


