import smbus
import time
from datetime import datetime, timedelta
import os
import sys

# Configuratie
ADS1115_ADDRESS = 0x48
GAIN = 1  # +/- 4.096V
LOG_DIRECTORY = "/diy/logs"
RETENTION_DAYS = 30
NUM_SAMPLES = 10 # Aantal metingen om te middelen voor het loggen

def read_raw_adc(channel):
    """Leest de ruwe analoge waarde van het gespecificeerde kanaal."""
    bus = smbus.SMBus(1)
    config = 0x8000  # Start single conversion

    # Select input channel (single-ended)
    if channel == 0:
        config |= (4 << 12)  # AIN0
    elif channel == 1:
        config |= (5 << 12)  # AIN1
    elif channel == 2:
        config |= (6 << 12)  # AIN2
    elif channel == 3:
        config |= (7 << 12)  # AIN3

    # Set gain
    if GAIN == 0:
        config |= (0 << 9)  # +/- 6.144V
    elif GAIN == 1:
        config |= (1 << 9)  # +/- 4.096V
    elif GAIN == 2:
        config |= (2 << 9)  # +/- 2.048V
    elif GAIN == 3:
        config |= (3 << 9)  # +/- 1.024V
    elif GAIN == 4:
        config |= (4 << 9)  # +/- 0.512V
    elif GAIN == 5:
        config |= (5 << 9)  # +/- 0.256V
    elif GAIN == 6:
        config |= (6 << 9)  # +/- 0.128V
    elif GAIN == 7:
        config |= (7 << 9)  # +/- 0.064V

    # Set single-shot mode
    config |= (1 << 8)

    # No comparator
    config |= (0 << 4)

    # Single-shot conversion
    config |= (1 << 15)

    bus.write_word_data(ADS1115_ADDRESS, 0x01, config) # ADS1115_CONFIG_REG is 0x01
    time.sleep(0.01) # Kortere wachttijd voor meerdere metingen
    value = bus.read_word_data(ADS1115_ADDRESS, 0x00) # ADS1115_CONVERSION_REG is 0x00
    swapped_value = ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)
    bus.close()
    return swapped_value

def cleanup_logs():
    now = datetime.now()
    cutoff = now - timedelta(RETENTION_DAYS)
    for filename in os.listdir(LOG_DIRECTORY):
        if filename.startswith("tds_") and filename.endswith(".log"):
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
    adc_channel = 3  # Lees kanaal A3 (kan je aanpassen)
    tds_values = []
    try:
        for _ in range(NUM_SAMPLES):
            raw_value = read_raw_adc(adc_channel)
            voltage = (raw_value * 4.096) / 32767
            tds_value = (voltage / 2.3) * 1000
            tds_values.append(tds_value)
            time.sleep(0.05)

        average_tds = sum(tds_values) / len(tds_values)

        log_filename = f"{LOG_DIRECTORY}/tds_{now.strftime('%Y%m%d')}.log"
        log_entry = f"{now.strftime('%H:%M:%S')}: {average_tds:.2f} ppm\n"
        try:
            os.makedirs(LOG_DIRECTORY, exist_ok=True)
            with open(log_filename, "a") as log_file:
                log_file.write(log_entry)
            print(f"TDS: {average_tds:.2f} ppm")
            sys.exit(0) # Succes
        except Exception as e:
            print(f"Fout bij wegschrijven naar logbestand: {e}")
            sys.exit(1) # Fout bij wegschrijven
    except Exception as e:
        print(f"Fout bij het uitlezen van de ADS1115: {e}")
        sys.exit(1) # Fout bij uitlezen
