#!/usr/bin/env python3
from datetime import datetime
from flask import Flask, render_template, redirect, request
import os
import subprocess
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialisation de l'I2C et de l'ADS1115
ads = None
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
except Exception as e:
    print(f"I2C/ADS1115 indisponible: {e}")

# Chemins des fichiers de configuration
MESURES_PATH = '/home/pi/Station_meteo/Mesures_temperatures/mesure.txt'

app = Flask(__name__)


def run_command(command):
    subprocess.run(command, check=False)


def ensure_parent_dir(path):
    repertoire = os.path.dirname(path)
    os.makedirs(repertoire, exist_ok=True)

def lire_fichier(chemin):
    try:
        with open(chemin, 'r') as fichier:
            return fichier.readline().strip()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {chemin}: {e}")
        return None

def mesure_capteur():
    if ads is None:
        return -255

    # Lire la valeur analogique du canal A0
    try:
        chan = AnalogIn(ads, 0)
        voltage = chan.voltage  # Lire la tension en volts
    except Exception as e:
        print(f"Erreur lecture capteur: {e}")
        return -255

    # Conversion de la tension en température
    track_temperature = voltage/3*340-70
    return track_temperature


def append_measurement():
    date = datetime.now()
    track_temperature = mesure_capteur()
    jour = date.strftime("%Y-%m-%d")
    heure = date.strftime("%H:%M")
    mesure = f"{jour} / {heure} / {round(track_temperature, 2)} /  /  / "

    ensure_parent_dir(MESURES_PATH)

    mode = 'a' if os.path.exists(MESURES_PATH) else 'w'
    with open(MESURES_PATH, mode) as fichier:
        if mode == 'w':
            fichier.write("Date / Time / Track_Temperature_1 / Humidity_% / Outside_Temperature / Atmospheric pressure hpa\n")
        fichier.write(mesure + '\n')

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
    append_measurement()
    return redirect(request.referrer)

@app.route("/removedata_bouton", methods=["post"])
def removedata_bouton():
    if os.path.exists(MESURES_PATH):
        os.remove(MESURES_PATH)
    append_measurement()
    return redirect(request.referrer)

@app.route("/reboot_bouton", methods=["post"])
def reboot_bouton():
    run_command(["sudo", "reboot", "now"])
    return redirect(request.referrer)

@app.route("/shutdown_bouton", methods=["post"])
def shutdown_bouton():
    run_command(["sudo", "shutdown", "now"])
    return redirect(request.referrer)

@app.route("/add_values")
def add_values():
    append_measurement()
    return "", 204

@app.route("/shutdown")
def shutdown():
    run_command(["sudo", "shutdown", "now"])
    return "", 204

@app.route("/reboot")
def reboot():
    run_command(["sudo", "reboot", "now"])
    return "", 204

@app.route("/removedata")
def removedata():
    if os.path.exists(MESURES_PATH):
        os.remove(MESURES_PATH)
    append_measurement()
    return "", 204

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
    app.run(debug=False, host='0.0.0.0', port=9001, use_reloader=False)