from motor_controll import stop_all
from PID import PIDController

def main():
    pid_controller = PIDController(is_connected=False)

    setpoint = 0  # Mittige Position (Anpassbar je nach Line-Tracking-Konfiguration)

    # PID-Regelschleife ausführen
    if rp2.bootsel_button() == 1:
        try:
            print("Running pid")
            pid_controller.run(setpoint)
        except KeyboardInterrupt:
            print("Program manually stopped.")
        finally:
            stop_all()  # Stellt sicher, dass die Motoren am Ende gestoppt werden

if __name__ == "__main__":
    main()
