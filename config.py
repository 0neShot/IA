import logging

class Config:
    """
    Configuration class for robot constants and settings.
    Update these values to suit your hardware and preferences.
    """

    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Commands
    DRIVE = 1
    STOPALL = 2
    STARTPID = 3

    # Robot Settings
    TRESHOLD = 5000  # Threshold for analog light sensor
    ANALOGSENSOR_PIN = 28
    ONBORDLED_PIN = 25
    IR_SENSOR_PINS = [19, 18, 17, 16, 15]  # Pins from left to right on IR-Array

    # Motor Settings
    PWM_FREQUENCY = 40
    TURNSPEED = 10  # % of maximum turn speed
    DEGREES_PER_SECOND = 90  # Supposed turn angle per second in degrees
    MOTOR_PINS = [13, 12, 11, 10]  # Motor_1_forward, Motor_1_backward, Motor_2_forward, Motor_2_backward

    # PID Settings
    KP = 0.45
    KI = 0.2
    KD = 0.01
    MAX_SPEED = 70  # % of maximum speed (0-100)

    # Network Settings
    SSID = 'CHRISTOPHER 9603'
    PASSWORD = '2s65Y88+'

    @staticmethod
    def set_variable(variable, new_value):
        """Updates configuration variables dynamically."""
        if hasattr(Config, variable):
            setattr(Config, variable, new_value)
            print(f"{variable} changed to: {new_value}")
        else:
            print(f"Variable {variable} does not exist.")
