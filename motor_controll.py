from machine import Pin, PWM
from config import Config
from time import sleep
import logging

# Initialize motor control pins
motor1_forward = Pin(Config.MOTOR_PINS[0], Pin.OUT)
motor1_backward = Pin(Config.MOTOR_PINS[1], Pin.OUT)
motor2_forward = Pin(Config.MOTOR_PINS[2], Pin.OUT)
motor2_backward = Pin(Config.MOTOR_PINS[3], Pin.OUT)

# Setup PWM for motors
pwm1 = PWM(Pin(Config.MOTOR_PINS[0]))
pwm2 = PWM(Pin(Config.MOTOR_PINS[2]))
pwm1.freq(Config.PWM_FREQUENCY)
pwm2.freq(Config.PWM_FREQUENCY)

def set_motor(motor, speed):
    """
    Controls motor speed and direction.

    Args:
        motor (str): Motor identifier ('motor1' or 'motor2').
        speed (int): Speed value (-255 to 255).
    """
    forward_pin = motor1_forward if motor == 'motor1' else motor2_forward
    backward_pin = motor1_backward if motor == 'motor1' else motor2_backward
    pwm = pwm1 if motor == 'motor1' else pwm2

    speed = max(-255, min(255, speed))

    if speed > 0:
        forward_pin.on()
        backward_pin.off()
        pwm.duty_u16(int((speed / 255) * 65535))
    elif speed < 0:
        forward_pin.off()
        backward_pin.on()
        pwm.duty_u16(int(((255 + speed) / 255) * 65535))
    else:
        forward_pin.off()
        backward_pin.off()
        pwm.duty_u16(0)

    logging.debug(f"Motor: {motor}, Speed: {speed}")

def stop_all():
    """Stops all motors."""
    motor1_forward.off()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.off()
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)
    logging.info("All motors stopped.")

def move(speed):
    """Moves both motors in the same direction."""
    logging.info(f"Moving at speed: {speed}")
    set_motor('motor1', speed)
    set_motor('motor2', speed)

def turn(direction, speed):
    """
    Turns the robot in the specified direction.

    Args:
        direction (str): 'left' or 'right'.
        speed (int): Speed value (0 to 255).
    """
    logging.info(f"Turning {direction} at speed: {speed}")
    if direction == 'left':
        set_motor('motor1', -speed)
        set_motor('motor2', speed)
    elif direction == 'right':
        set_motor('motor1', speed)
        set_motor('motor2', -speed)

def turn_angle(angle):
    """
    Rotates the robot by a specific angle.

    Args:
        angle (float): Angle to rotate (in degrees).
    """
    time_to_turn = abs(angle) / Config.DEGREES_PER_SECOND
    direction = 'left' if angle > 0 else 'right'
    logging.info(f"Turning {direction} for angle: {angle} degrees")
    turn(direction, Config.TURNSPEED)
    sleep(time_to_turn)
    stop_all()

def drive(angle, speed):
    """
    Adjusts motor speeds to drive at a specific angle.

    Args:
        angle (float): Steering angle (-128 to 128).
        speed (int): Base speed (0 to 255).
    """
    logging.info(f"Driving at angle: {angle}, speed: {speed}")
    if angle > 0:
        set_motor('motor1', speed)
        set_motor('motor2', int(speed * (1 - angle / 128)))
    else:
        set_motor('motor1', int(speed * (1 + angle / 128)))
        set_motor('motor2', speed)
