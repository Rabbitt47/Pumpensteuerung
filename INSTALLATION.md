# Pumpensteuerung - Installationsanleitung

## Überblick

Dieses Projekt erstellt ein automatisches Pumpen-Steuersystem für Raspberry Pi mit Touch-Display Bedienung.

## Hardware-Liste

### Essenzielle Komponenten
- Raspberry Pi 3B+ oder höher
- Strom PI (Power Management + RTC)
- Waveshare 7" HDMI LCD Touch Screen (1024x600)
- 5x Digital Input Module (für Sensoren)
- 3x Relais Module (für Ausgänge)
- Micro-SD Karte (min. 16GB)
- USB-Netzteil für Raspberry Pi (2.5A+)

### Sensoren/Schalter
- 5x Float-Schalter oder Kapazitive Level-Sensoren
- Jumper-Kabel und Stecker

### Stromversorgung/Relais
- Netzteil für 230V → 5V Umschaltung
- 3x Relais-Module oder Motorschutzschalter
- Kabel für Pumpe, Bewässerung, Fehler-Signal

## Schritt-für-Schritt Installation

### 1. Raspberry Pi OS vorbereiten

```bash
# SD-Karte mit Raspberry Pi Imager formatieren
# - Raspberry Pi OS Lite (64-bit) auswählen
# - SSH und WLAN aktivieren
# - In Advanced Options

# SSH verbinden
ssh pi@raspberrypi.local
# Standard Passwort: raspberry
```

### 2. Betriebssystem aktualisieren

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git python3-pip python3-dev
```

### 3. I2C und Strom PI aktivieren

```bash
# I2C aktivieren
sudo raspi-config
# Interfacing Options -> I2C -> Yes -> Finish
# Reboot: Yes

# Nach Reboot: I2C Tools installieren
sudo apt-get install -y i2c-tools
sudo apt-get install -y libffi-dev libssl-dev
```

### 4. RTC-Modul (Strom PI) konfigurieren

```bash
# RTC aktivieren
sudo nano /etc/modules
# Am Ende hinzufügen: rtc-ds3231
# Speichern: Ctrl+X, Y, Enter

# Device Tree konfigurieren
sudo nano /boot/firmware/config.txt
# Am Ende hinzufügen:
# dtoverlay=i2c-rtc,ds3231

sudo reboot
```

### 5. Verprojekt clonen oder hochladen

```bash
cd /home/pi
# Option A: Wenn auf GitHub
git clone <your-repo-url> Pumpensteuerung
cd Pumpensteuerung

# Option B: Dateiübertragung von Windows
# (sftp oder scp verwenden)
```

### 6. Python-Dependencies installieren

```bash
cd /home/pi/Pumpensteuerung

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Zusätzlich für GUI
pip install kivy

# Für Raspberry Pi GPIO
pip install RPi.GPIO
```

### 7. GPIO-Pins testen

```bash
# Testen ob GPIO funktioniert
python3 -c "
from src.gpio_handler import GPIOManager
gm = GPIOManager()
print('GPIO Manager initialisiert')
print('Eingänge:', list(gm.inputs.keys()))
print('Ausgänge:', list(gm.outputs.keys()))
"
```

### 8. Hardwire-Verbindungen

#### GPIO-Pin Belegung überprüfen

```bash
# Raspberry Pi GPIO-Layout anzeigen
pinout
```

#### Eingänge verdrahten (5V Sensoren)

```
Sensor 1 (BRUNNEN_VOLL):
  + → 5V Power
  - → GND
  Signal → GPIO 17 (via Pull-Up Widerstand)

[Gleiches für die anderen 4 Sensoren mit GPIO 27, 22, 23, 24]
```

#### Ausgänge verdrahten (230V Relais)

```
WICHTIG: GPIO kann nur 3.3V, max 16mA liefern!
Muss über Relais-Modul oder Optokoppler erfolgen!

GPIO Output → Relais-Modul → 230V Pump/Ventil
```

### 9. Display konfigurieren

```bash
# Waveshare Display aktivieren
sudo nano /boot/firmware/config.txt

# Hinzufügen:
max_usb_current=1
hdmi_drive=2
config_hdmi_boost=4

# Speichern und reboot
sudo reboot
```

### 10. Autostart konfigurieren

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/pumpensteuerung.service
```

```ini
[Unit]
Description=Pump Control System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Pumpensteuerung
ExecStart=/home/pi/Pumpensteuerung/venv/bin/python /home/pi/Pumpensteuerung/main_new.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service aktivieren
sudo systemctl daemon-reload
sudo systemctl enable pumpensteuerung
sudo systemctl start pumpensteuerung

# Status überprüfen
sudo systemctl status pumpensteuerung

# Logs anschauen
sudo journalctl -u pumpensteuerung -f
```

## Testing

### 1. Lokales Testen (ohne Hardware)

```bash
# Im Windows/Mac Terminal
pip install kivy
python main_new.py
```

