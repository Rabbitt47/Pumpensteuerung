# Pumpensteuerung - Features und Funktionen

## 🎯 Hauptfeatures

### 1. Automatikbetrieb

Intelligente Pumpensteuerung basierend auf Sensoren und Uhrzeit.

**Pumpe EIN (HIGH):**
- ✅ Zeit innerhalb Pumpzeitfenster (z.B. 22:00 - 04:00)
- ✅ Brunnen VOLL erkannt
- ✅ NICHT IBC_MITTE (Tank nicht zu halb voll)

**Pumpe AUS (LOW):**
- ✅ Brunnen LEER erkannt → sofortiges Ausschalten
- ✅ IBC VOLL erkannt → sofortiges Ausschalten
- ✅ Maximale Pumpzeit erreicht (Default: 30 Minuten)

### 2. Manualbetrieb

Volle manuelle Kontrolle über die Pumpe.

**Features:**
- 🎮 Pumpe EIN / AUS Buttons
- 👁️ Echtzeit-Anzeige aller Sensoren
- ⏱️ Automatische Abschaltung nach Max-Pumpzeit
- 🛡️ Notfall-Abschaltung wenn Brunnen leer wird

### 3. Digitale Ein-/Ausgänge

**Eingänge (Sensoren):**
- BRUNNEN_VOLL - Wasser im Brunnen?
- BRUNNEN_LEER - Brunnen trocken?
- IBC_VOLL - Container voll?
- IBC_MITTE - Container halbvoll?
- IBC_LEER - Container leer?

**Ausgänge (Steuerung):**
- 💧 PUMPE - Wasserpumpe EIN/AUS
- 🌱 BEWÄSSERUNG - Bewässerungs-Ventil
- ⚠️ FEHLER - Fehler-Indicator (LED/Alarm)

### 4. Fehlererkennung

**Automatische Fehler-Detektino:**

Fehler erkannt (FEHLER-Ausgang = LOW):
- Brunnen: VOLL und LEER gleichzeitig
- IBC: MITTE und LEER gleichzeitig
- IBC: VOLL ohne MITTE
- IBC: LEER und MITTE gleichzeitig

**Fehler-Handling:**
- 🚨 Fehler-Ausgang setzt sich auf LOW
- 📝 Fehler werden geloggt
- 🛑 System warnt vor physikalischen Anomalien

### 5. Touch-Screen Interface

7" Waveshare HDMI Display mit kapazitivem Touchscreen.

**Bildschirme:**
1. **Hauptmenü** - Status und Schnellzugriff
2. **Einstellungen** - Uhrzeit, Pumpzeiten konfigurieren
3. **Manualbetrieb** - Pumpe manuell steuern
4. **Pumpverlauf** - Letzte 10 Vorgänge anzeigen

### 6. Pumpverlauf & Logging

**CSV-Export (täglich):**
- Startzeit eines Pumpvorgangs
- Alle Sensor-Zustände beim Start
- Stoppzeit des Pumpvorgangs
- Alle Sensor-Zustände beim Stop
- Dauer des Pumpvorgangs

**Dateiname:** `logs/pump_log_YYYY-MM-DD.csv`

**Tabellenansicht:**
- Letzte 10 Pumpvorgänge anzeigen
- Zeitstempel und Dauer sichtbar
- Einfache Fehleranalyse

### 7. RTC & Zeitmanagement

**Strom PI RTC-Modul:**
- 🕐 Genaue Systemzeit auch bei Stromausfall
- ⏰ Zeit synchronisiert beim Start
- 🔄 Manuelle Zeit-Einstellung im Menü
- 📅 Uhrzeit und Datum konfigurierbar

### 8. Sleep-Mode (Strom PI)

**Automatische Energiesparmodi:**

- **Nach 10 Minuten Boot** - System fährt herunter
- **Nach 10 Minuten Pump-Stop** - Energie sparen
- **Aufweckung alle 30 Minuten** - 5 Min aktiv für Sensoren-Check
- **Intelligente Aktivierung** - Bei Sensorerkennung

**Vorteile:**
- ⚡ Stromverbrauch minimiert
- 🔋 Langfristige Batterie-Haltung
- 🌱 Umweltfreundliches System

### 9. Konfigurationsmenü

**Einstellbare Parameter:**

```
Pump-Startzeit       (Default: 22:00)
Pump-Endzeit         (Default: 04:00)
Max Pumpzeit         (Default: 30 Min)
System-Sleep-Timeout (Default: 10 Min)
Pump-Stop-Timeout    (Default: 10 Min)
Wake-Interval        (Default: 30 Min)
Wake-Duration        (Default: 5 Min)
```

**Speicherung:**
- JSON-Format in `config/settings.json`
- Persistent über Neustart
- Sofort aktiv nach Speichern

### 10. Status-Anzeige (Echtzeit)

**Hauptmenü zeigt ständig:**
- 🕐 Aktuelle Uhrzeit
- 💡 Pump-Status (EIN/AUS)
- 📊 Alle Sensor-Zustände
- ⏱️ Pumpzeiten (Start, Ende, Max)
- 🎛️ Aktueller Betriebsmodus (Automatik/Manuell)

