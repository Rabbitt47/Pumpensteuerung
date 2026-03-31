# Version 4 - USB-Stick Logging & Monatliche Archivierung

## Was ist neu?

### 🔄 Monatliche CSV-Dateien (statt täglich)
- **Vorher:** Neue CSV-Datei täglich → weniger Schreibvorgänge auf SD-Karte
- **Nachher:** Eine CSV pro Monat (z.B. `pump_log_2026-03.csv`)
- **Vorteil:** Weniger Verschleiß der SD-Karte, übersichtlichere Dateistruktur

### 💾 USB-Stick Unterstützung
- **Automatische Erkennung** von USB-Sticks auf dem Raspberry Pi
- **CVS-Dateien landen auf dem USB-Stick** → keine speicherkarte ausbau nötig!
- **Fallback auf SD-Karte** wenn kein USB-Stick verfügbar

### 📊 Verbesserte Log-Struktur

Die CSV-Einträge enthalten jetzt auch:
- **Datum** (YYYY-MM-DD) - ermöglicht das Filtern über Monatsgrenzen hinweg
- Alle bisherigen Daten (Zeiten, Sensoren, Dauern)

**Beispiel CSV-Zeile:**
```
2026-03-15;14:32:10;L;L;H;L;L;H;L;14:42:15;L;L;H;L;L;H;L;10.08
```

---

## Installation auf Raspberry Pi

### 1. Repository clonen
```bash
cd /home/pi
git clone https://github.com/Rabbitt47/Pumpensteuerung.git
cd Pumpensteuerung/V4
```

### 2. USB-Stick vorbereiten (Windows)
1. USB-Stick an Computer anschließen
2. Formatieren als **FAT32**
3. **Nichts löschen** - die App erstellt selbst die Struktur

### 3. USB-Stick am Raspberry verbinden
- Einen der USB-Slots des Raspberry Pi nutzen
- Automatisch erkannt beim Programmstart ✓

### 4. Dependencies installieren
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install RPi.GPIO kivy
```

### 5. Programm starten
```bash
python3 main_new.py
```

---

## Speicherorte

### Mit USB-Stick (empfohlen)
```
/media/pi/<usb-name>/pumpensteuerung/
├── pump_log_2026-03.csv
├── pump_log_2026-04.csv
└── pump_log_2026-05.csv
```

### Ohne USB-Stick (Fallback)
```
/home/pi/Pumpensteuerung/V4/logs/
├── pump_log_2026-03.csv
├── pump_log_2026-04.csv
└── pump_log_2026-05.csv
```

---

## Neue Features

### Logging-Status in UI
Das Programm zeigt an:
- ✓ USB-Stick erkannt oder ⚠ Fallback auf lokales Speichern
- Aktuelles Speicherverzeichnis
- Anzahl der Log-Dateien und Einträge

### Automatische USB-Erkennung
Sucht in diesen Pfaden:
- `/media/pi/*` (Standard Raspberry Pi)
- `/mnt/*` (alternative Linux-Mounts)
- `/media/*` (generische Linux-Mounts)

### Robuste Fehlerbehandlung
- Wenn USB-Stick entfernt wird → automatischer Fallback auf SD-Karte
- Wenn USB-Stick wieder angesteckt wird → nächste Datei wird dort erstellt
- Keine Datenverluste!

---

## CSV-Export (für Excel/LibreOffice)

Die CSV-Dateien können direkt in Excel geöffnet werden:

1. USB-Stick an Computer anschließen
2. CSV-Datei öffnen mit Excel
3. **Trennzeichen:** Semikolon (`;`)
4. **Kodierung:** UTF-8

**Spalten:**
- Datum
- Startzeit
- Sensoren Start (BRUNNEN_VOLL, BRUNNEN_LEER, IBC_VOLL, IBC_MITTE, IBC_LEER, PUMPE, BEWAESSERUNG)
- Stoppzeit
- Sensoren Stop (wie oben)
- Dauer in Minuten

---

## Tipps & Tricks

### USB-Stick wechseln
1. Im Menü: Settings → Log-Status überprüfen
2. USB-Stick abziehen → Fallback auf SD-Karte
3. Neuen USB-Stick anstecken
4. Nächster Eintrag wird auf dem neuen Stick gespeichert

### Historische Daten ansehen
1. Im App-Menü: **History Screen**
2. Zeigt alle Pumpvorgänge des aktuellen Monats
3. Statistiken: Anzahl Zyklen, Gesamtlaufzeit

### Problembehebung
**Q: USB-Stick wird nicht erkannt**
- A: Überprüfen Sie mit `lsblk` und `mount` am Raspberry Pi
- A: USB-Stick muss formatiert sein (FAT32 empfohlen)
- A: Überprüfen Sie die Berechtigungen (`chmod 777`)

**Q: Logs landen nicht auf dem USB-Stick**
- A: Überprüfen Sie mit `df -h` ob der Stick gemountet ist
- A: Starten Sie das Programm neu
- A: Schauen Sie in `logs/ui.log` für Fehler

---

## Changelog: V3 → V4

| Feature | V3 | V4 |
|---------|-----|-----|
| Tägliche CSV-Dateien | ✓ | ✗ |
| Monatliche CSV-Dateien | ✗ | ✓ |
| USB-Stick Unterstützung | ✗ | ✓ |
| Automatische Erkennung | ✗ | ✓ |
| Datum in CSV | ✗ | ✓ |
| Fallback auf SD-Karte | ✗ | ✓ |

---

**Feedback?** Öffnen Sie ein Issue auf GitHub: 
https://github.com/Rabbitt47/Pumpensteuerung/issues
