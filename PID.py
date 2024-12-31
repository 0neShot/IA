from time import sleep
from motor_controll import set_motor, stop_all
from config import Config
import logging

class PIDController:
    """
    Implements a PID controller for line tracking.
    """

    def __init__(self, is_connected):
        """
        Initializes the PID controller with sensor settings and initial values.

        Args:
            is_connected (bool): Connection status to the client.
        """
        self.previous_error = 0
        self.integral = 0
        self.is_connected = is_connected
        self.dt = 0.01
        self.integral_limit = 10
        logging.info("PIDController initialized.")

    def calculate_pid(self, setpoint, current_value):
        """
        Calculates PID correction.

        Args:
            setpoint (float): Desired target value.
            current_value (float): Current measured value.

        Returns:
            float: PID output for correction.
        """
        error = setpoint - current_value

        # Proportional
        p_term = Config.KP * error

        # Integral
        self.integral += error * self.dt
        self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)
        i_term = Config.KI * self.integral

        # Derivative
        d_term = Config.KD * (error - self.previous_error) / self.dt
        self.previous_error = error

        correction = p_term + i_term + d_term
        logging.debug(f"PID calculation: P={p_term}, I={i_term}, D={d_term}, Correction={correction}")
        return correction

    def execute(self, setpoint, current_value):
        """
        Executes PID control to adjust motor speeds.

        Args:
            setpoint (float): Target value.
            current_value (float): Current value from sensors.
        """
        correction = self.calculate_pid(setpoint, current_value)
        base_speed = Config.MAX_SPEED

        left_speed = base_speed - correction
        right_speed = base_speed + correction

        set_motor('motor1', left_speed)
        set_motor('motor2', right_speed)
        logging.info(f"Executing PID control: Left Speed={left_speed}, Right Speed={right_speed}")

    def stop_if_disconnected(self):
        """
        Stops motors if the client is disconnected.

        Returns:
            bool: True if stopped, False otherwise.
        """
        if not self.is_connected:
            stop_all()
            logging.warning("Client disconnected. Motors stopped.")
            return True
        return False
