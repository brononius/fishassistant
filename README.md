
# Quality meter for Fishtank, Pond...

--- Under Development ---

A complete installation to monitor the water for example a fish tank, pond...

- Different monitoring tools as Temperatur, PH, NH, waterlevel ...
- Different controls as pump, lights ...
- Extra's as realtime video ...
- Hardware design, 3D print casing...
- Control software by Home Assistant. Dashboard, rules ...


## Hard- & Software

### Raspberry pi
Central board is a raspberry pi Zero 2W.

I put all my scripts in the folder /diy/. If you change this, all scripts need to be updated accordingly.

To run all scripts below, I'm using just 1 script where you define the timing, the kind of sensors you have, the LED status...

- Script: valueAll.py


### Temperature
Simple measurement of temperature
- Hardware: DS18B20
- Connectivity: 3.3V + GND + GPIO 21
- Symbolic link: /diy/gpio21InTemperature -> /sys/bus/w1/devices/28-0000008564fc/w1_slave

      ln -s /sys/bus/w1/devices/28-0000008564fc/w1_slave /diy/gpio21InTemperature

- Script: /diy/valueTemperature.py


### PH Sensor

### NH Sensor

### Water Sensor
Measurement of sensor in or out water (level warning)
- Hardware: CQRSENYW002
- Connectivity: 3.3V + GND + GPIO 20
- Script: /diy/valueInWater.py

### Out 1
Simply ON/OFF relay that can be used for lights, pumps...
- Hardware: Relaymodule DC 5V 230V 4 Channels (Out 1 > Out 4)
- Connectivity: 5V + GND + 5
- Script: /diy/outRelay1.py
    - ON: "python /diy/outRelay1.py ON"
    - OFF: "python /diy/outRelay1.py OFF"

### Out 2
Simply ON/OFF relay that can be used for lights, pumps...
- Hardware: Relaymodule DC 5V 230V 4 Channels (Out 1 > Out 4)
- Connectivity: 5V + GND + 6
- Script: /diy/outRelay2.py
    - ON: "python /diy/outRelay2.py ON"
    - OFF: "python /diy/outRelay2.py OFF"

### Out 3
Simply ON/OFF relay that can be used for lights, pumps...
- Hardware: Relaymodule DC 5V 230V 4 Channels (Out 1 > Out 4)
- Connectivity: 5V + GND + 13
- Script: /diy/outRelay3.py
    - ON: "python /diy/outRelay3.py ON"
    - OFF: "python /diy/outRelay3.py OFF"

### Out 4
Simply ON/OFF relay that can be used for lights, pumps...
- Hardware: Relaymodule DC 5V 230V 4 Channels (Out 1 > Out 4)
- Connectivity: 5V + GND + 19
- Script: /diy/outRelay4.py
    - ON: "python /diy/outRelay4.py ON"
    - OFF: "python /diy/outRelay4.py OFF"


### Led Red
Showing the status of the running scripts. Can also be controlled from outside (eg Home Assitant) to show when a treshold is triggered (eg to low temperature).
- Hardware: LED Red
- Connectivity: 5V + 23
- Script: ValueAll.py

### Led Green
Showing the status of the running scripts. Can also be controlled from outside (eg Home Assitant) to show when a treshold is triggered (eg to low temperature).
- Hardware: LED Red
- Connectivity: 5V + 24
- Script: ValueAll.py


### Camera
Raspberry PI camera, to show the enviroment (eg pond, fish tank...)
  Motion

### Home Assistant

#### MQTT connectivity

#### Dashboard

#### Rules, automations
