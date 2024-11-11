from machine import Pin, PWM
from time import sleep
from config import Config


motor1_forward = Pin(Config.MOTOR_PINS[1], Pin.OUT)
motor1_backward = Pin(Config.MOTOR_PINS[0], Pin.OUT)
motor2_forward = Pin(Config.MOTOR_PINS[3], Pin.OUT)
motor2_backward = Pin(Config.MOTOR_PINS[2], Pin.OUT)

# PWM für die Motoren festlegen
pwm1 = PWM(Config.MOTOR_PINS[1])
pwm2 = PWM(Config.MOTOR_PINS[3])

# PWM-Frequenz setzen
pwm1.freq(Config.PWM_FREQUENCY)
pwm2.freq(Config.PWM_FREQUENCY)

def set_motor(motor, speed):
    """
    Steuert die Motoren für Vorwärts- und Rückwärtsbewegungen.
    
    :param motor: "motor1" oder "motor2"
    :param speed: Geschwindigkeit (0 bis 100)
    """
    
    forward_pin = motor1_forward if motor == 'motor1' else motor2_forward
    backward_pin = motor1_backward if motor == 'motor1' else motor2_backward
    # Begrenze die Geschwindigkeit auf einen Bereich von -100 bis 100
    speed = max(-255, min(255, speed))

    if speed > 0:
        # Vorwärtslauf
        forward_pin.on()
        backward_pin.off()
        duty_cycle = int((speed / 255) * 65535)
    elif speed < 0:
        # Rückwärtslauf
        forward_pin.off()
        backward_pin.on()
        duty_cycle = int(((255 + speed) / 255) * 65535)
    else:
        # Stoppe den Motor
        forward_pin.off()
        backward_pin.off()
        pwm1.duty_u16(0) if motor == 'motor1' else pwm2.duty_u16(0)
        return
    
    print(f"Motor: {motor}, Speed: {speed}, Duty Cycle: {duty_cycle}")
    if motor == 'motor1':
        pwm1.duty_u16(duty_cycle)
    elif motor == 'motor2':
        pwm2.duty_u16(duty_cycle)

def stop_all():
    """Stoppt beide Motoren."""
    motor1_forward.off()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.off()
    
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)

def move(speed):
    """Bewegt beide Motoren in eine Richtung."""
    set_motor('motor1', speed)
    set_motor('motor2', speed)
    
def turn(direction, speed):
    """
    Dreht den Roboter.
    :param direction: "left" oder "right"
    :param speed: Geschwindigkeit (0 bis 100)
    """
    if direction == 'left':
        set_motor('motor1', -speed)  # Motor 1 vorwärts
        set_motor('motor2', speed)    # Motor 2 rückwärts
    elif direction == 'right':
        set_motor('motor1', speed)     # Motor 1 rückwärts
        set_motor('motor2', -speed)    # Motor 2 vorwärts

def turn_angle(angle):
    """
    Dreht den Roboter um einen bestimmten Winkel.
    :param angle: Der Winkel, um den der Roboter gedreht werden soll (in Grad).
    """
    # Berechne die Zeit, die benötigt wird, um den gewünschten Winkel zu drehen
    time_to_turn = abs(angle) / Config.DEGREESPERSECOND
    
    if angle > 0:
        turn('left', Config.TURNSPEED)  # Drehung nach links
    else:
        turn('right', Config.TURNSPEED)  # Drehung nach rechts
    
    sleep(time_to_turn)  # Warte die erforderliche Zeit
    stop_all()  # Stoppe die Motoren nach dem Drehen
    
def drive(angle, speed):
    if (angle > 0):
         set_motor('motor1', speed)
         set_motor('motor2', speed * (1 - angle / 128))
    else:
         set_motor('motor1', speed * (1 + angle / 128))
         set_motor('motor2', speed)


