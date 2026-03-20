# Station Meteo

This project reads the track temperature on a Raspberry Pi and exposes:

- a Flask web UI on port 9001
- a raw measurement server on port 9000

## Raspberry Pi Setup

Repository address:

```bash
https://github.com/MaximePWRT/Station_meteo.git
```

### 1. Connect to the Raspberry Pi

From another machine on the same network:

```bash
ssh pi@<raspberry-pi-ip>
```

Replace `<raspberry-pi-ip>` with the current IP of the Raspberry Pi.

If your Raspberry Pi hostname is known on the network, you can also use:

```bash
ssh pi@tracktemp-pi.local
```

### 2. Clone the project on a fresh Raspberry Pi

If the project is not already on the Pi:

```bash
cd /home/pi
git clone https://github.com/MaximePWRT/Station_meteo.git
cd /home/pi/Station_meteo
```

### 3. Update the project on a Raspberry Pi that already has it

If the repository is already present:

```bash
cd /home/pi/Station_meteo
git pull --ff-only
```

### 4. Run the installer

```bash
cd /home/pi/Station_meteo
bash installation/setup_raspberry_pi.sh
```

The installer will automatically:

- install the required system packages
- enable I2C
- create a Python virtual environment in `.venv`
- install Python dependencies from `requirements.txt`
- configure autostart with `systemd`

After installation, the services start automatically and also restart automatically on boot.

## Access The Station

Use the current Raspberry Pi IP address:

- `http://<raspberry-pi-ip>:9001`
- `http://<raspberry-pi-ip>:9000`

If hostname resolution is available on your network, you can also try:

- `http://tracktemp-pi.local:9001`
- `http://tracktemp-pi.local:9000`

To find the Raspberry Pi IP directly on the Pi:

```bash
hostname -I
```

To check the Raspberry Pi hostname directly on the Pi:

```bash
hostname
```

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