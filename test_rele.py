from digitalio import DigitalInOut, Direction
import board
import time

state_r = True

while (True):

    rele1           = DigitalInOut(board.D23)
    rele1.direction = Direction.OUTPUT
    rele1.value     = state_r  
    rele2           = DigitalInOut(board.D24)
    rele2.direction = Direction.OUTPUT
    rele2.value     = state_r 
    rele3           = DigitalInOut(board.D27)
    rele3.direction = Direction.OUTPUT
    rele3.value     = state_r
    rele4           = DigitalInOut(board.D18)
    rele4.direction = Direction.OUTPUT
    rele4.value     = state_r
    print(state_r)
    state_r = not state_r
    time.sleep(1)
