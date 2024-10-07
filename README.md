# wordsclock
Clock based on words for ArduinoMega or RaspberryPi

## 🕹 Action button

The action button changes the wordsclock mode in the following way:
  - LongClick:      ALWAYS_OFF_MODE
  - x1 SingleClick: ALWAYS_ON_MODE
  - X2 SingleClick: FLASH_MODE
  - X3 SingleClick: ECO_MODE

## 💡 Clock modes

  - ALWAYS_OFF_MODE: The leds are always switched off.
  - ALWAYS_ON_MODE:  The leds are always switched on.
  - FLASH_MODE:      The leds are only activated during some seconds when minutes change.
  - ECO_MODE:        For every hour of the week, it can be scheduled the clock mode to ALWAYS_ON_MODE, FLASH_MODE or ALWAYS_OFF_MODE. This can be done modifying the variable ECO_MODE_SCHEDULE in [wordsclockEnum.py](raspberry/wordsclockEnum.py).


## 🎮 Raspi commands

 0. Get raspi ip
```
ping wordsclock.local
```

 2.  Raspi ssh access
```
ssh pi@192.168.0.71
```

 2. Prerequisites:
```
Enable I2C in raspi preferences
python -m venv wordsclock
wordsclock/bin/pip install smbus2
wordsclock/bin/pip install pcf8574-io
wordsclock/bin/pip install pytz
```

 3. Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/wordsclock/raspberry/*.* pi@192.168.0.71:/home/pi/Documents/wordsclock
````

 4. Execute wordsclock manually from Raspi
```
cd /home/pi/Documents/wordsclock
source ./bin/activate
python3 main.py
```

 5. Kill wordsclock program
```
ps aux | grep main.py
kill -7 process_id
```

 6. Program a cron for executing wordsclock on restart
```
sudo crontab -e -u pi
@reboot /bin/bash /home/pi/Documents/wordsclock/launcher.sh >/home/pi/Documents/wordsclock/logs/cron.log 2>&1
0 0 * * 0 > /home/pi/Documents/wordsclock/logs/wordsclock.log
```

 7. Read Raspi logs
```
cd /home/pi/Documents/wordsclock/logs
cat wordsclock.log
```

EXTRA: How to deal WIFI change?
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add at the end of the file the new WIFI network and password
```
network={
    ssid="Network1"
    psk="password1"
}

network={
    ssid="Network2"
    psk="password2"
}
```
