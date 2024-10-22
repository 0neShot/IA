from pydualsense import pydualsense
import socket, logging
from config import Config
from time import sleep
import logging

connected = False
client_socket = 0

def initConnection():
    #Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    try:
        # Connect to the server
        client_socket.connect(('192.168.137.215', 80))
        logging.info("Connected to robot successfully")
        connected = True
    except socket.timeout:
            logging.warning("Failed to connect to robot")

def sendCommand(action, paramater = None):
    message = str(action)
    if paramater is not None:
        message += ";" + str(paramater)
    if not connected:
        logging.warning(f"Failed to send '{message}' because bot is not connected")
        return
    logging.info(f'Sending "{message}"')
    #client_socket.send(message.encode())

def joystickChanged(stateX, stateY):
    print(f"{stateX} X-Value")
    sendCommand(Config.SPEED, stateX)

def trianglePressed(state):
    print(f"Triangle: {state}")
    sendCommand(Config.STOPALL)
    
def r2Changed(state):
    print(f"R2: {state}")
    
def main():
    # Initialize the DualSense controller
    ds = pydualsense()
    ds.init()
    ds.light.setColorI(255,0,0) # set touchpad color to red
    
    # Initialize Connection
    initConnection()
    ds.light.setColorI(0,128,0) # set touchpad color to green
    
    # Set up event handlers for buttons
    ds.triangle_pressed += trianglePressed
    ds.left_joystick_changed += joystickChanged
    ds.r2_changed += r2Changed
    print(ds.state.LX)

    try:
        print("Press any button to see the output...")
        print(ds.state.LX)
        while True:
            pass  # Keep the script running to listen for events
    except KeyboardInterrupt:
        pass
    finally:
        ds.close()  # Close the controller connection

if __name__ == "__main__":
    main()
