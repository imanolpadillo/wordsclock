# wordsclock
Clock based on words for ArduinoMega or RaspberryPi

## 🎮 Raspi commands

 1.  Raspi ssh access
```
ssh pi@192.168.0.25
```

 2. Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/wordsclock/raspberry/*.* pi@192.168.0.25:/home/pi/Documents/wordsclock
````

 3. Execute wordsclock manually from Raspi
```
cd /home/pi/Documents/wordsclock
python3 main.py
```

 4. Kill wordsclock program
```
ps aux | grep main.py
kill -7 process_id
```