# Pumpensteuerung - Projektübersicht

## Projektstruktur

```
Pumpensteuerung/
│
├── 📄 main_new.py                 # ⭐ HAUPTANWENDUNG - Starten Sie diese
├── 📄 main.py                     # Alte Version (deprecated)
│
├── 📂 src/                        # Kernlogik und Business-Logik
│   ├── __init__.py               # Package Init
│   ├── app.py                    # Hauptanwendungsklasse
│   ├── gpio_handler.py           # GPIO Ein-/Ausgänge
│   ├── pump_logic.py             # Pumpensteuerungslogik
│   ├── pump_logger.py            # CSV-Logging
│   ├── config_manager.py         # Konfigurationsverwaltung
│   └── strom_pi_manager.py       # Strom PI Integration (RTC, Sleep)
│
├── 📂 ui/                         # Benutzeroberfläche (Kivy)
│   ├── __init__.py               # Package Init
│   ├── main_screen.py            # Hauptmenü
│   ├── settings_screen.py        # Einstellungen
│   ├── manual_screen.py          # Manualbetrieb
│   └── history_screen.py         # Pumpverlauf-Anzeige
│
├── 📂 config/                     # Konfigurationsdateien
│   └── settings.json             # Einstellungen (Uhrzeit, Pumpzeiten, etc.)
│
├── 📂 logs/                       # Logdateien
│   ├── app.log                   # App-Logdatei
│   ├── ui.log                    # UI-Logdatei
│   └── pump_log_YYYY-MM-DD.csv   # Tägliche CSV mit Pumpvorgängen
│
├── 📄 README.md                  # 📖 Grundlegender Überblick und Dokumentation
├── 📄 INSTALLATION.md            # 🔧 Schritt-für-Schritt Installationsanleitung
├── 📄 CUSTOMIZATION.md           # 🎨 Anleitung zur UI-Anpassung (Farben, Layout)
├── 📄 GPIO_CONFIG.md             # ⚡ GPIO Pin-Konfiguration und Hardware-Setup
├── 📄 requirements.txt           # 📦 Python Dependencies
└── 📄 FEATURES.md                # ✨ Detaillierte Feature-Übersicht
```

## Schnellstart

### Auf Raspberry Pi

```bash
# 1. Projekt clonen oder hochladen
cd /home/pi
git clone <repo-url> Pumpensteuerung
cd Pumpensteuerung

# 2. Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Starten
python main_new.py
```

### Lokal (Windows/Mac) - Simulation

```bash
# Ohne Hardware, nur UI-Test
pip install kivy
python main_new.py
```

## Dateien schnell erklären

### ⭐ Hauptdateien

| Datei | Zweck | Ändern für |
|-------|-------|-----------|
| `main_new.py` | **App-Start** | - |
| `src/app.py` | Kernlogik | Logik-Änderungen |
| `src/pump_logic.py` | Steuerungslogik | Pumpen-Regeln ändern |
| `config/settings.json` | Einstellungen | Uhrzeit, Pumpzeiten |
| `ui/main_screen.py` | Hauptmenü | UI-Layout, Farben |

### 🔌 Hardware-Integration

| Datei | Zweck |
|-------|-------|
| `src/gpio_handler.py` | GPIO Pin-Verwaltung |
| `src/strom_pi_manager.py` | RTC + Sleep-Mode |
| `GPIO_CONFIG.md` | Pin-Konfiguration |

### 📝 Dokumentation

| Datei | Inhalt |
|-------|--------|
| `README.md` | Überblick, Features, Menüstruktur |
| `INSTALLATION.md` | Schritt-für-Schritt Setup |
| `CUSTOMIZATION.md` | UI anpassen (Farben, Schriftgröße, Layout) |
| `GPIO_CONFIG.md` | GPIO Pins, Hardware, Fehlersuche |

## Typische Anpassungen

### 1. UI-Farben ändern
**Datei:** `ui/main_screen.py` (oder andere UI-Dateien)
```python
background_color=(0.2, 0.8, 0.2, 1)  # Grün
```
👉 Siehe [CUSTOMIZATION.md](CUSTOMIZATION.md)

