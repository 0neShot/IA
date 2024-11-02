from machine import Pin
from motor_controll import set_motor, stop_all
from config import Config

class PIDController:
    def __init__(self, is_connected):
        # Initialisiere 5 digitale IR-Sensoren auf festgelegten Pins
        self.sensor_pins = [Pin(pin, Pin.IN) for pin in Config.IR_SENSOR_PINS]
        self.board_led = Pin(Config.ONBORDLED_PIN, Pin.OUT)

        # PID Variablen
        self.previous_error = 0
        self.integral = 0
        self.integral_limit = 10
        self.dt = 0.01
        self.is_connected = is_connected

    def get_sensor_values(self):
        """Liest die Werte aller digitalen IR-Sensoren aus."""
        return [sensor.value() for sensor in self.sensor_pins]

    def calculate_position(self):
        """
        Berechnet die Position der Linie basierend auf den aktiven Sensoren.
        Gibt einen Wert zurück, der angibt, wie weit der Roboter von der Linie entfernt ist.
        """
        sensor_values = self.get_sensor_values()
        
        # Gewichte für die Position jedes Sensors im Array
        weights = [-2, -1, 0, 1, 2]
        
        # Berechne die gewichtete Summe basierend auf aktiven Sensoren
        weighted_sum = sum(w * v for w, v in zip(weights, sensor_values))
        
        # Zähle die aktiven Sensoren
        active_sensors = sum(sensor_values)

        # Berechne die mittlere Position der Linie
        if active_sensors == 0:
            return 0  # Standardwert, wenn keine Linie erkannt wird
        else:
            return weighted_sum / active_sensors

    def pid_control(self, setpoint, sensor_position):
        """Führt die PID-Regelung basierend auf der Abweichung von der Linie durch."""
        error = setpoint - sensor_position

        # Berechne die Regelanteile
        P = Config.KP * error

        self.integral += error * self.dt
        self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)
        I = Config.KI * self.integral

        derivative = (error - self.previous_error) / self.dt
        D = Config.KD * derivative

        # Gesamtausgabe berechnen
        output = P + I + D

        # Speichere den aktuellen Fehler für den nächsten Zyklus
        self.previous_error = error

        return output

    def steer_motors_pid(self, correction):
        """Steuert die Motoren basierend auf der PID-Korrektur."""
        base_speed = Config.MAX_SPEED * 0.01
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        left_speed = max(min(left_speed, 1), -1)
        right_speed = max(min(right_speed, 1), -1)

        set_motor('motor1', left_speed * 100)
        set_motor('motor2', right_speed * 100)

    def check_stop_condition(self):
        """Überprüft, ob der STOP_ALL-Befehl gesendet wurde oder die Client-Verbindung verloren ist."""
        if not self.connection.is_connected:
            stop_all()
            print("client disconnected. Motors stopped.")
            return True  # Stop condition met
        return False  # No stop condition

    def run(self, setpoint):
        """Führt die Hauptregelungsschleife durch."""
        while True:
            # Überprüfen, ob der STOP_ALL-Befehl gesendet wurde oder Verbindung verloren ist
            if self.is_connected:
                break  # Beende die Schleife, wenn eine Stopp-Bedingung erfüllt ist

            # Position basierend auf Sensor-Array berechnen
            sensor_position = self.calculate_position()
            correction = self.pid_control(setpoint, sensor_position)

            # Motoren steuern
            self.steer_motors_pid(correction)

