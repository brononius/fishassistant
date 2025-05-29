import smbus
import time
from datetime import datetime, timedelta
import os
import sys

# Configuratie
ADS1115_ADDRESS = 0x48
GAIN = 3  # +/- 1.024V
LOG_DIRECTORY = "/diy/logs"
RETENTION_DAYS = 30
NUM_SAMPLES = 10 # Aantal metingen om te middelen voor het loggen

def read_raw_adc(channel):
    """Leest de ruwe analoge waarde van het gespecificeerde kanaal."""
    bus = smbus.SMBus(1)
    config = 0x8000 + (channel << 12) + (GAIN << 9) + (1 << 8)  # Single shot, gekozen kanaal, gain
    bus.write_word_data(ADS1115_ADDRESS, 0x01, config)
    time.sleep(0.01)
    value = bus.read_word_data(ADS1115_ADDRESS, 0x00)
    swapped_value = ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)
    bus.close()
    return swapped_value

def calculate_ph(adc_value):
    if adc_value <= 51569:
        # Kalibratie tussen pH 4.01 en 6.86
        slope = (6.86 - 4.01) / (51569 - 49159)
        intercept = 4.01 - slope * 49159
        return slope * adc_value + intercept
    else:
        # Kalibratie tussen pH 6.86 en 9.18
        slope = (9.18 - 6.86) / (53696 - 51569)
        intercept = 6.86 - slope * 51569
        return slope * adc_value + intercept

def cleanup_logs():
    now = datetime.now()
    cutoff = now - timedelta(RETENTION_DAYS)
    for filename in os.listdir(LOG_DIRECTORY):
        if filename.startswith("ph_") and filename.endswith(".log"):
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
    adc_channel = 1  # Lees kanaal A1 (pH sensor)
    ph_values = []
    try:
        for _ in range(NUM_SAMPLES):
            raw_value = read_raw_adc(adc_channel)
            ph_values.append(calculate_ph(raw_value))
            time.sleep(0.05)

        average_ph = sum(ph_values) / len(ph_values)

        log_filename = f"{LOG_DIRECTORY}/ph_{now.strftime('%Y%m%d')}.log"
        log_entry = f"{now.strftime('%H:%M:%S')}: {average_ph:.2f} pH\n"
        try:
            os.makedirs(LOG_DIRECTORY, exist_ok=True)
            with open(log_filename, "a") as log_file:
                log_file.write(log_entry)
#            print(f"pH waarde {average_ph:.2f} weggeschreven naar {log_filename}")
            print(f"PH waarde: {average_ph:.2f} ")
            sys.exit(0) # Succes
        except Exception as e:
            print(f"Fout bij wegschrijven naar logbestand: {e}")
            sys.exit(1) # Fout bij wegschrijven
    except Exception as e:
        print(f"Fout bij het uitlezen van de ADS1115: {e}")
        sys.exit(1) # Fout bij uitlezen
