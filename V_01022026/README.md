# Pumpensteuerung mit Raspberry Pi 3+

Automatische Pumpensteuerung für Brunnen und IBC-Container mit Waveshare 7-Zoll Touch-Display.

## Hardware-Anforderungen

- **Raspberry Pi 3+** oder höher
- **Strom PI** (RTC-Modul und Power Management)
- **Waveshare 7" LCD HDMI 1024x600** mit kapazitivem Touchscreen
- **5 digitale Eingänge** (Sensoren)
  - BRUNNEN_VOLL (HIGH)
  - BRUNNEN_LEER (LOW)
  - IBC_VOLL (HIGH)
  - IBC_MITTE (HIGH)
  - IBC_LEER (LOW)
- **3 digitale Ausgänge** (Relais)
  - PUMPE
  - BEWÄSSERUNG
  - FEHLER

## Installation

### 1. Abhängigkeiten installieren

```bash
# Python-Pakete
pip install -r requirements.txt

# Kivy-Dependencies (für GUI)
sudo apt-get install python3-kivy

# GPIO-Bibliotheken
pip install RPi.GPIO
```

### 2. Projektstruktur

```
Pumpensteuerung/
├── main_new.py              # Hauptanwendung
├── src/
│   ├── app.py              # Kernlogik
│   ├── gpio_handler.py      # GPIO-Verwaltung
│   ├── pump_logic.py        # Pumpensteuerungslogik
│   ├── pump_logger.py       # CSV-Logging
│   └── config_manager.py    # Konfiguration
├── ui/
│   ├── main_screen.py       # Hauptmenü
│   ├── settings_screen.py   # Einstellungen
│   ├── manual_screen.py     # Manualbetrieb
│   └── history_screen.py    # Pumpverlauf
├── config/
│   └── settings.json        # Einstellungsdatei
├── logs/                    # Logdateien
└── README.md
```

## Pin-Belegung

### GPIO-Eingänge (BCM-Nummerierung)

| Sensor | GPIO | Logik |
|--------|------|-------|
| BRUNNEN_VOLL | GPIO 17 | HIGH = voll |
| BRUNNEN_LEER | GPIO 27 | HIGH = leer |
| IBC_VOLL | GPIO 22 | HIGH = voll |
| IBC_MITTE | GPIO 23 | HIGH = mittel |
| IBC_LEER | GPIO 24 | HIGH = leer |

### GPIO-Ausgänge (BCM-Nummerierung)

| Ausgang | GPIO | Logik |
|---------|------|-------|
| PUMPE | GPIO 18 | HIGH = ein |
| BEWÄSSERUNG | GPIO 25 | HIGH = ein |
| FEHLER | GPIO 16 | LOW = Fehler |

## Steuerungslogik

### Automatikbetrieb

**Pumpe einschalten (HIGH):**
- Zeit innerhalb Pumpzeitfenster UND
- Brunnen voll UND
- NICHT IBC_MITTE

**Pumpe ausschalten (LOW):**
- Brunnen leer ODER
- IBC voll

**Fehlererkennung (Fehler = LOW):**
- Brunnen: VOLL und LEER gleichzeitig
- IBC: MITTE und LEER gleichzeitig
- IBC: VOLL ohne MITTE
- IBC: LEER und MITTE gleichzeitig

### Manualbetrieb

- Pumpe über Button ein/ausschalten
- Automatische Abschaltung nach maximaler Pumpzeit (Standard: 30 Min)
- Abschaltung wenn Brunnen leer wird

## Konfiguration

Einstellungen werden in `config/settings.json` gespeichert:

```json
{
  "pump_start_time": "22:00",
  "pump_end_time": "04:00",
  "max_pump_duration": 30,
  "system_sleep_timeout": 10,
  "pump_off_sleep_timeout": 10,
  "wake_interval": 30,
  "wake_duration": 5,
  "display_theme": "dark",
  "date_format": "%d.%m.%Y",
  "time_format": "%H:%M:%S"
}
```

## Menüstruktur

### 1. Hauptmenü
- **Pump-Status Anzeige** (Echtzeit)
- **E/A Zustände** (Alle Eingänge und Ausgänge)
- **Pumpzeiten** (Start, Ende, Max-Dauer)
- **Betriebsmodus Toggle** (Automatik / Manuell)
- **Buttons:**
  - ⚙ Einstellungen
  - 📋 Pumpverlauf
  - 🎮 Manualbetrieb

### 2. Einstellungen
- Pump-Startzeit (Stunden, Minuten)
- Pump-Endzeit (Stunden, Minuten)
- Maximale Pumpzeit (Minuten)
- Speichern und Zurück

