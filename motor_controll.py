from machine import Pin, PWM
from time import sleep

# Motorsteuerungspins definieren
motor_pins = {
    'motor1_forward': Pin(13, Pin.OUT),
    'motor1_backward': Pin(12, Pin.OUT),
    'motor2_forward': Pin(11, Pin.OUT),
    'motor2_backward': Pin(10, Pin.OUT)
}

# PWM für die Motoren festlegen
pwm1 = PWM(Pin(13))
pwm2 = PWM(Pin(11))

# PWM-Frequenz auf 48Hz setzen
pwm1.freq(40)
pwm2.freq(40)

# Konstante für die Drehgeschwindigkeit
TURN_SPEED = 20  # % der maximalen Geschwindigkeit
DEGREES_PER_SECOND = 90  # Annahme: 90 Grad pro Sekunde Drehgeschwindigkeit

def set_motor(motor, speed):
    """
    Steuert die Motoren für Vorwärts- und Rückwärtsbewegungen.
    
    :param motor: "motor1" oder "motor2"
    :param speed: Geschwindigkeit (0 bis 100)
    """
    
    forward_pin = motor_pins[f'{motor}_forward']
    backward_pin = motor_pins[f'{motor}_backward']
    
    # Begrenze die Geschwindigkeit auf einen Bereich von -100 bis 100
    speed = max(-100, min(100, speed))

    forward_pin = motor_pins[f'{motor}_forward']
    backward_pin = motor_pins[f'{motor}_backward']

    if speed > 0:
        # Vorwärtslauf
        forward_pin.on()
        backward_pin.off()
    elif speed < 0:
        # Rückwärtslauf
        forward_pin.off()
        backward_pin.on()
    else:
        # Stoppe den Motor
        forward_pin.off()
        backward_pin.off()
        pwm1.duty_u16(0) if motor == 'motor1' else pwm2.duty_u16(0)
        return
    
     # Berechne das Duty-Cycle-Verhältnis (0 bis 65535 für 100% PWM)
    duty_cycle = int((speed / 100) * 65535)
    
   # Wähle das richtige PWM-Objekt für den Motor
    if motor == 'motor1':
        pwm1.duty_u16(duty_cycle)
    elif motor == 'motor2':
        pwm2.duty_u16(duty_cycle)

def stop_all():
    """Stoppt beide Motoren."""
    for pin in motor_pins.values():
        pin.off()
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)

def move(direction, speed):
    """Bewegt beide Motoren in eine Richtung."""
    set_motor('motor1', direction, speed)
    set_motor('motor2', direction, speed)
    
def turn(direction, speed):
    """
    Dreht den Roboter.
    
    :param direction: "left" oder "right"
    :param speed: Geschwindigkeit (0 bis 100)
    """
    if direction == 'left':
        set_motor('motor1', 'forward', speed)
        set_motor('motor2', 'backward', speed)
    elif direction == 'right':
        set_motor('motor1', 'backward', speed)
        set_motor('motor2', 'forward', speed)

def turn_angle(angle):
    """
    Dreht den Roboter um einen bestimmten Winkel.
    
    :param angle: Der Winkel, um den der Roboter gedreht werden soll (in Grad).
    """
    # Berechne die Zeit, die benötigt wird, um den gewünschten Winkel zu drehen
    time_to_turn = abs(angle) / DEGREES_PER_SECOND
    
    if angle > 0:
        turn('left', TURN_SPEED)  # Drehung nach links
    else:
        turn('right', TURN_SPEED)  # Drehung nach rechts
    
    sleep(time_to_turn)  # Warte die erforderliche Zeit
    stop_all()  # Stoppe die Motoren nach dem Drehen

