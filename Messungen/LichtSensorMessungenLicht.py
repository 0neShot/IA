import machine
import utime
import uos
import sys
import select

# ADC-Pin für den Lichtsensor (Pin 28 entspricht ADC2)
light_sensor = machine.ADC(28)

# Globale Variablen
filename = "lightsensor_average_data_L4_2.csv"  # CSV-Dateiname
paused = False  # Status für Pause

# Funktion zum Berechnen des Mittelwerts
def calculate_average(values):
    return sum(values) / len(values)

# Funktion zum Erstellen und Schreiben in die CSV-Datei
def save_to_csv(mean_value, measurement_number):
    try:
        # Überprüfen, ob die Datei existiert
        mode = "a" if filename in uos.listdir() else "w"
        with open(filename, mode) as f:
            # Kopfzeile nur beim ersten Erstellen hinzufügen
            if mode == "w":
                f.write("Durchlauf,Mittelwert\n")
            # Daten hinzufügen
            f.write(f"{measurement_number},{mean_value}\n")
        print(f"Mittelwert gespeichert: {mean_value} (Durchlauf {measurement_number})")
    except Exception as e:
        print("Fehler beim Schreiben der CSV-Datei:", e)

# Funktion, um Benutzereingaben zu überprüfen
def check_input():
    global paused
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:  # Prüfen, ob Eingabe vorliegt
        char = sys.stdin.read(1).lower()  # Eingabe auslesen und in Kleinbuchstaben umwandeln
        if char == "p":
            paused = True
            print("Messung pausiert. Drücken Sie Enter, um fortzufahren.")
        elif char == "\n" and paused:
            paused = False
            print("Messung wird fortgesetzt...")
        elif char == "q":
            print("Programm wird beendet...")
            sys.exit()

# Hauptfunktion
def main():
    global paused
    print("Starte Messungen... Drücken Sie P, um zu pausieren, Enter, um fortzufahren, und Q, um das Programm zu beenden.")
    measurement_number = 1  # Nummer der Mittelwert-Serien
    total_series = 5  # Maximale Anzahl an Serien (Abbruchbedingung)

    while measurement_number <= total_series:  # Abbruch nach 5 Serien
        data = []  # Liste für die 10 Messwerte

        # 10 Messungen durchführen
        print(f"Durchlauf {measurement_number}: Starte Messung...")
        for i in range(10):
            # Pause überprüfen
            while paused:
                check_input()  # Eingabe prüfen, ob Benutzer "Enter" drückt, um fortzufahren
                utime.sleep(0.1)  # Kurze Pause zur Prozessschonung

            check_input()  # Benutzeraktionen (P, Q) prüfen
            value = light_sensor.read_u16()  # 16-Bit-ADC-Wert auslesen
            data.append(value)
            print(f"Messung {i + 1}: {value}")
            utime.sleep(1)  # 1 Sekunde Pause zwischen den Messungen

        # Mittelwert berechnen
        mean_value = calculate_average(data)
        print(f"Durchschnittswert (Mittelwert) der 10 Messungen: {mean_value}")

        # Mittelwert in CSV-Datei speichern
        save_to_csv(mean_value, measurement_number)

        # Durchlaufzähler erhöhen
        measurement_number += 1

        # Pause zwischen den Serien, wenn noch Serien übrig sind
        if measurement_number <= total_series:
            print("Pause für 5 Sekunden...")
            for _ in range(50):  # Pause in kleinen Schritten, um Eingabe prüfen zu können
                check_input()  # Benutzeraktionen (P, Q) prüfen
                utime.sleep(0.1)

    # Nach der letzten Serie:
    print("Maximale Anzahl an Serien erreicht (5 Serien abgeschlossen). Programm wird beendet.")

# Hauptprogramm starten
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramm manuell beendet. CSV-Datei wurde aktualisiert.")
