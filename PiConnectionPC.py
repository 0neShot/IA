import socket
import network
from time import sleep
from machine import Pin
from config import Config

led_onboard = Pin("LED", Pin.OUT)

def initPiConnection():
    ip = connect()
    connection = open_socket(ip)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(Config.SSID)
    print(Config.PASSWORD)
    wlan.connect(Config.SSID, Config.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led_onboard.on()
    return ip
 
def open_socket(ip):
    address = (ip,80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    #print(connection)
    return connection
 
try:
    initPiConnection()
    while True:
        # Accept a connection from a client
        client, addr = connection.accept()
        print(f'Connected to {addr}')
        while True:
            # Receive data from the client
            data = client.recv(1024)
            if data:
                # Print the data to the console
                print(data)
                    
except KeyboardInterrupt:
    # Close the server socket
    connection.close()
