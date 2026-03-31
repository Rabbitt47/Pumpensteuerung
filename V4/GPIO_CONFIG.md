# GPIO Konfiguration und Anpassung

## GPIO Pin-Belegung

### Aktuelle Konfiguration

Die Standard-Pin-Zuweisungen sind in `src/gpio_handler.py` definiert:

```python
# EINGÄNGE (Sensoren)
self.inputs['BRUNNEN_VOLL'] = DigitalInput(17, 'BRUNNEN_VOLL')
self.inputs['BRUNNEN_LEER'] = DigitalInput(27, 'BRUNNEN_LEER')
self.inputs['IBC_VOLL'] = DigitalInput(22, 'IBC_VOLL')
self.inputs['IBC_MITTE'] = DigitalInput(23, 'IBC_MITTE')
self.inputs['IBC_LEER'] = DigitalInput(24, 'IBC_LEER')

# AUSGÄNGE (Relais/Ventile)
self.outputs['PUMPE'] = DigitalOutput(18, 'PUMPE')
self.outputs['BEWAESSERUNG'] = DigitalOutput(25, 'BEWAESSERUNG')
self.outputs['FEHLER'] = DigitalOutput(16, 'FEHLER')
```

## GPIO-Pins ändern

### Schritt 1: Raspberry Pi GPIO-Anschlüsse identifizieren

```bash
# PIN-Layout auf Raspberry Pi anzeigen
pinout
```

### Schritt 2: Pins in gpio_handler.py anpassen

**Datei:** `src/gpio_handler.py`

```python
class GPIOManager:
    def __init__(self):
        self.inputs: Dict[str, DigitalInput] = {}
        self.outputs: Dict[str, DigitalOutput] = {}
        
        # Beispiel: Neue PIN-Belegung
        self.inputs['BRUNNEN_VOLL'] = DigitalInput(4, 'BRUNNEN_VOLL')  # GPIO 4 statt 17
        self.inputs['BRUNNEN_LEER'] = DigitalInput(5, 'BRUNNEN_LEER')  # GPIO 5 statt 27
        # ... weitere Pins ...
```

### Schritt 3: Logik testen

```bash
python3 -c "from src.gpio_handler import GPIOManager; gm = GPIOManager(); print(gm.inputs)"
```

## Neue Ein-/Ausgänge hinzufügen

### Neuen Eingang hinzufügen

**In `src/gpio_handler.py`:**

```python
class GPIOManager:
    def __init__(self):
        # ... bestehende Eingänge ...
        
        # Neuer Eingang
        self.inputs['PUMPEN_FEHLER'] = DigitalInput(26, 'PUMPEN_FEHLER')
```

**In `src/pump_logic.py` - Logik hinzufügen:**

```python
def check_error_condition(self) -> bool:
    # ... bestehender Code ...
    
    # Neuer Fehler-Check
    pumpen_fehler = self.gpio.get_input('PUMPEN_FEHLER').is_high()
    if pumpen_fehler:
        error = True
        logging.warning("FEHLER: Pump-Fehler erkannt!")
    
    return error
```

**In UI - E/A Anzeige hinzufügen:**

**Datei:** `ui/main_screen.py`

```python
def update_display(self, dt=None):
    # ... bestehender Code ...
    
    # E/A-Zustände aktualisieren
    self.io_grid.clear_widgets()
    for name, state in status['input_states'].items():
        color = (0.2, 0.8, 0.2, 1) if state else (0.8, 0.2, 0.2, 1)
        label = Label(text=f'{name}:', size_hint_y=0.5)
        state_btn = Button(
            text='HIGH' if state else 'LOW',
            size_hint_y=0.5,
            background_color=color
        )
        self.io_grid.add_widget(label)
        self.io_grid.add_widget(state_btn)
```

### Neuen Ausgang hinzufügen

**In `src/gpio_handler.py`:**

```python
class GPIOManager:
    def __init__(self):
        # ... bestehende Ausgänge ...
        
        # Neuer Ausgang
        self.outputs['ALARM'] = DigitalOutput(19, 'ALARM')
```

**In `src/pump_logic.py` - Aktivierung hinzufügen:**

```python
def update_error_output(self):
    # Fehler-Logik
    if self.check_error_condition():
        self.gpio.get_output('FEHLER').set_low()
        self.gpio.get_output('ALARM').set_high()  # Alarm aktivieren
    else:
        self.gpio.get_output('FEHLER').set_high()
        self.gpio.get_output('ALARM').set_low()   # Alarm deaktivieren
```

## GPIO-Modi (Pull-Up / Pull-Down)

### Pull-Up Eingänge (Standard)

```python
# Schalter mit Pull-Up (aktiv LOW, passiv HIGH)
self.inputs['SENSOR'] = DigitalInput(17, 'SENSOR', pull_up=True)
```

### Pull-Down Eingänge

```python
# Schalter mit Pull-Down (aktiv HIGH, passiv LOW)
self.inputs['SENSOR'] = DigitalInput(17, 'SENSOR', pull_up=False)
```

## Testen der GPIO-Verbindungen

### Schritt-für-Schritt Test

