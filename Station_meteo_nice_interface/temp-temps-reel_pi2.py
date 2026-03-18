#!/usr/bin/env python3
from datetime import datetime
from flask import Flask, render_template, redirect, request
import os
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialisation de l'I2C et de l'ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Chemins des fichiers de configuration
MESURES_PATH = '/home/pi/Station_meteo/Mesures_temperatures/mesure.txt'
SERVEUR_SCRIPT = '/home/pi/Station_meteo/programme/app.py'

app = Flask(__name__)

def lire_fichier(chemin):
    try:
        with open(chemin, 'r') as fichier:
            return fichier.readline().strip()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {chemin}: {e}")
        return None

def mesure_capteur():
    # Lire la valeur analogique du canal A0
    chan = AnalogIn(ads, ADS.P0)  # Remplacer ADS.P0 par le bon canal si nécessaire
    voltage = chan.voltage  # Lire la tension en volts

    # Conversion de la tension en température
    track_temperature = voltage/3*340-70
    return track_temperature

@app.route('/')
def affTemp():
    heure = datetime.now().strftime("%H:%M")
    return render_template('index.html', 
                           temp1=round(mesure_capteur(), 2), 
                           temp3=-255,  # Suppression des données du BME280
                           humidity=-255,  # Suppression de l'humidité
                           heure=heure, 
                           pression=-255)  # Suppression de la pression

@app.route("/save_value", methods=["post"])
def save_value():
    os.system(f"sudo python3 {SERVEUR_SCRIPT}")
    return redirect(request.referrer)

@app.route("/removedata_bouton", methods=["post"])
def removedata_bouton():
    if os.path.exists(MESURES_PATH):
        os.remove(MESURES_PATH)
        os.system(f"sudo python3 {SERVEUR_SCRIPT}")
    return redirect(request.referrer)

@app.route("/reboot_bouton", methods=["post"])
def reboot_bouton():
    os.system("sudo reboot now")
    return redirect(request.referrer)

@app.route("/shutdown_bouton", methods=["post"])
def shutdown_bouton():
    os.system("sudo shutdown now")
    return redirect(request.referrer)

@app.route("/add_values")
def add_values():
    os.system(f"sudo python3 {SERVEUR_SCRIPT}")
    return

@app.route("/shutdown")
def shutdown():
    os.system("sudo shutdown now")
    return

@app.route("/reboot")
def reboot():
    os.system("sudo reboot now")
    return

@app.route("/removedata")
def removedata():
    if os.path.exists(MESURES_PATH):
        os.remove(MESURES_PATH)
        os.system(f"sudo python3 {SERVEUR_SCRIPT}")
    return

@app.route("/instant_values")
def instant_values():
    Time = datetime.now().strftime("%H:%M")
    T_Track = mesure_capteur()
    values = f"{Time} / {round(T_Track, 2)} /  /  / "
    return values

@app.route("/Values")
def Values():
    try:
        with open(MESURES_PATH, 'r') as f:
            contenu = f.read()
    except Exception as e:
        contenu = f"Erreur lors de la lecture du fichier: {e}"
    return contenu

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)