# Import
import os
import time
import RPi.GPIO as GPIO


# Definition des pins
demarrage = 6
pinBtn = 5
led_rouge = 13
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Definition des pins en entree / sortie
GPIO.setup(pinBtn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(demarrage, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#led def
GPIO.setup(led_rouge, GPIO.OUT)



# Boucle infinie
while True:
    etat = GPIO.input(pinBtn)
    print(etat)
    etat_2 = GPIO.input(demarrage)
    if (etat_2 == 1) :
        os.system ("sudo shutdown now")

    # etat==0 => bouton appuye => LED allumee
    if os.path.exists("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt"):
    
        if (etat == 1) :
            os.remove("/home/pi/Station_meteo/Mesures_temperatures/mesure.txt") 
            for i in range (10):
                GPIO.output(led_rouge, 1)  # allumer la led
                time.sleep(0.1)  # temporisation en seconde
                GPIO.output(led_rouge, 0)  # eteindre la led
                time.sleep(0.1)  # temporisation en seconde
            os.system ("sudo python3 /home/pi/Station_meteo/programme/app.py")
    # Temps de repos pour eviter la surchauffe du processeur
    time.sleep(0.3)