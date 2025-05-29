import time
import subprocess
from datetime import datetime
import RPi.GPIO as GPIO

# Stel de GPIO-modus in op BCM-nummering
GPIO.setmode(GPIO.BCM)

# Definieer de GPIO-pinnen
rood_led_pin = 23
groen_led_pin = 24

# Stel de GPIO-pinnen in als outputs
GPIO.setup(rood_led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(groen_led_pin, GPIO.OUT, initial=GPIO.HIGH) # Initieel groen aan

def set_groen_status(status):
    GPIO.output(groen_led_pin, status)

def set_rood_status(status):
    GPIO.output(rood_led_pin, status)

def knipper_rood(aantal=3, snelheid=0.2):
    for _ in range(aantal):
        GPIO.output(rood_led_pin, GPIO.HIGH)
        time.sleep(snelheid)
        GPIO.output(rood_led_pin, GPIO.LOW)
        time.sleep(snelheid)

def knipper_groen(aantal=3, snelheid=0.5):
    for _ in range(aantal):
        GPIO.output(groen_led_pin, GPIO.HIGH)
        time.sleep(snelheid)
        GPIO.output(groen_led_pin, GPIO.LOW)
        time.sleep(snelheid)

# Variabelen
# ----------

RUN_INTERVAL_SECONDS = 5  # Standaard elke minuut, kun je aanpassen

SCRIPTS_TO_RUN = {
    "/diy/valueTemperature.py": "Y",
    "/diy/valuePh.py": "Y",
    "/diy/valueTds.py": "Y",
    "/diy/valueInWater.py": "Y",
}

# Script
# ------
def run_script(script_name):
    try:
        result = subprocess.run(["python3", f"{script_name}"], capture_output=True, text=True)
        print(result.stdout.strip()) # Print de output van het script
        if result.returncode == 0:
#            print(f"Script '{script_name}' succesvol uitgevoerd.")
            return True
        else:
            print(f"Script '{script_name}' gaf een foutcode: {result.returncode}")
            print(f"Stderr: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print(f"Fout: Script '{script_name}' niet gevonden.")
        return False

if __name__ == "__main__":
    print(f"De scripts zullen elke {RUN_INTERVAL_SECONDS} seconden uitgevoerd worden.")
    print("\nDe volgende scripts zijn geconfigureerd:")
    for script, should_run in SCRIPTS_TO_RUN.items():
        status = "wordt uitgevoerd" if should_run.upper() == "Y" else "wordt overgeslagen"
        print(f"- {script}: {status}")

    try:
        while True:
            now = datetime.now()
            formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
#            print(f"\nPeriodieke run ({formatted_time}):")
            all_scripts_ok = True

            for script, should_run in SCRIPTS_TO_RUN.items():
                if should_run.upper() == "Y":
                    if not run_script(script):
                        all_scripts_ok = False

            if all_scripts_ok:
                # Alle scripts succesvol (return code 0)
                set_groen_status(GPIO.HIGH)
                set_rood_status(GPIO.LOW)
#               print("Alle geconfigureerde scripts succesvol uitgevoerd.")
            else:
                # Minstens één script gaf een non-zero return code
                print("Minstens één script heeft een fout geretourneerd!")
                knipper_rood(aantal=3, snelheid=0.2)
                set_groen_status(GPIO.LOW)
                set_rood_status(GPIO.HIGH)

            time.sleep(RUN_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Script gestopt door de gebruiker.")

    finally:
        GPIO.cleanup()
        print("GPIO opgeruimd.")
