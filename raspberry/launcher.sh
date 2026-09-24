#!/bin/bash
sleep 10
cd /home/pi/Documents/wordsclock
source ./bin/activate
mkdir -p logs
python3 main.py >> logs/wordsclock.log 2>&1
