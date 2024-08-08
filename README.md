# wordsclock
Clock based on words for ArduinoMega or RaspberryPi

## 🎮 Raspi commands

 1.  Raspi ssh access
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