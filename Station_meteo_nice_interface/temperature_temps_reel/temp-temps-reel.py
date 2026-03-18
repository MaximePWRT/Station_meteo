#!/usr/bin/env python3
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request  
import RPi.GPIO as GPIO
import os
import time
from MCP3008 import MCP3008
import bme280
import numpy



led_rouge = 13
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_rouge, GPIO.OUT)
adc = MCP3008()

coeff = open('/home/pi/Station_meteo/Mesures_temperatures/coeff',"w")
print(0,file=coeff)
coeff.close()

gain = open('/home/pi/Station_meteo/Mesures_temperatures/gain',"w")
print(1,file=gain)
gain.close()

# f = open('/home/pi/Station_meteo/identity_sensors.txt')
# contenu = f.readlines()
# f.close()
# data_tempo = contenu[1].split(':')
# sensor_2 = data_tempo[1]

app = Flask(__name__)

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
    Track_Temperature_2 = Track_Temperature_1 ##- (208.07*numpy.exp(-0.019*mesure_lum())) ##- (78307777381.09*float(mesure_lum())**-4.44)
        
    return Track_Temperature_2
    



def mesure_humidity_temperature():
    date = datetime.now()
    heure = date.strftime("%H:%M")
    date_str = date.strftime("%d/%m/%Y  %H:%M")
    try:
        temperature_ext,pression,humidity = bme280.readBME280All()
    except :
        temperature_ext = -255
        pression = -255
        humidity = -255

    return heure, date_str, humidity, temperature_ext, pression

def on_off_affichage():
    f = open('/home/pi/Station_meteo/Mesures_temperatures/On_Off')
    a = f.readlines()
    f.close()
    var = float (a[0])
    if var == 1:
        etat = "on"
    else:
        etat = "Off"
        
    return etat


@app.route('/')
def affTemp():
    heure, date_str, humidity, temperature_ext, pression = mesure_humidity_temperature()
    return render_template('index.html', temp1 = round(mesure_capteur_1(),2) , temp3 = round(temperature_ext,2), humidity= round(humidity,2), heure = heure, date = date_str, pression = round(pression,2),coeff = coeff(),gain = gain(),lum = mesure_lum(), correcteur = on_off_affichage())


@app.route("/setcoeff", methods = ["post"])
def setcoeff():
    coeff = request.form["coeff"]
    f = open('/home/pi/Station_meteo/Mesures_temperatures/coeff',"w")
    print(coeff, file = f)
    f.close()
    return redirect(request.referrer)


@app.route("/setgain", methods = ["post"])
def setgain():
    gain = request.form["gain"]
    f = open('/home/pi/Station_meteo/Mesures_temperatures/gain',"w")
    print(gain, file = f)
    f.close()
    return redirect(request.referrer)


@app.route("/save_value", methods = ["post"])
def save_value():
    os.system ("sudo python3 /home/pi/Station_meteo/programme/app.py")
    return redirect(request.referrer)

@app.route("/removedata_bouton", methods = ["post"])
def removedata_bouton():
    if os.path.exists("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt"):
        os.remove("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt")
        for i in range (10):
            GPIO.output(led_rouge, 1)  # allumer la led
            time.sleep(0.1)  # temporisation en seconde
            GPIO.output(led_rouge, 0)  # eteindre la led
            time.sleep(0.1)  # temporisation en seconde
        os.system ("sudo python3 /home/pi/Station_meteo/programme/app.py")
    return redirect(request.referrer)

@app.route("/reboot_bouton", methods = ["post"])
def reboot_bouton():
    os.system ("sudo reboot now")
    return redirect(request.referrer)

@app.route("/shutdown_bouton", methods = ["post"])
def shutdown_bouton():
    os.system ("sudo shutdown now")
    return redirect(request.referrer)

@app.route("/on_off2", methods = ["post"])
def on_off2():
    
    f = open('/home/pi/Station_meteo/Mesures_temperatures/On_Off')
    a = f.readlines()
    f.close()
    var = float (a[0])
    if var == 1:
        f = open('/home/pi/Station_meteo/Mesures_temperatures/On_Off',"w")
        print(0, file = f)
        f.close()
    
    else:
        f = open('/home/pi/Station_meteo/Mesures_temperatures/On_Off',"w")
        print(1, file = f)
        f.close()
        
    return redirect(request.referrer)
    


##request

@app.route("/corrector", methods = ["get"])
def corrector():
    corrector = request.args
    offset = corrector["offset"]
    gain = corrector["gain"]

    f = open('/home/pi/Station_meteo/Mesures_temperatures/coeff',"w")
    print(offset, file = f)
    f.close()
    
    a = open('/home/pi/Station_meteo/Mesures_temperatures/gain',"w")
    print(gain, file = a)
    a.close()
    return

@app.route("/add_values")
def add_values():
    os.system ("sudo python3 /home/pi/Station_meteo/programme/app.py")
    return

@app.route("/shutdown")
def shutdown():
    os.system ("sudo shutdown now")
    return

@app.route("/reboot")
def reboot():
    os.system ("sudo reboot now")
    return

@app.route("/removedata")
def removedata():
    if os.path.exists("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt"):
        os.remove("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt")
        for i in range (10):
            GPIO.output(led_rouge, 1)  # allumer la led
            time.sleep(0.1)  # temporisation en seconde
            GPIO.output(led_rouge, 0)  # eteindre la led
            time.sleep(0.1)  # temporisation en seconde
        os.system ("sudo python3 /home/pi/Station_meteo/programme/app.py")
    return

@app.route("/instant_values")
def instant_values():
    Time, Humidity, T_Out, Atmos_P = mesure_humidity_temperature()
    T_Track = mesure_capteur_1()
    
    values = str(Time) +" / "+ str(round(T_Track,2)) +" / "+ str(round(Humidity,2)) +" / "+ str(T_Out) +" / "+ str(round(Atmos_P,2))
    
    return values

@app.route("/Values")
def Values():
    f = open('/home/pi/Station_meteo/Mesures_temperatures/mesure.txt')
    contenu = str(f.readlines())
    f.close()
    return contenu


app.run(debug=True, host='0.0.0.0', port=9001)
