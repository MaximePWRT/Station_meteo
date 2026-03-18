import time
from datetime import datetime, timedelta
import os
import RPi.GPIO as GPIO
from MCP3008 import MCP3008
import bme280
import numpy

date_reff = datetime.now()
date_reff_H = int(date_reff.strftime("%H"))
##date_reff_M = int(date_reff.strftime("%M"))

while True :
    
    
    reff_H = int(datetime.now().strftime("%H")) - date_reff_H
    ##reff_M = int(datetime.now().strftime("%M")) - date_reff_M
    if (reff_H == 8) :
        os.system ("sudo reboot")

    time.sleep(10)