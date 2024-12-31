# main.py
from piConnectionPC import PiConnection
from time import sleep

def mainDrive():
    pi = PiConnection() 
    pi.start_listening() # Start listening for events

if rp2.bootsel_button() == 1:
    try:
        mainDrive()
    except KeyboardInterrupt:
       pass




