import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import os
import sys

LOG_DIRECTORY = "/diy/logs"
RETENTION_DAYS = 30
SENSOR_PIN = 20  # De GPIO pin waar de waterniveausensor is aangesloten

# Stel de GPIO modus in op BCM nummering
GPIO.setmode(GPIO.BCM)
# Stel de GPIO pin in als input
GPIO.setup(SENSOR_PIN, GPIO.IN)

def get_water_level():
    """Leest de status van de waterniveausensor."""
    try:
        sensor_waarde = GPIO.input(SENSOR_PIN)
        if sensor_waarde == GPIO.HIGH:
            return "Ja"
        else:
            return "Nee"
    except Exception as e:
        print(f"Fout bij het uitlezen van de waterniveausensor: {e}")
        return None

def cleanup_logs():
    """Verwijdert oude logbestanden."""
    now = datetime.now()
    cutoff = now - timedelta(days=RETENTION_DAYS)
    for filename in os.listdir(LOG_DIRECTORY):
        if filename.startswith("waterniveau_") and filename.endswith(".log"):
            filepath = os.path.join(LOG_DIRECTORY, filename)
            try:
                file_creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if file_creation_time < cutoff:
                    os.remove(filepath)
                    print(f"Oud logbestand verwijderd: {filepath}")
            except Exception as e:
                print(f"Fout bij het controleren/verwijderen van logbestand {filepath}: {e}")

if __name__ == "__main__":
    cleanup_logs() # Eerst de oude logs opruimen
    now = datetime.now()
    water_level = get_water_level()
    if water_level is None:
        GPIO.cleanup()
        sys.exit(1) # Fout bij het uitlezen van de sensor

    log_filename = f"{LOG_DIRECTORY}/waterniveau_{now.strftime('%Y%m%d')}.log"
    log_entry = f"{now.strftime('%H:%M:%S')}: {water_level}\n"
    try:
        with open(log_filename, "a") as log_file:
            log_file.write(log_entry)
        print(f"Waterniveau: {water_level}")
        sys.exit(0) # Succes
    except Exception as e:
        print(f"Fout bij wegschrijven naar logbestand: {e}")
        GPIO.cleanup()
