#!/usr/bin/env python3
from datetime import datetime
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

# Chemins des fichiers
MESURES_PATH = '/home/pi/Station_meteo/Mesures_temperatures/mesure.txt'
SERVEUR_SCRIPT = '/home/pi/Station_meteo/serveur/serveur.js'

def lire_fichier(chemin):
    try:
        with open(chemin, 'r') as fichier:
            return fichier.readline().strip()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {chemin}: {e}")
        return None

def mesure_track_temp():
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

def temp_cpu():
    return lire_fichier("/sys/class/thermal/thermal_zone0/temp")[:2]

# Programme principal
subprocess.run(["sudo", "pkill", "-x", "node"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
date = datetime.now()
track_temperature = mesure_track_temp()
jour = date.strftime("%Y-%m-%d")
heure = date.strftime("%H:%M")
    
mesure = f"{jour} / {heure} / {round(track_temperature, 2)} /  /  / "
repertoire = os.path.dirname(MESURES_PATH)
os.makedirs(repertoire, exist_ok=True)
    
mode = 'a' if os.path.exists(MESURES_PATH) else 'w'
with open(MESURES_PATH, mode) as f:
    if mode == 'w':
        f.write("Date / Time / Track_Temperature_1 / Humidity_% / Outside_Temperature / Atmospheric pressure hpa\n")
    f.write(mesure + '\n')
subprocess.run(["node", SERVEUR_SCRIPT], check=False)