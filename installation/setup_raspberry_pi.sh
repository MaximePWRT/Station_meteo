#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVICE_USER="${SUDO_USER:-$(id -un)}"
VENV_DIR="$REPO_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "This installer must be run on the Raspberry Pi itself."
    exit 1
fi

if [[ ! -f "$REPO_DIR/requirements.txt" ]]; then
    echo "Missing requirements.txt in $REPO_DIR"
    exit 1
fi

run_sudo() {
    sudo "$@"
}

install_packages() {
    run_sudo apt update
    run_sudo apt install -y \
        git \
        python3 \
        python3-pip \
        python3-venv \
    python3-lgpio \
        nodejs \
        npm \
        i2c-tools \
        python3-smbus
}

enable_i2c() {
    if command -v raspi-config >/dev/null 2>&1; then
        run_sudo raspi-config nonint do_i2c 0
        return
    fi

    local config_file="/boot/firmware/config.txt"
    if ! run_sudo grep -q '^dtparam=i2c_arm=on' "$config_file"; then
        echo "dtparam=i2c_arm=on" | run_sudo tee -a "$config_file" >/dev/null
    fi
}

create_venv() {
    if [[ -f "$VENV_DIR/pyvenv.cfg" ]] && grep -q '^include-system-site-packages = false$' "$VENV_DIR/pyvenv.cfg"; then
        rm -rf "$VENV_DIR"
    fi

    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv --system-site-packages "$VENV_DIR"
    fi

    "$PIP_BIN" install --upgrade pip
    "$PIP_BIN" install -r "$REPO_DIR/requirements.txt"
}

install_sudoers() {
    local sudoers_file="/etc/sudoers.d/station-meteo"
    cat <<EOF | run_sudo tee "$sudoers_file" >/dev/null
$SERVICE_USER ALL=(root) NOPASSWD: /usr/sbin/reboot, /usr/sbin/shutdown
EOF
    run_sudo chmod 440 "$sudoers_file"
}

install_units() {
    cat <<EOF | run_sudo tee /etc/systemd/system/station-meteo-ui.service >/dev/null
[Unit]
Description=Station Meteo Flask UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$REPO_DIR
ExecStart=$PYTHON_BIN $REPO_DIR/temperature_temps_reel/temp-temps-reel.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    cat <<EOF | run_sudo tee /etc/systemd/system/station-meteo-raw.service >/dev/null
[Unit]
Description=Station Meteo Raw Data Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$REPO_DIR
ExecStart=/usr/bin/node $REPO_DIR/serveur/serveur.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    cat <<EOF | run_sudo tee /etc/systemd/system/station-meteo-writer.service >/dev/null
[Unit]
Description=Station Meteo Measurement Writer
After=network.target

[Service]
Type=oneshot
User=$SERVICE_USER
WorkingDirectory=$REPO_DIR
ExecStart=$PYTHON_BIN $REPO_DIR/programme/app.py
EOF

    cat <<EOF | run_sudo tee /etc/systemd/system/station-meteo-writer.timer >/dev/null
[Unit]
Description=Station Meteo Measurement Writer Timer

[Timer]
OnBootSec=30s
OnUnitActiveSec=10min
AccuracySec=1s
Persistent=true
Unit=station-meteo-writer.service

[Install]
WantedBy=timers.target
EOF
}

enable_units() {
    run_sudo systemctl daemon-reload
    run_sudo systemctl enable station-meteo-ui.service station-meteo-raw.service station-meteo-writer.timer
    run_sudo systemctl restart station-meteo-ui.service
    run_sudo systemctl restart station-meteo-raw.service
    run_sudo systemctl start station-meteo-writer.service
    run_sudo systemctl restart station-meteo-writer.timer
}

print_summary() {
    local host_ip
    host_ip="$(hostname -I | awk '{print $1}')"
    echo
    echo "Station Meteo setup complete."
    echo "UI:  http://$host_ip:9001"
    echo "Raw: http://$host_ip:9000"
    echo
    echo "Service status commands:"
    echo "  sudo systemctl status station-meteo-ui.service"
    echo "  sudo systemctl status station-meteo-raw.service"
    echo "  sudo systemctl status station-meteo-writer.timer"
}

install_packages
enable_i2c
create_venv
install_sudoers
install_units
enable_units
print_summary