from time import sleep
from machine import Pin, ADC, Timer
from motor_controll import set_motor, stop_all

# PID-Koeffizienten
Kp = 1.0
Ki = 0.1
Kd = 0.05

# PID Variablen
previous_error = 0
integral = 0
integral_limit = 10
dt = 0.01

"Sensor"
groveled = Pin(18, Pin.OUT)
boardled = Pin(25, Pin.OUT)
adc = ADC(Pin(28))

timer = Timer()

def blink(timer):
    groveled.toggle()
    
timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

# Definiere eine Schwelle für die Erkennung von schwarz
threshold = 5000

lf = Pin(20, Pin.IN)

def getSensorValue():
    rawValue = adc.read_u16()
    if (rawValue < threshold):
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
    global Kp, Ki, Kd
    # Passen Sie die Koeffizienten basierend auf der Fehlerhistorie an
    Kp += adaptation_rate * abs(error)
    Ki += adaptation_rate * error
    Kd += adaptation_rate * (error - previous_error)

def pid_controller(setpoint, sensor_value):
    global previous_error, integral

    # Fehlerberechnung
    error = setpoint - sensor_value

    # Proportionaler Anteil
    P = Kp * error

    # Integral Anteil mit Anti-Windup
    integral += error * dt
    integral = max(min(integral, integral_limit), -integral_limit)
    I = Ki * integral

    # Differentialer Anteil
    derivative = (error - previous_error) / dt
    D = Kd * derivative

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
    
