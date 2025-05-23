import time
import subprocess
from datetime import datetime

# Intro
# -----

# Script om periodiek verschillen scripts te runnen.
# Je kan makkelijk scripts toevoegen, de timing aanpassen.

# Variabelen
# ----------

RUN_INTERVAL_SECONDS = 5  # Standaard elke minuut, kun je aanpassen

SCRIPTS_TO_RUN = {
    "/diy/valueTemperature.py": "Y",
    "/diy/valueInWater.py": "Y",
}


# Script
# ------
def run_script(script_name):
    try:
        subprocess.run(["python3", f"{script_name}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het uitvoeren van script '{script_name}': {e}")
    except FileNotFoundError:
        print(f"Fout: Script '{script_name}' niet gevonden.")

if __name__ == "__main__":
    print(f"\nDe scripts zullen elke {RUN_INTERVAL_SECONDS} seconden uitgevoerd worden.")
    print("\nDe volgende scripts zijn geconfigureerd:")
    for script, should_run in SCRIPTS_TO_RUN.items():
        status = "wordt uitgevoerd" if should_run.upper() == "Y" else "wordt overgeslagen"
        print(f"- {script}: {status}")

    while True:
        now = datetime.now()
        formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"\nPeriodieke run ({formatted_time}):")
        for script, should_run in SCRIPTS_TO_RUN.items():
            if should_run.upper() == "Y":
                run_script(script)
            else:
                pass # Script wordt overgeslagen, geen actie nodig hier
        time.sleep(RUN_INTERVAL_SECONDS)
