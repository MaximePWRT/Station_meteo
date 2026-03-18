# Station Meteo - Copilot Notes

## Runtime endpoints
- Flask UI and API run on port 9001.
- Raw data server runs on port 9000 and serves Mesures_temperatures/mesure.txt.

## Temperature calibration model
- Use Offset A: active offset = latest manual calibration event.
- Calibration history file: Mesures_temperatures/calibration_history.csv.
- CSV columns: timestamp,reference_temp,sensor_reading,calculated_offset.

## Data contract
- Keep Track_Temperature_1 as the offseted value for downstream readers (HHDM).
- Keep raw value in extra column Track_Temperature_1_No_Offset.

## Sensor and hardware assumptions
- ADS1115 should use AnalogIn(ads, 0) for channel A0.
- If I2C or ADS1115 is unavailable, return -255 as fallback.

## Service paths on Raspberry Pi
- Flask script path: /home/pi/Station_meteo/temperature_temps_reel/temp-temps-reel.py
- Reboot script path: /home/pi/Station_meteo/programme/Reboot.py
