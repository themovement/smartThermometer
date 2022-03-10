#! /usr/bin/python

import os
import time
import glob
import smtplib
import math
from email.mime.text import MIMEText
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sensors i used are high temp wire sensors DS18B20
#Amazon title Gikfun DS18B20 Temperature Sensor Waterproof Digital Thermal Probe Sensor for Arduino (Pack of 5pcs) EK1083
temp_sensor1 = '/sys/bus/w1/devices/28-01144bf8a9aa/w1_slave'
temp_sensor2 = '/sys/bus/w1/devices/28-01144d0516aa/w1_slave'
temp_sensor3 = '/sys/bus/w1/devices/28-01144d5718aa/w1_slave'

alert1Sent = False
alert2Sent = False
alert3Sent = False

#Finish setting Up 7 segment display for Temps. never got to this.
# GPIO ports for the 7seg pins

#segments =  (11,4,23,14,10,13,25)
segments =  (25,10,23,4,11,13,14)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-3 pins 
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
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


def sendText(msg):
    # Email address i use to send texts to myself, you need to turn off Security features to allow 3rd parties to log in ( the pi )
    USERNAME = "blahblah@gmail.com"
    # Password for above email address
    PASSWORD = "password"
    # I email text messages to myself so look at att, or vzr for their ending  @txt.att.net or @vtext.com
    MAILTO = "phoneNumber@txt.att.net"

    msg = MIMEText(msg)
    msg['Subject'] = 'Alert'
    msg['From'] = USERNAME
    msg['to'] = MAILTO

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME, MAILTO, msg.as_string())
    server.quit()

def read_temp_raw():
    f1 = open(temp_sensor1, 'r')
    lines1 = f1.readlines()
    f1.close()

    f2 = open(temp_sensor2, 'r')
    lines2 = f2.readlines()
    f2.close()

    f3 = open(temp_sensor3, 'r')
    lines3 = f3.readlines()
    f3.close()

    return lines1 + lines2 + lines3

def dispay_temp(tmp1):
    m = math.ceil(tmp1)
    s = str(m)
    print(s)
    for digit in range(len(s)):
        GPIO.output(digits[digit],1)
        for loop in range(0,7):
            GPIO.output(segments[loop], num[s[digit]][loop])
            print(segments[loop], num[s[digit]][loop])
       
        
# Curently set up for a brisket i monitor point / flat / air temp if any get out of range i send emial
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES' or lines[4].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t='), lines[3].find('t='), lines[5].find('t=')
    temp_string = lines[1].strip()[equals_pos[0]+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0

    temp_string2 = lines[3].strip()[equals_pos[1]+2:]
    temp_c2 = float(temp_string2) / 1000.0
    temp_f2 = temp_c2 * 9.0 / 5.0 + 32.0

    temp_string3 = lines[5].strip()[equals_pos[2]+2:]
    temp_c3 = float(temp_string3) / 1000.0
    temp_f3 = temp_c3 * 9.0 / 5.0 + 32.0
    global alert1Sent
    global alert2Sent
    global alert3Sent
    dispay_temp(temp_f);

    if temp_f  > 200 and alert1Sent == False:
        sendText("Meat Left Done")
        alert1Sent = True
        print("Meat Left" , temp_f)
    else:
        print("Meat Left" , temp_f)

    if temp_f2  > 200 and alert2Sent == False:
        sendText("Meat Right Done")
        alert2Sent = True
        print("Meat Right" , temp_f2)
    else:
        print("Meat Right" , temp_f2)

    if temp_f3  < 200 and alert3Sent == False:
        sendText("Smoker Temp Low")
        alert3Sent = True
        print("Smoker Temp" , temp_f3)
    else:
        print("Smoker Temp" , temp_f3)

    return
while True:
    read_temp()
    time.sleep(30)