1. **Alle Eingänge testen:**

```python
from src.gpio_handler import GPIOManager

gpio = GPIOManager()

# Eingänge lesen
print("Eingänge:")
for name, inp in gpio.inputs.items():
    print(f"{name}: {inp.read()}")
```

2. **Alle Ausgänge testen:**

```python
# Ausgänge nacheinander testen
for name, out in gpio.outputs.items():
    print(f"Teste {name}...")
    out.set_high()
    time.sleep(0.5)
    out.set_low()
    time.sleep(0.5)
```

3. **Callback-Test:**

```python
def on_input_change(name, state):
    print(f"{name} geändert: {'HIGH' if state else 'LOW'}")

gpio.get_input('BRUNNEN_VOLL').add_callback(on_input_change)
# Sensor manuell betätigen und Ausgabe beobachten
```

## Sicherheit

### Logik zur Fehlerdetektino

```python
# WICHTIG: Fehler müssen sofort erkannt werden
def check_error_condition(self) -> bool:
    # ... Fehler-Bedingungen prüfen ...
    
    # Sicherheits-Timeout: Pumpe nicht länger als max_pump_duration
    if pump.is_high() and self.pump_start_datetime:
        duration = (datetime.now() - self.pump_start_datetime).total_seconds() / 60
        if duration > self.max_pump_duration:
            pump.set_low()
            return True  # Fehler: Timeout
    
    return False
```

### Notfall-Abschaltung

Die Pumpe wird automatisch abgeschaltet bei:
1. Brunnen leer
2. IBC voll
3. Fehler erkannt
4. Maximale Pumpzeit überschritten

## Debugging GPIO-Probleme

### Kein Signal auf Input

```bash
# GPIO-Status überprüfen
gpioinfo 17  # GPIO 17 überprüfen

# Spannungsprüfung mit Multimeter
# Sollte 3.3V sein wenn HIGH
# Sollte 0V sein wenn LOW
```

### Ausgang funktioniert nicht

```python
# Test mit direktem GPIO-Befehl
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)  # LED sollte leuchten
GPIO.output(18, GPIO.LOW)   # LED sollte erlöschen
GPIO.cleanup()
```

### Event-Erkennung funktioniert nicht

```python
# Callbacks überprüfen
inp = gpio.get_input('BRUNNEN_VOLL')
print(f"Callbacks registriert: {len(inp.callbacks)}")

# Manually read state
state = inp.read()
print(f"Zustand: {state}")
```

## Simulation vs. Real Hardware

### Automatische Erkennung

In `src/gpio_handler.py`:

```python
try:
    import RPi.GPIO as GPIO
    ON_RASPBERRY = True
except (ImportError, RuntimeError):
    ON_RASPBERRY = False
    logging.warning("RPi.GPIO nicht verfügbar - Simulation Modus")
```

### Manueller Modus

Zum Testen auf Windows/Linux ohne Raspberry Pi:

```python
# In src/gpio_handler.py
ON_RASPBERRY = False  # Erzwinge Simulation
```

### Simulation testen

```python
# Während Simulation
gpio = GPIOManager()

# Werte direkt setzen
gpio.get_input('BRUNNEN_VOLL').state = True
gpio.get_output('PUMPE').set_high()

# App sollte normal funktionieren
```

## Best Practices

1. **Immer Pull-up für Schalter verwenden** (sicherer gegen Fehler)
2. **Fehler-Detektino aktiv halten** (Sicherheit)
3. **Maximale Pumpzeit definieren** (verhindert Schäden)
4. **Regelmäßig Logs überprüfen** (frühzeitige Fehler-Erkennung)
5. **Ausgänge mit Relais schützen** (RPi nur bis 16mA)

## GPIO-Sicherheit

### Spannungsschutz

```
Raspberry Pi GPIO: 3.3V / max 16mA pro Pin
Relais benötigen: 5V / 50-100mA typisch

MUSS Optokoppler oder Relais-Modul verwenden!
```

### Verdrahtung

```
Eingänge (Sensoren):
  + → 3.3V
  - → GND
  Signal → GPIO mit Pull-Up

Ausgänge (Relais):
  MUSS über Relais-Modul/Optokoppler
  GPIO Signal → Opto/Relais → 5V Stromversorgung
  Pumpe/Ventil → Relais-Kontakte
```

## Spezifische Sensoren

### Digitale Schalter (Float-Schalter)

```python
# Float-Schalter: Normally Open (NO)
input = DigitalInput(17, 'SCHALTER', pull_up=True)
# Logik: HIGH = Schalter offen (Wasser da)
```

### Capacitive Level Sensors

```python
# Kapazitive Sensoren: Analog über Komparator
input = DigitalInput(17, 'CAPACITIVE', pull_up=True)
# Logik: HIGH = Objekt erkannt
```

### Optische Sensoren

```python
# Optische Sensoren: Aktiv
input = DigitalInput(17, 'OPTICAL', pull_up=False)
# Logik: HIGH = Licht erkannt
```

Alle verwenden die gleiche `DigitalInput` Klasse - nur die Pull-up Einstellung anpassen!
