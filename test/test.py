import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
relais_pin = 5
GPIO.setup(relais_pin, GPIO.OUT)

try:
    print("Relais AAN (LOW) voor 5 seconden...")
    GPIO.output(relais_pin, GPIO.LOW)
    time.sleep(5)
    print("Relais UIT (HIGH).")
    GPIO.output(relais_pin, GPIO.HIGH)
finally:
    GPIO.cleanup()
