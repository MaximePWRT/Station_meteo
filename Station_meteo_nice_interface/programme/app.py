#!/usr/bin/env python3
import time
from datetime import datetime, timedelta
import os
import RPi.GPIO as GPIO
from MCP3008 import MCP3008
import bme280
import numpy


led_verte = 23
led_orange = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_orange, GPIO.OUT)
GPIO.setup(led_verte, GPIO.OUT)
adc = MCP3008()

# f = open('/home/pi/Station_meteo/identity_sensors.txt')
# contenu = f.readlines()
# f.close()
# data_tempo = contenu[1].split(':')
# sensor_2 = data_tempo[1]

def coeff():
    f = open('/home/pi/Station_meteo/Mesures_temperatures/coeff')
    a = f.readlines()
    f.close()
    coeff = a[0]
    return coeff

def gain():
    f = open('/home/pi/Station_meteo/Mesures_temperatures/gain')
    a = f.readlines()
    f.close()
    gain = a[0]
    return gain

def mesure_lum ():
    
    lum = adc.read( channel = 4 )                      
    return lum

def mesure_capteur_1():


    value = adc.read( channel = 4 )

    Track_Temperature_1 = (((value / 1023.0*3.3)/3)*450-70)##*float(gain()) + float(coeff())
    f = open('/home/pi/Station_meteo/Mesures_temperatures/On_Off')
    a = f.readlines()
    f.close()
    var = float (a[0])
    
    Track_Temperature_2 = Track_Temperature_1 ##- (78307777381.09*float(mesure_lum())**-4.44)
        
    return Track_Temperature_2
    
  



def mesure_humidity_temperature():
    try :
        temperature_ext,pression,humidity = bme280.readBME280All()
    except :
        temperature_ext = -255
        pression = -255
        humidity = -255
    return humidity,temperature_ext,pression

def Temp_CPU():
    f = open("/sys/class/thermal/thermal_zone0/temp")
    a = f.readlines()
    temp = a[0]
    temp = temp[0:2]
    return temp

def mesure_lum ():
    lum = adc.read( channel = 4 )      
    return lum

def getTemp():
    date = datetime.now()
    Track_Temperature_1 = mesure_capteur_1()
    lum = mesure_lum()
    
    jour = str(date)[:10]
    heur = date.strftime("%H:%M")

    humidity, temperature_ext, pression = mesure_humidity_temperature()
        
    mesure = jour + " / " + heur + " / " + str(round(Track_Temperature_1,2)) + " / " + str(round (humidity,2)) + " / " + str(round(temperature_ext,2)) + " / " + str(round(pression,2)) + " / " + str(lum)
    repertoire = '/home/pi/Station_meteo/Mesures_temperatures/'
    if not os.path.isdir(repertoire):
        os.makedirs(repertoire)
        
    fich_Temp = repertoire + 'mesure.txt'
    if os.path.exists(fich_Temp):
        f = open(fich_Temp,"a")
    else:
        f = open(fich_Temp,"w")
        print("Date / Time / Track_Temperature_1 / Humidity_% / Outside_Temperature / Atmospheric pressure hpa / luminosity ", file=f)
        
    print(mesure, file=f)
    f.close()





#Programme principal

        
os.system ("sudo killall node")
for i in range (10):
    GPIO.output(led_verte, 0)  # allumer la led
    time.sleep(0.1)  # temporisation en seconde
    GPIO.output(led_verte, 1)  # eteindre la led
    time.sleep(0.1)  # temporisation en seconde
                
getTemp()
os.system ("node /home/pi/Station_meteo/serveur/serveur.js")