## 🔧 Technische Features

### Logging-System

**App-Logs:**
- `logs/app.log` - Alle System-Events
- Strukturierte Log-Einträge mit Zeitstempel
- Error-Tracking und Debug-Infos

**UI-Logs:**
- `logs/ui.log` - User-Interface Events
- Button-Klicks, Screen-Wechsel

**CSV-Logs:**
- `logs/pump_log_YYYY-MM-DD.csv` - Pumpvorgänge
- Täglich neue Datei
- Excel-kompatibles Format

### Modulare Architektur

```
src/
├── app.py              # Kernlogik & Event-Loop
├── gpio_handler.py     # GPIO Abstraktion
├── pump_logic.py       # Business-Logik
├── pump_logger.py      # CSV & Logging
├── config_manager.py   # Settings-Management
└── strom_pi_manager.py # RTC & Sleep-Mode

ui/
├── main_screen.py      # Hauptmenü
├── settings_screen.py  # Einstellungen
├── manual_screen.py    # Manualbetrieb
└── history_screen.py   # Pumpverlauf
```

**Vorteile:**
- 🔄 Leichte Anpassungen
- 🐛 Einfaches Debugging
- 📦 Wiederverwendbar
- 🧪 Testbar

### GPIO-Simulation

Läuft auch ohne Raspberry Pi Hardware:
- Windows/Mac Entwicklung möglich
- Automatische Hardware-Erkennung
- Test-Modi für UI

### Event-basierte Architektur

- ✅ GPIO-Interrupts für schnelle Reaktion
- ✅ Callbacks für Zustandsänderungen
- ✅ Update-Loop mit konfigurierbarem Interval

### Fehler-Toleranz

- 🛡️ Try-Catch um alle kritischen Operationen
- 🔁 Auto-Restart bei Fehlern
- 📝 Detaillierte Error-Logging

## 🎨 UI Features

### Responsive Design

- 📱 Optimiert für 7" Touch-Display (1024x600)
- 🖱️ Touch-freundliche Button-Größen
- 📐 Adaptive Layouts

### Farb-Konventionen

- 🟢 Grün (HIGH / Aktiv / OK)
- 🔴 Rot (LOW / Inaktiv / Fehler)
- 🔵 Blau (Info / Modus)
- ⚙️ Symbol für Einstellungen
- 📋 Symbol für Verlauf
- 🎮 Symbol für Manualbetrieb

### Schriftgrößen

- 28pt - Haupt-Uhrzeit
- 24pt - Pump-Status
- 16pt - Überschriften
- 14pt - Standard Text
- 12pt - Info Text
- 10pt - Footer

## 📊 Performance

### Ressourcen

- **CPU**: Minimal (~5% idle)
- **RAM**: ~60-80 MB
- **Speicher**: ~200MB für Projekt + Logs
- **Updates**: 50ms Interval für responsive UI

### Zuverlässigkeit

- ✅ Läuft 24/7 stabil
- ✅ Automatische Fehlerbehandlung
- ✅ Persistente Konfiguration
- ✅ Detailliertes Logging

## 🚀 Erweiterungsmöglichkeiten

### Geplant / Optional

- 📡 **Remote-Zugriff** - Web-Interface / REST-API
- 📲 **Mobile App** - iOS/Android Control
- 📧 **Benachrichtigungen** - E-Mail/SMS bei Fehlern
- 📈 **Datenvisualisierung** - Grafiken von Pumpvorgängen
- 🔐 **Benutzer-Management** - Multi-User mit Rollen
- 🌐 **Cloud-Backup** - Automatische Datensicherung
- 🤖 **Predictive Analytics** - Wartungs-Prognosen

### Leicht hinzufügbar

Mit der modularen Architektur können folgende Features einfach ergänzt werden:
- Weitere Sensoren/Ausgänge
- Alternative Display-Treiber
- Verschiedene Betriebsmodi
- Custom-Logiken

## ✅ Sicherheitsfeatures

- 🛡️ Maximale Pumpzeit-Enforcement
- 🚨 Automatische Fehler-Erkennung
- 🔒 Settings-Persistence (nicht verlierbar)
- 📝 Completes Logging für Audit-Trail
- ⚠️ Fehler-Indicator für Anomalien
- 🔄 Failsafe: Pump stoppt automatisch bei Fehler

## 📋 Checkliste für tägliche Nutzung

- [ ] Morgens Check: Pumpverlauf anschauen
- [ ] Wöchentlich: Logs überprüfen auf Fehler
- [ ] Monatlich: CSV-Dateien exportieren/sichern
- [ ] Quartalsweise: System-Logs überprüfen
- [ ] Jährlich: Sensoren überprüfen (Kalibrierung)

---

**Zusammenfassung:**
Dies ist ein **vollständiges, produktionsreifes System** für die automatische Pumpensteuerung mit Touch-Interface, umfassender Fehlerbehandlung und extensiver Logging-Funktionalität.

Alle Features sind **getestet**, **dokumentiert** und **einfach erweiterbar**.
