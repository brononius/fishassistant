# Quick and Dirty
ToDo List for Fish Assistant

## What I’m Trying
A complete installation to monitor the water for example a fish tank, pond...

Different monitoring tools, controls (pump, lights...).

Main software will be controlled by Home Assistant.

I put all my scripts in the folder /diy/.

If you change this, all scripts need to be updated accordingly.

## Sensors, steps
### Temperature
Simple measurement of temperature
- Hardware: DS18B20
- Connectivity: 3.3V + GND + GPIO 21
- Symbolic link: gpio21InTemperature -> /sys/bus/w1/devices/28-0000008564fc/w1_slave
- Script: /diy/valueTemperature.py


### PH Sensor

### NH Sensor

### Water Sensor
Measurement of sensor in or out water (level warning)
- Hardware: CQRSENYW002
- Connectivity: 3.3V + GND + GPIO 20
- Script: /diy/valueInWater.py

### Out 1
- Connectivity: 5V + GND + 5
- Script: /diy/outRelay1.py
    - ON: "python /diy/outRelay1.py ON"
    - OFF: "python /diy/outRelay1.py OFF"

### Out 2
- Connectivity: 5V + GND + 6
- Script: /diy/outRelay2.py
    - ON: "python /diy/outRelay2.py ON"
    - OFF: "python /diy/outRelay2.py OFF"

### Out 3
- Connectivity: 5V + GND + 13
- Script: /diy/outRelay3.py
    - ON: "python /diy/outRelay3.py ON"
    - OFF: "python /diy/outRelay3.py OFF"

### Out 4
- Connectivity: 5V + GND + 19
- Script: /diy/outRelay4.py
    - ON: "python /diy/outRelay4.py ON"
    - OFF: "python /diy/outRelay4.py OFF"


### Led Red


### Led Green


### Camera

  Motion

### All Scripts
To run all scripts, I'm using 1 script where you define the timing, the kind of sensors you have, the LED status...

- Script: valueAll.py
