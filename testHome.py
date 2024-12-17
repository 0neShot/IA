import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# I2C-Schnittstelle initialisieren
i2c = busio.I2C(board.GP1, board.GP0)  # SCL auf GP1, SDA auf GP0

# ADS1115-Instanz erstellen
adc = ADS1115(i2c)

# Kanäle einrichten
chan0 = AnalogIn(adc, ADS1115.P0)
chan1 = AnalogIn(adc, ADS1115.P1)
chan2 = AnalogIn(adc, ADS1115.P2)
chan3 = AnalogIn(adc, ADS1115.P3)

print("Reading ADS1115 values...")

while True:
    print(f"Channel 0: {chan0.voltage:.2f} V")
    print(f"Channel 1: {chan1.voltage:.2f} V")
    print(f"Channel 2: {chan2.voltage:.2f} V")
    print(f"Channel 3: {chan3.voltage:.2f} V")
    print("---------------")
    time.sleep(1)
