class Config:
    "Constants for Communication. Do not change!"
    DRIVE = 1
    STOPALL = 2
    STARTPID = 3
    
    "Definitions for Robot"
    TRESHOLD = 5000 #Threshold for analog light sensor
    ANALOGSENSORPIN = 28
    ONBORDLEDPIN = 25
    IRSENSOR1 = 19 #Pins declared from left to right
    IRSENSOR2 = 18
    IRSENSOR3 = 17
    IRSENSOR4 = 16
    IRSENSOR5 = 15
    
    "Motor Definitions"
    PWMFREQUENCY = 40
    TURNSPEED = 20 #% of maximum turn speed
    DEGREES_PER_SECOND = 90 # Supposed turn angle per second in degrees
    
    "Constants for PID"
    KP = 1.0
    KI = 0.1
    KD = 0.05
    
    "Wifi Connection Settings"
    SSID = 'DESKTOP-12QN0M'
    PASSWORD = '6d]9129K'
