#-------------------------------
# Alejandro De los Santos
# EMail: alejandrodlsp@hotmail.es
# Twitter: @alejandrodlsp
#-------------------------------

# Default 4 Digit Display GPIO Layout:
# D1:2, D2:3, D3:4, D4:14,
# A:15, B:17, C:18, D:27, E:22, F:23, G:24, DP:10
# Pin layout: https://i.stack.imgur.com/vJzZu.png

segments =  (15,17,18,27,22,23,24,10) # Define GPIO ports for the 7seg pins
digits = (2,3,4,14) # Define GPIO ports for the digit 0-3 pins

print_views = false # Set to true to print total view count instead of subscriber count
keyboard_interrupt = true; # Interrupt program with keyboard

refreshRate = 10  #Subscribers refresh rate in seconds
url = "https://www.googleapis.com/youtube/v3/channels?key={API KEY}&forUsername={YOUTUBE USERNAME}&part=statistics"   # replace {API key} with your google dev API key and {YOUTUBE USERNAME} with the channel username

import RPi.GPIO as GPIO
import time
import sys
import json
import requests
import socket
import urllib
import string
from decimal import Decimal

GPIO.setmode(GPIO.BCM)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ':(0,0,0,0,0,0,0),	# Define segment combination for each number
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}


def get_json():  # Get JSON data from youtube's api
    res = requests.get(url)
    if(res.status_code==200):
        json_data = json.loads(res.text)
        return json_data
    return {}

def parseData():   # Parses subscriber count and view count from JSON data
    try:
        data = get_json()
        subscribers = Decimal(int(data["items"][0]["statistics"]["subscriberCount"]))
        views = int(data["items"][0]["statistics"]["viewCount"])
        print(subscribers)
        print(views)
        return print_views? views: subscribers
    except KeyboardInterrupt:
        if keyboard_interrupt:
            sys.exit(-1)



# Display value in 4 digits 7 segment display
refreshCount = refreshRate * 100
n = 0
try:
    while True:
        time.sleep(.01)

        if refreshCount == refreshRate * 100:
            n = parseData()
            refreshCount = 0
        else:
            refreshCount += 1

        n = int(n)
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])

            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
finally:
    GPIO.cleanup()
