import time
import board
import adafruit_dht
import RPi.GPIO as GPIO  
from digitalio import DigitalInOut, Direction
import threading
import collections
from datetime import datetime
from statistics import mean
import schedule


class PakiController(object):

    def __init__(self):
        
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.dhtDevice1 = adafruit_dht.DHT22(board.D16, use_pulseio=False)
        self.dhtDevice2 = adafruit_dht.DHT22(board.D20, use_pulseio=False)
        self.dhtDevice3 = adafruit_dht.DHT22(board.D21, use_pulseio=False)

        schedule.every().day.at("16:20").do(self.Light1On)
        schedule.every().day.at("16:21").do(self.Light1Off)
        schedule.every().day.at("16:05").do(self.Light2On)
        schedule.every().day.at("16:05").do(self.Light2Off)



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
                print("Reading data from sensors")
                self.t1      = self.dhtDevice1.temperature
                self.h1      = self.dhtDevice1.humidity
                self.t2      = self.dhtDevice2.temperature
                self.h2      = self.dhtDevice2.humidity
                self.t3      = self.dhtDevice3.temperature
                self.h3      = self.dhtDevice3.humidity
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
        print("threads started")
        return True

    def run_app(self):
        while True:
            # print("Temp: {:.1f} C    Humidity: {}% ".format( self.t1, self.h1))
            # print("Temp: {:.1f} C    Humidity: {}% ".format( self.t2, self.h2))
            # print("Temp: {:.1f} C    Humidity: {}% ".format( self.t3, self.h3))
            schedule.run_pending()
            time.sleep(5)
        


if __name__ == "__main__":
    PakiController()
 


