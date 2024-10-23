from pydualsense import pydualsense
import socket, logging
from config import Config
from time import sleep
import logging

connected = False
client_socket = None
ds = None 

def initConnection():
    global connected, client_socket
    #Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    try:
        # Connect to the server
        client_socket.connect(('192.168.137.161', 80))
        logging.info("Connected to robot successfully")
        connected = True
    except socket.timeout:
            logging.warning("Failed to connect to robot")

def sendCommand(action, *parameters):
    global connected, client_socket
    message = str(action)
    if parameters is not None:
        message += ";" + ";".join(str(param) for param in parameters) + '\n'
    if not connected:
        logging.warning(f"Failed to send '{message}' because bot is not connected")
        return
    logging.info(f'Sending "{message}"')
    client_socket.send(message.encode())
    sleep(0.1)

def joystickChanged(stateX, stateY):
    global ds
    sendCommand(Config.DRIVE, stateX, ds.state.R2)

def trianglePressed(state):
    sendCommand(Config.STOPALL)
    
def r2Changed(state):
    global ds
    sendCommand(Config.DRIVE, ds.state.LX, state)
    
def main():
    global ds
    # Initialize the DualSense controller
    ds = pydualsense()
    ds.init()
    ds.light.setColorI(255,0,0) # set touchpad color to red
    
    # Initialize Connection
    initConnection()
    if (connected):
        ds.light.setColorI(0,128,0) # set touchpad color to green
        ds.setRightMotor(100)
        sleep(1)
        ds.setRightMotor(0)
    
    # Set up event handlers for buttons
    ds.triangle_pressed += trianglePressed
    ds.left_joystick_changed += joystickChanged
    ds.r2_changed += r2Changed

    try:
        print("Press any button to see the output...")
        while True:
            pass  # Keep the script running to listen for events
    except KeyboardInterrupt:
        pass
    finally:
        ds.close()  # Close the controller connection

if __name__ == "__main__":
    main()
