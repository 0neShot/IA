from pydualsense import *
from client import Client
from config import Config
from time import sleep

class Dualsense(pydualsense):
    controller_input = False
    
    def __init__(self, client, gui):
        super().__init__()
        self.client = client
        self.gui = gui
        self.init()
        self.light.setColorI(255,0,0) # set touchpad color to red
        if (client.connected):
            self.light.setColorI(0,128,0) # set touchpad color to green
            self.setRightMotor(100) # Vibrate 
            sleep(1)
            self.setRightMotor(0)
            Dualsense.controller_input = True # Enable Controller input so Values are send to client
        else:
            Dualsense.controller_input = False
            
        self.triangle_pressed += self.trianglePressed
        self.left_joystick_changed += self.joystickChanged
        self.r2_changed += self.r2Changed
        self.circle_pressed += self.circlePressed

    def joystickChanged(self, stateX, stateY):
        """Callback für das Verschieben des Joysticks"""
        if (self.controller_input):
            if (self.state.L2 > 10):
                self.client.sendCommand(Config.DRIVE, stateX, -1 * self.state.R2)
            else:
                self.client.sendCommand(Config.DRIVE, stateX, self.state.R2)

    def trianglePressed(self, state):
        """Callback für das Drücken der 'Triangle'-Taste"""
        if (self.controller_input):
            self.client.sendCommand(Config.STOPALL)
            self.controller_input = False
            self.gui.controller_input_clicked()
        
    def r2Changed(self, state):
        """Callback für das Ändern des R2-Triggers"""
        if (self.controller_input):
            if (self.state.L2 > 10):
                self.client.sendCommand(Config.DRIVE, self.state.LX, -1 * state)
            else:
                self.client.sendCommand(Config.DRIVE, self.state.LX, state)
    
    def circlePressed(self, state):
        if (self.controller_input):
            self.client.sendCommand(Config.STARTPID)
