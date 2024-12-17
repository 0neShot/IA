import socket, logging
from time import sleep

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.connected = False
        try:
            self.socket.connect((host, port))
            logging.info("Connected to robot successfully")
            self.connected = True
        except socket.timeout:
            logging.warning("Failed to connect to robot")
        
    def sendCommand(self, action, *parameters):
        message = str(action)
        if parameters is not None:
            message += ";" + ";".join(str(param) for param in parameters) + '!'
        if not self.connected:
            logging.warning(f"Failed to send '{message}' because bot is not connected")
            return
        logging.info(f'Sending "{message}"')
        self.socket.send(message.encode())
        sleep(0.01)