### 2. Pumpzeiten einstellen
**Datei:** `config/settings.json`
```json
"pump_start_time": "22:00",
"pump_end_time": "04:00"
```
👉 Oder über UI: ⚙ EINSTELLUNGEN

### 3. GPIO-Pins zuordnen
**Datei:** `src/gpio_handler.py`
```python
self.inputs['BRUNNEN_VOLL'] = DigitalInput(17, ...)  # GPIO 17
```
👉 Siehe [GPIO_CONFIG.md](GPIO_CONFIG.md)

### 4. Steuerungslogik ändern
**Datei:** `src/pump_logic.py`
```python
def calculate_pump_state_automatic(self) -> bool:
    # Hier die Logik anpassen
```

## Feature-Übersicht

✅ **Automatikbetrieb** - Pumpe nach Sensoren & Uhrzeit
✅ **Manualbetrieb** - Manuelle Steuerung mit Buttons
✅ **5 Digitale Eingänge** - Brunnen & IBC Sensoren
✅ **3 Digitale Ausgänge** - Pumpe, Bewässerung, Fehler
✅ **Touch-Screen UI** - 7" Waveshare Display
✅ **Pumpverlauf-Logging** - CSV-Export täglich
✅ **RTC-Modul** - Strom PI Zeitmanagement
✅ **Sleep-Mode** - Energy-Saving nach Timeout
✅ **Fehlererkennung** - Automatische Fehler-Detektion
✅ **Einstellungsmenü** - Uhrzeit, Pumpzeiten

## Wichtige Konzepte

### Ein- und Ausgänge

- **Eingänge (Sensoren)**: Lesen Wasserspiegel
- **Ausgänge (Relais)**: Schalten Pumpe/Ventile
- **Pull-Up Logik**: HIGH = Aktiv (Standardeinstellung)

### Betriebsmodi

1. **Automatikbetrieb**: System macht alles selbst
   - Liest Sensoren
   - Entscheidet ob Pumpe läuft
   - Fehler erkennen

2. **Manualbetrieb**: Benutzer steuert alles
   - Button für Pumpe EIN/AUS
   - Max-Pumpzeit wird eingehalten
   - Brunnen-Leer sperrt Pumpe

### Sleep-Mode

Nach definierten Zeiten fährt das System herunter:
- Nach **10 min Boot** (keine Aktivität)
- Nach **10 min Pump-Stop** (Energie sparen)
- **Aufweckung alle 30 min** für 5 min Sensoren-Check

## Fehlerbehebung Quick-Links

| Problem | Lösung |
|---------|--------|
| App startet nicht | [INSTALLATION.md](INSTALLATION.md#Problembehebung) |
| GPIO-Fehler | [GPIO_CONFIG.md](GPIO_CONFIG.md#Debugging) |
| Display zeigt nichts | [INSTALLATION.md](INSTALLATION.md#Problembehebung) |
| RTC funktioniert nicht | [GPIO_CONFIG.md](GPIO_CONFIG.md#RTC) |
| UI sieht hässlich aus | [CUSTOMIZATION.md](CUSTOMIZATION.md) |

## Logs überprüfen

```bash
# Live-Logging
tail -f logs/app.log

# Pumpvorgänge
cat logs/pump_log_2024-02-01.csv

# Systemd logs (wenn als Service)
sudo journalctl -u pumpensteuerung -f
```

## Häufig ändern

**Diese Dateien werden am häufigsten modifiziert:**

1. `config/settings.json` - Pumpzeiten, Timeouts
2. `ui/main_screen.py` - Farben, Layout
3. `src/pump_logic.py` - Steuerungsregeln
4. `src/gpio_handler.py` - GPIO-Pins (einmalig)

## Support & Fragen

Für spezifische Fragen:
- **UI-Design**: Siehe [CUSTOMIZATION.md](CUSTOMIZATION.md)
- **Hardware-Setup**: Siehe [GPIO_CONFIG.md](GPIO_CONFIG.md)
- **Installation**: Siehe [INSTALLATION.md](INSTALLATION.md)
- **Logik**: Siehe [README.md](README.md#Steuerungslogik)

---

**Version**: 1.0.0
**Erstellt**: Februar 2024
**Python**: 3.7+
**Kivy**: 2.1+

Happy Coding! 🚀
