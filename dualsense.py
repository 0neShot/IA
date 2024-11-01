from pydualsense import *
from client import Client
from config import Config

class Dualsense(pydualsense):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init()
        self.light.setColorI(255,0,0) # set touchpad color to red
        if (client.connected):
            self.light.setColorI(0,128,0) # set touchpad color to green
            self.setRightMotor(100) # Vibrate 
            sleep(1)
            self.setRightMotor(0)
        self.triangle_pressed += self.trianglePressed
        self.left_joystick_changed += self.joystickChanged
        self.r2_changed += self.r2Changed

    def joystickChanged(self, stateX, stateY):
        """Callback für das Verschieben des Joysticks"""
        self.client.sendCommand(Config.DRIVE, stateX, self.state.R2)

    def trianglePressed(self, state):
        """Callback für das Drücken der 'Triangle'-Taste"""
        self.client.sendCommand(Config.STOPALL)
        
    def r2Changed(self, state):
        """Callback für das Ändern des R2-Triggers"""
        self.client.sendCommand(Config.DRIVE, self.state.LX, state)
