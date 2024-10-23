import socket
import network
from time import sleep
from machine import Pin
from config import Config
from motor_controll import *

led_onboard = Pin("LED", Pin.OUT)
connection = None

def initPiConnection():
    global connection
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

def parseMessage(message):
    # Nachricht nach Semikolon trennen
    print(message)
    parts = message.split(";")
    # Die erste Zahl bestimmt die Aktion
    action = int(parts[0])
    # Die restlichen Teile in eine Liste von Ganzzahlen umwandeln
    numbers = [int(num) for num in parts[1:]]
    # Rückgabe von Aktion und Zahlenliste
    return action, numbers

try:
    initPiConnection()
    while True:
        # Accept a connection from a client
        client, addr = connection.accept()
        print(f'Connected to {addr}')
        while True:
            # Receive data from the client
            data = client.recv(50)
            if not data:
                print(f' >> {addr} disconnected')
                stop_all()
                break
            else:
                try:
                    # Print the data to the console
                    action, numbers = parseMessage(data.decode().strip())
                    if (action == Config.DRIVE):
                        drive(numbers[0], numbers[1])
                    if (action == Config.STOPALL):
                        stop_all()
                except ValueError as e:
                    print(f"ValueError: {e} for data: {data.decode()}")  # Debugging line
                except Exception as e:
                    print(f"Unexpected error: {e}")  # Catch any other errors    
                    
except KeyboardInterrupt:
    # Close the server socket
    print("Program interrupted. Closing connections...")
finally:
    # Ensure the server socket is closed and WLAN is disconnected
    if connection:
        connection.close()
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()  # Disconnect from WLAN
    print("Connection closed.")