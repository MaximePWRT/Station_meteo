import urllib.request
import RPi.GPIO as GPIO
import os
import time
import socket
import json


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

            
    #     GPIO.output(led_verte, 1)
    if os.path.exists("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt"):
        try:
            urllib.request.urlopen('http://wrtweather:9000/')
            GPIO.output(led_verte, 1)
            time_ref = time.process_time()
        except:
            if time.process_time() - time_ref > 120 :
                GPIO.output(led_verte, 0)
            else :
                for i in range (10):
                    GPIO.output(led_verte, 1)  # allumer la led
#                     time.sleep(0.1)  # temporisation en seconde
#                     GPIO.output(led_verte, 0)  # eteindre la led
#                     time.sleep(0.1)  # temporisation en seconde
                time_ref-=2
    time.sleep(20)