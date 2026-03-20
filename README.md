# Station Meteo

This project runs a Raspberry Pi weather station with:

- a Flask web UI on port 9001
- a raw measurement server on port 9000
- an ADS1115-based temperature acquisition flow over I2C

## Fresh Raspberry Pi Setup

After cloning the repository on the Raspberry Pi:

```bash
cd /home/pi/Station_meteo
bash installation/setup_raspberry_pi.sh
```

The installer will:

- install the required system packages
- enable I2C
- create a Python virtual environment in `.venv`
- install Python dependencies from `requirements.txt`
- configure autostart with `systemd`

## Installed Services

The installer creates these units:

- `station-meteo-ui.service`
- `station-meteo-raw.service`
- `station-meteo-writer.service`
- `station-meteo-writer.timer`

## Useful Commands

Check status:

```bash
sudo systemctl status station-meteo-ui.service
sudo systemctl status station-meteo-raw.service
sudo systemctl status station-meteo-writer.timer
```

Restart services:

```bash
sudo systemctl restart station-meteo-ui.service
sudo systemctl restart station-meteo-raw.service
sudo systemctl restart station-meteo-writer.timer
```

Default endpoints:

- `http://<raspberry-pi-ip>:9001`
- `http://<raspberry-pi-ip>:9000`