import time
from datetime import datetime, timedelta
import os

date_reff = datetime.now()

while True :
    elapsed = datetime.now() - date_reff
    if elapsed >= timedelta(hours=8):
        os.system ("sudo reboot")

    time.sleep(10)