### 3. Manualbetrieb
- Digitale E/A Anzeige
- 🟢 Pumpe EIN Button
- 🔴 Pumpe AUS Button
- Automatische Abschaltung nach Max-Pumpzeit

### 4. Pumpverlauf
- Tabelle der letzten 10 Pumpvorgänge
- Spalten: Startzeit, Stoppzeit, Dauer (min)
- CSV-Export auf SD-Karte (täglich)

## Layout anpassen

### Farben ändern

In den UI-Dateien (`ui/*.py`) können Farben einfach angepasst werden:

```python
# RGB-Farbe (0-1 range)
button.background_color = (R, G, B, A)

# Beispiele:
(0.2, 0.8, 0.2, 1)  # Grün
(0.8, 0.2, 0.2, 1)  # Rot
(0.2, 0.2, 0.8, 1)  # Blau
```

### Schriftgrößen ändern

```python
Label(text='Text', font_size='16sp')  # 16 Scale Points
```

### Layout-Dimensionen

Grid-Layouts können in den UI-Dateien konfiguriert werden:

```python
GridLayout(cols=2, spacing=10, size_hint_y=0.5)
```

- `cols`: Spaltenanzahl
- `rows`: Zeilenanzahl (automatisch berechnet)
- `spacing`: Abstand zwischen Elementen (Pixel)
- `size_hint_y`: Relative Höhe (0.0 - 1.0)
- `size_hint_x`: Relative Breite (0.0 - 1.0)

## Logging und Datenexport

### CSV-Logdatei
Täglich eine neue CSV-Datei: `logs/pump_log_YYYY-MM-DD.csv`

Spalten:
- Startzeit
- Sensor-Zustände beim Start
- Stoppzeit
- Sensor-Zustände beim Stop
- Dauer (Minuten)

### App-Log
`logs/app.log` - Alle Systemereignisse und Fehler

## Betriebsmodi

### Automatikbetrieb
- Pumpe läuft nach konfigurierten Zeiten
- Intelligente Sensoren-Logik
- Fehlererkennung aktiv

### Manualbetrieb
- Manuelle Steuerung über Touch-Buttons
- Sensoren werden weiterhin überwacht
- Max-Pumpzeit wird eingehalten

## Sleep-Modus (Strom PI)

Das System kann in den Schlafmodus versetzt werden:

- **Nach 10 Min Boot** - Wenn keine Aktivität
- **Nach 10 Min Pump-Stop** - Energy-Saving
- **Aufweckung alle 30 Min** - 5 Minuten aktiv
- **Sensoren-Check** - Bei Aufweckung

## Fehlerbehebung

### GPIO-Fehler

Wenn GPIO nicht verfügbar ist (z.B. auf Windows), läuft die App im **Simulation Modus**.

```python
# In gpio_handler.py
ON_RASPBERRY = False  # Automatisch erkannt
```

### Display-Kalibrierung

Für Waveshare 7" Display in `config/settings.json`:

```bash
# Touchscreen-Kalibrierung durchführen
sudo TSLIB_CALIBFILE=/etc/pointercal TSLIB_CONFFILE=/etc/ts.conf xinput-calibrator
```

### RTC-Modul

RTC vom Strom PI wird automatisch erkannt. Falls nicht vorhanden, wird Systemzeit verwendet.

## Start und Stop

### Starten
```bash
# Terminal 1
python main_new.py

# Oder mit nohup für Background
nohup python main_new.py &
```

### Herunterfahren
- **ESC-Taste** im Display
- **Oder:** Systembefehl `shutdown -h now`

## Anpassungen und Entwicklung

### Neue Eingänge hinzufügen

In `src/gpio_handler.py`:

```python
self.inputs['NEUER_SENSOR'] = DigitalInput(pin=26, name='NEUER_SENSOR')
```

In `src/pump_logic.py`:

```python
neuer_sensor = self.gpio.get_input('NEUER_SENSOR').is_high()
```

### Neue Logik-Regeln

In `src/pump_logic.py` - Methode `calculate_pump_state_automatic()`:

```python
if condition1 and condition2:
    return True  # Pumpe ein
return False     # Pumpe aus
```

### UI-Farben und Layout

Jede UI-Datei in `ui/` ist unabhängig und kann einzeln angepasst werden.

## Lizenz

Projekt für Eigennutzung

## Support

Bei Fragen oder Problemen:
1. Logs in `logs/` überprüfen
2. GPIO-Verbindungen prüfen
3. Konfiguration in `config/settings.json` validieren
