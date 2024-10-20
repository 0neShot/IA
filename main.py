# main.py
import time
from motor_controll import set_motor, stop_all
from PID import pid_controller, getSensorValue, isBlackDetected
import socket
import network

threshold = 5000

ds = pydualsense()
ds.init()

def steerMotorsPID(correction):
    base_speed = 0.2
    left_speed = base_speed - correction
    right_speed = base_speed + correction

    # Begrenzen der Geschwindigkeit auf -1 bis 1
    left_speed = max(min(left_speed, 1), -1)
    right_speed = max(min(right_speed, 1), -1)

    # Setze die Motoren mit den übergebenen Geschwindigkeiten
    set_motor('motor1', left_speed * 20 )  # Prozentwert für die Geschwindigkeit
    set_motor('motor2', right_speed * 20)

def mainDrive():
    # Hauptschleife
    while True:
        sensor_value = getSensorValue()
        print(sensor_value)
        setpoint = 1
        
        
        if isBlackDetected(threshold):
            setpoint = 1  # Sollwert ist die Linie
        else:
            setpoint = 0  # Keine Linie erkannt
        # PID-Controller
        correction = pid_controller(setpoint, sensor_value)

        # Fahrzeug steuern
        steerMotorsPID(correction)

        time.sleep(0.05)

try:
    mainDrive()
except KeyboardInterrupt:
    stop_all()
finally:
    ds.close()  # Close the controller connection