Die App läuft im Simulations-Modus ohne GPIO.

### 2. RTC testen

```bash
# RTC-Modul überprüfen
sudo i2cdetect -y 1
# Sollte "68" anzeigen (DS3231 I2C-Adresse)

# Zeit lesen
sudo hwclock --show

# Zeit mit System synchronisieren
sudo hwclock --hctosys
```

### 3. GPIO Test

```bash
# Als root ausführen
sudo python3 << 'EOF'
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

# Test Eingang
GPIO.setup(17, GPIO.IN)
state = GPIO.input(17)
print(f"GPIO 17: {state}")

# Test Ausgang
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
sleep(0.5)
GPIO.output(18, GPIO.LOW)
print("GPIO 18 Toggle erfolgreich")

GPIO.cleanup()
EOF
```

## Problembehebung

### App startet nicht

```bash
# Logs überprüfen
tail -f logs/app.log
tail -f logs/ui.log

# Kivy Fehler?
python main_new.py 2>&1 | tee debug.log
```

### Display zeigt nichts

```bash
# HDMI überprüfen
sudo tvservice -l

# Ausgänge aktivieren
sudo tvservice -p

# Resolution prüfen
sudo xrandr
```

### GPIO-Fehler

```bash
# BCM Pinmapping überprüfen
gpio readall

# als root testen
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM)"
```

### RTC funktioniert nicht

```bash
# I2C-Geräte auflisten
i2cdetect -y 1

# Wenn DS3231 nicht sichtbar:
# 1. Verbindung überprüfen
# 2. Modul neu starten: sudo modprobe -r rtc_ds3231
# 3. Modul neu laden: sudo modprobe rtc_ds3231
```

## Erste Inbetriebnahme

1. **Starten:**
   ```bash
   ssh pi@raspberrypi.local
   sudo systemctl start pumpensteuerung
   ```

2. **Interface öffnen:**
   - Auf dem 7" Display oder SSH-Verbindung
   - Hauptmenü sollte sichtbar sein

3. **Einstellungen konfigurieren:**
   - ⚙ EINSTELLUNGEN öffnen
   - Pumpzeiten setzen
   - Speichern

4. **Sensoren testen:**
   - Im Hauptmenü E/A-Zustände überprüfen
   - Sensoren manuell auslösen
   - Status sollte sich ändern

5. **Manualbetrieb testen:**
   - 🎮 MANUALBETRIEB
   - Pumpe-Buttons testen
   - Prüfe, dass Relais schaltet

6. **Automatikbetrieb aktivieren:**
   - Modus toggle auf AUTOMATIK
   - System sollte automatisch je nach Sensoren schalten

## Konfiguration

Siehe [README.md](README.md) für Menüstruktur und Logik.

Siehe [CUSTOMIZATION.md](CUSTOMIZATION.md) für UI-Anpassungen.

Siehe [GPIO_CONFIG.md](GPIO_CONFIG.md) für GPIO-Konfiguration.

## Logs und Daten

```bash
# App-Logs
tail -f /home/pi/Pumpensteuerung/logs/app.log

# UI-Logs
tail -f /home/pi/Pumpensteuerung/logs/ui.log

# Pumpvorgänge (CSV)
ls /home/pi/Pumpensteuerung/logs/pump_log_*.csv

# CSV-Datei anschauen
cat /home/pi/Pumpensteuerung/logs/pump_log_2024-02-01.csv
```

## Systemd Service Befehle

```bash
# Status
sudo systemctl status pumpensteuerung

# Start
sudo systemctl start pumpensteuerung

# Stop
sudo systemctl stop pumpensteuerung

# Restart
sudo systemctl restart pumpensteuerung

# Enable (beim Boot starten)
sudo systemctl enable pumpensteuerung

# Disable
sudo systemctl disable pumpensteuerung

# Logs
sudo journalctl -u pumpensteuerung -f
sudo journalctl -u pumpensteuerung --since "2 hours ago"
```

## Sicherung und Backup

```bash
# Konfiguration sichern
cp -r /home/pi/Pumpensteuerung/config /home/pi/pump_config_backup

# Logs sichern
cp -r /home/pi/Pumpensteuerung/logs /home/pi/pump_logs_backup

# SD-Karte vollständig sichern (von Windows mit Win32DiskImager)
```

## Weitere Schritte

1. **SSL für Remote-Zugriff**: SSH-Schlüssel statt Passwort
2. **Backup-Strategie**: Automatische Datensicherung
3. **Monitoring**: Systemüberwachung hinzufügen
4. **Web-Interface**: Optional REST-API für Remote-Zugriff
5. **Fehlerbenachrichtigungen**: E-Mail/SMS bei Fehlern

---

**Wichtig:** Immer Sicherheit beachten!
- GPIO-Pins sind 3.3V
- Relais für 230V verwenden
- Fehlererkennung aktiv halten
- Maximale Pumpzeit konfigurieren
