from time import sleep
from machine import Pin, ADC, Timer
from motor_controll import set_motor, stop_all
from config import Config

# PID Variablen
previous_error = 0
integral = 0
integral_limit = 10
dt = 0.01

"Sensor"
boardled = Pin(Config.ONBORDLEDPIN, Pin.OUT)
adc = ADC(Pin(Config.ANALOGSENSORPIN))

def getSensorValue():
    rawValue = adc.read_u16()
    if (rawValue < Config.TRESHOLD):
        boardled.on()
    else:
        boardled.off()
    print(rawValue)
    sleep(0.1)
    return rawValue

def isBlackDetected(threshold):
    sensor_value = getSensorValue()
    return sensor_value >= threshold
    
# Anpassungsrate der PID-Koeffizienten
adaptation_rate = 0.01

def adapt_pid_coefficients(error):
    # Passen Sie die Koeffizienten basierend auf der Fehlerhistorie an
    Config.KP += adaptation_rate * abs(error)
    Config.KI += adaptation_rate * error
    Config.KD += adaptation_rate * (error - previous_error)

def pid_controller(setpoint, sensor_value):
    global previous_error, integral

    # Fehlerberechnung
    error = setpoint - sensor_value

    # Proportionaler Anteil
    P = Config.KP * error

    # Integral Anteil mit Anti-Windup
    integral += error * dt
    integral = max(min(integral, integral_limit), -integral_limit)
    I = Config.KI * integral

    # Differentialer Anteil
    derivative = (error - previous_error) / dt
    D = Config.KD * derivative

    # Regelgröße berechnen
    output = P + I + D

    # PID-Koeffizienten anpassen
    adapt_pid_coefficients(error)

    # Update für den nächsten Durchlauf
    previous_error = error

    return output

def steerMotorsPID(correction):
    base_speed = 0.5
    left_speed = base_speed - correction
    right_speed = base_speed + correction

    left_speed = max(min(left_speed, 1), -1)
    right_speed = max(min(right_speed, 1), -1)

    set_motor('motor1', left_speed * 100)
    set_motor('motor2', right_speed * 100)
