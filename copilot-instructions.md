# Station Meteo - Copilot Notes

## Runtime endpoints
- Flask UI and API run on port 9001.
- Raw data server runs on port 9000 and serves Mesures_temperatures/mesure.txt.

## Temperature model
- Use raw sensor value (no calibration offset applied).

## Data contract
- Keep Track_Temperature_1 as the raw value for downstream readers (HHDM).

## Sensor and hardware assumptions
- ADS1115 should use AnalogIn(ads, 0) for channel A0.
- If I2C or ADS1115 is unavailable, return -255 as fallback.

## Service paths on Raspberry Pi
- Flask script path: /home/pi/Station_meteo/temperature_temps_reel/temp-temps-reel.py
- Reboot script path: /home/pi/Station_meteo/programme/Reboot.py
