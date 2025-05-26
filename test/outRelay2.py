import RPi.GPIO as GPIO
import time
import sys

# Stel de GPIO-modus in op BCM-nummering
GPIO.setmode(GPIO.BCM)

# Definieer de GPIO-pin voor het relais (pas dit aan indien nodig)
relais_pin = 6

# Stel de GPIO-pin in als output
GPIO.setup(relais_pin, GPIO.OUT)

def set_relais(status):
    delay = 0.1  # Voeg een kleine vertraging toe
    if status.upper() == "ON":
        print(f"Relais op GPIO {relais_pin} inschakelen (LOW).")
        GPIO.output(relais_pin, GPIO.LOW)
        time.sleep(delay)
    elif status.upper() == "OFF":
        print(f"Relais op GPIO {relais_pin} uitschakelen (HIGH).")
        GPIO.output(relais_pin, GPIO.HIGH)
        time.sleep(delay)
    else:
        print(f"Ongeldige status: '{status}'. Gebruik 'ON' of 'OFF'.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        command = sys.argv[1]
        set_relais(command)
    else:
        print("Gebruik: python3 outRelay1.py [ON|OFF]")
        print("Voorbeeld: python3 outRelay1.py ON")
