import time
import board
import subprocess
from datetime import datetime, timedelta
import os
import sys

LOG_DIRECTORY = "/diy/logs"
RETENTION_DAYS = 30
TEMP_FILE = "/diy/gpio21InTemperature"

def get_temperature():
    try:
        full_temp_output = subprocess.check_output(["cat", TEMP_FILE], text=True).strip()
        lines = full_temp_output.splitlines()
        if len(lines) >= 2:
            temp_gpio21_line2 = lines[1].strip()
            if "t=" in temp_gpio21_line2:
                parts = temp_gpio21_line2.split("t=")
                if len(parts) > 1:
                    raw_temp_str = parts[1].strip()
                    try:
                        raw_temp_int = int(raw_temp_str)
                        return raw_temp_int / 1000.0
                    except ValueError:
                        print(f"Fout: Kan 't=' waarde niet converteren naar een getal: {raw_temp_str}")
                        return None
                else:
                    print(f"Waarschuwing: 't=' gevonden maar geen waarde erna. Volledige output: {temp_gpio21_line2}")
                    return None
            else:
                print(f"Waarschuwing: 't=' niet gevonden in de tweede regel. Volledige output: {temp_gpio21_line2}")
                return None
        else:
            print(f"Waarschuwing: Bestand {TEMP_FILE} bevat minder dan twee regels. Volledige output: {full_temp_output}")
            return None
    except FileNotFoundError:
        print(f"Fout: Bestand {TEMP_FILE} niet gevonden.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het lezen van {TEMP_FILE}: {e}")
        return None
    except Exception as e:
        print(f"Onverwachte fout bij uitlezen temperatuur: {e}")
        return None

def cleanup_logs():
    now = datetime.now()
    cutoff = now - timedelta(days=RETENTION_DAYS)
    for filename in os.listdir(LOG_DIRECTORY):
        if filename.startswith("temperatuur_") and filename.endswith(".log"):
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
    temperature = get_temperature()
    if temperature is not None:
        log_filename = f"{LOG_DIRECTORY}/temperatuur_{now.strftime('%Y%m%d')}.log"
        log_entry = f"{now.strftime('%H:%M:%S')}: {temperature:.1f}°C\n"
        try:
            with open(log_filename, "a") as log_file:
                log_file.write(log_entry)
            print(f"Temperatuur {temperature:.1f}°C")
            sys.exit(0) # Succes
        except Exception as e:
            print(f"Fout bij wegschrijven naar logbestand: {e}")
            sys.exit(1) # Fout bij wegschrijven
    else:
        sys.exit(1) # Fout bij het ophalen van de temperatuur
