import os
import subprocess

# Fonction pour exécuter les commandes système
def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de : {command}")
        exit(1)  # Arrêter le script en cas d'erreur

# Mettre à jour le système
run_command("sudo apt update")
run_command("sudo apt upgrade -y")

# Installer les dépendances Python et I2C
run_command("sudo apt install -y python3-pip i2c-tools python3-smbus")

# Installer les bibliothèques Python nécessaires
run_command("pip3 install adafruit-circuitpython-ads1x15 --break-system-packages")

# Installer Node.js et npm
run_command("sudo apt install -y nodejs npm")

print("Toutes les dépendances sont installées avec succès !")