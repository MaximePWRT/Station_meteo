import urllib.request
import RPi.GPIO as GPIO
import os
import time
import socket
import json
import bme280

led_verte = 26
led_orange = 19
led_rouge = 13

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(led_verte, GPIO.OUT)
GPIO.setup(led_orange, GPIO.OUT)
GPIO.setup(led_rouge, GPIO.OUT)

GPIO.output(led_verte, 0)
GPIO.output(led_orange, 0)
GPIO.output(led_rouge, 0)



time_ref = time.process_time()

while True :
    
# #test capteurs
    try :
        temperature_ext,pression,humidity = bme280.readBME280All()
        GPIO.output(led_orange, 0)

    except:

        GPIO.output(led_orange, 1)


#test connexion lan
    try :
        googleIP = "8.8.8.8"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((googleIP, 0))
        addrIP = s.getsockname()[0]
        host = socket.gethostname()
        GPIO.output(led_rouge, 0)

    except :
        GPIO.output(led_rouge, 1)

    time.sleep(20)
    