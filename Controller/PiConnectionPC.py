import socket
import network
from time import sleep
from machine import Pin
from config import Config
from motor_controll import *
from PID import PIDController

class PiConnection:
    def __init__(self):
        self.led_onboard = Pin("LED", Pin.OUT)
        self.connection = None
        self.wlan = network.WLAN(network.STA_IF)
        self.client = None
        self.is_connected = False

    def init_connection(self):
        ip = self.connect()
        self.connection = self.open_socket(ip)

    def connect(self):
        # WLAN-Verbindung herstellen
        self.wlan.active(True)
        print(Config.SSID)
        print(Config.PASSWORD)
        self.wlan.connect(Config.SSID, Config.PASSWORD)
        
        while not self.wlan.isconnected():
            print('Waiting for connection...')
            sleep(3)
        
        ip = self.wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        self.led_onboard.on()
        return ip

    def open_socket(self, ip):
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        return connection

    @staticmethod
    def parse_message(message):
        # Nachricht in Aktion und Parameter aufteilen
        print(f"Parsing message: {message}")
        parts = message.split(";")
        try:
            # Überprüfen, ob die Nachricht überhaupt eine Aktion enthält
            if not parts or len(parts[0].strip()) == 0:
                print("Fehler: Die Nachricht enthält keine gültige Aktion.")
                return None, []  # Rückgabe von None für die Aktion und einer leeren Liste

            action = int(parts[0])  # Umwandlung des ersten Teils in einen Integer

            # Überprüfen, ob weitere Parameter vorhanden sind
            if len(parts) > 1:
                numbers = []
                for num in parts[1:]:
                    num = num.strip()
                    if num.isdigit() or (num.startswith("-") and num[1:].isdigit()):  # Negative Zahlen abfangen
                        numbers.append(int(num))
                    else:
                        print(f"Warnung: Ungültiger Parameter '{num}' in Nachricht: {message}")
                return action, numbers
            else:
                print("Hinweis: Keine zusätzlichen Parameter in Nachricht.")
                return action, []
        except ValueError as e:
            print(f"ValueError beim Parsen der Nachricht: {e} für Daten: {message}")
            return None, []
    
    def start_listening(self):
        try:
            self.init_connection()
            while True:
                # Warten auf eine Client-Verbindung
                client, addr = self.connection.accept()
                print(f'Connected to {addr}')
                self.handle_client(client, addr)
        except KeyboardInterrupt:
            print("Program interrupted. Closing connections...")
        finally:
            self.close_connection()

    def handle_client(self, client, addr):
        self.is_connected = True
        self.client = client
        buffer = ""  # Puffer zum Speichern empfangener Daten
        try:
            while True:
                data = client.recv(15)  # Setze die empfangene Länge auf 15 Bytes
                if not data:
                    print(f' >> {addr} disconnected')
                    stop_all()  # Stoppe den Roboter, wenn die Verbindung getrennt wird
                    self.is_connected = False
                    break
                else:
                    buffer += data.decode()  # Füge die empfangenen Daten zum Puffer hinzu
                    while "!" in buffer:  # Überprüfe, ob im Puffer vollständige Nachrichten sind
                        message, buffer = self.extract_message(buffer)  # Extrahiere die Nachricht
                        if message:  # Überprüfen, ob die Nachricht nicht leer ist
                            try:
                                action, numbers = self.parse_message(message)
                                self.execute_action(action, numbers)
                            except ValueError as e:
                                print(f"ValueError: {e} for data: {message}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")
        except OSError as e:  # Erfassung allgemeiner Socket-Fehler
            print(f"Connection error with {addr}: {e}")
            stop_all()  # Stoppe den Roboter, wenn ein Verbindungsfehler auftritt
        finally:
            client.close()  # Schließe den Client-Socket
            
    def extract_message(self, buffer):
        # Teile den Puffer an der ersten Stelle, an der ein Ausrufezeichen gefunden wird
        parts = buffer.split("!")
        if len(parts) > 1:
            # Nachricht bis zum letzten "!" als vollständige Nachricht betrachten
            message = parts[0]  # Nimm das erste Segment als Nachricht
            remaining = "!".join(parts[1:])  # Rest bleibt im Puffer
            print(f"Extrahierte Nachricht: {message} mit verbleibendem Puffer: {remaining}")
        else:
            message = ""
            remaining = buffer  # Kein "!" im Buffer, nichts extrahieren
            print(f"Unvollständige Nachricht: nur Puffer '{buffer}'")

        return message, remaining

    
    def execute_action(self, action, numbers):
        if action == Config.DRIVE:
            drive(numbers[0], numbers[1])
        elif action == Config.STOPALL:
            stop_all()
            print("Stopping all motors...")
        elif action == Config.STARTPID:
            pid = PIDController(self.is_connected)
            print("Starting PID...")
            pid.run(0) # Run PID-Algo with Setpoint 0 (Black line in the middle)

    def close_connection(self):
        if self.connection:
            self.connection.close()
        if self.wlan.isconnected():
            self.wlan.disconnect()
        print("Connection closed.")
        self.led_onboard.off()

