# Quick and Dirty
ToDo List for Fish Assistant

## What I’m Trying
A complete installation to monitor the water for example a fish tank, pond...
Different monitoring tools, controls (pump, lights...). 
Main software will be controlled by Home Assistant.
I put all my scripts in the folder /diy/
If you change this, all scripts need to be updated accordingly.

## Sensors, steps
- Temperature
    Simple measurement of temperature
    DS18B20
    3.3V + GND + GPIO 21
    Symbolic link: gpio21InTemperature -> /sys/bus/w1/devices/28-0000008564fc/w1_slave
    Script: /diy/valueTemperature.py

- PH Sensor

- NH Sensor

- Water Sensor
    Measurement of sensor in or out water (level warning)
    CQRSENYW002
    3.3V + GND + GPIO 20
    Script: /diy/valueInWater.py

- Out 1
    5V + GND + 5
    Script: /diy/outRelay1.py
        ON: "python /diy/outRelay1.py ON"
        OFF: "python /diy/outRelay1.py OFF"

- Out 2
    5V + GND + 5
    Script: /diy/outRelay2.py
        ON: "python /diy/outRelay2.py ON"
        OFF: "python /diy/outRelay2.py OFF"

- Out 3
    5V + GND + 5
    Script: /diy/outRelay3.py
        ON: "python /diy/outRelay3.py ON"
        OFF: "python /diy/outRelay3.py OFF"

- Out 4
    5V + GND + 5
    Script: /diy/outRelay4.py
        ON: "python /diy/outRelay4.py ON"
        OFF: "python /diy/outRelay4.py OFF"


- Led Red


- Led Green


- Camera

  Motion




-rw-r--r-- 1 root root 3.3K May 26 14:41 valueAll.py

-rw-r--r-- 1 root root  983 May 26 15:33 outRelay2.py
-rw-r--r-- 1 root root  984 May 26 15:33 outRelay3.py
-rw-r--r-- 1 root root  984 May 26 15:33 outRelay4.py
-rw-r--r-- 1 root root  703 May 26 15:58 README.md
  
