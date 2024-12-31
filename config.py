class Config:
    "Constants for Communication. Do not change!"
    DRIVE = 1
    STOPALL = 2
    STARTPID = 3

    "Definitions for Robot"
    TRESHOLD = 5000 # Threshold for analog light sensor
    ANALOGSENSOR_PIN = 28
    ONBORDLED_PIN = 25
    IR_SENSOR_PINS = [19,18,17,16,15] # Pins from left to right on IR-Array

    "Motor Definitions"
    PWM_FREQUENCY = 40
    TURNSPEED = 10 # % of maximum turn speed
    DEGREES_PER_SECOND = 90 # Supposed turn angle per second in degrees
    MOTOR_PINS = [13,12,11,10] # Motor_1_forwad, Motor_1_backward, Motor_2_forwad, Motor_2_backward

    "Constants for PID"
    KP = 0.45
    KI = 0.2
    KD = 0.01
    MAX_SPEED = 70 # % of maximum speed (0-100)

    "Wifi Connection Settings"
    SSID = 'CHRISTOPHER 9603'
    PASSWORD = '2s65Y88+'

    def set_variable(self, variable, new_value):
        if hasattr(self, variable):  # Check if variable exists
            setattr(self, variable, new_value)
            print(f"{variable} changed to: {new_value}")
        else:
            print(f"Variable {variable} doesnt exist.")
