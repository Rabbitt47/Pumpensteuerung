# Anpassungsanleitung - UI Layout und Design

## Überblick

Das UI-System ist modular aufgebaut, sodass jeder Bildschirm unabhängig angepasst werden kann.

## 1. Farben und Themes

### Farb-Codes (RGB Format 0-1)

```python
# Standardfarben
GRUEN = (0.2, 0.8, 0.2, 1)      # Aktiv/Ja
ROT = (0.8, 0.2, 0.2, 1)        # Aus/Fehler
BLAU = (0.2, 0.2, 0.8, 1)       # Info/Modus
GRAU = (0.5, 0.5, 0.5, 1)       # Standard
DUNKELGRAU = (0.3, 0.3, 0.3, 1) # Hintergrund
HELLGRAU = (0.7, 0.7, 0.7, 1)   # Text-Info
```

### Farben in den UI-Dateien ändern

**Beispiel: main_screen.py**

```python
# Pumpe-Status Button
self.pump_status_button = Button(
    text='PUMPE: AUS',
    background_color=(0.8, 0.2, 0.2, 1),  # ROT ändern zu BLAU
)
```

Ändern Sie einfach die RGB-Werte:

```python
background_color=(0.2, 0.2, 0.8, 1),  # Jetzt Blau
```

## 2. Schriftgrößen anpassen

### Font-Größen (in Scale Points - sp)

```python
# Große Überschrift
font_size='28sp'

# Normale Überschrift
font_size='16sp'

# Standard Text
font_size='14sp'

# Kleine Text
font_size='12sp'
font_size='10sp'
```

**Beispiel ändern:**

```python
# Vorher
self.time_label = Label(text='', font_size='28sp', bold=True)

# Nachher (kleiner)
self.time_label = Label(text='', font_size='20sp', bold=True)
```

## 3. Layout-Struktur

### Box-Layouts (Lineare Anordnung)

```python
# Vertikal (übereinander)
BoxLayout(orientation='vertical', spacing=10)

# Horizontal (nebeneinander)
BoxLayout(orientation='horizontal', spacing=10)

# Größen definieren
BoxLayout(size_hint_y=0.5)  # 50% der Höhe
BoxLayout(size_hint_x=0.3)  # 30% der Breite
```

### Grid-Layouts (Tabellarische Anordnung)

```python
# 2 Spalten
GridLayout(cols=2, spacing=10)

# 3 Spalten
GridLayout(cols=3, spacing=10)

# Mit Größe
GridLayout(cols=2, spacing=5, size_hint_y=0.5)
```

## 4. Button und Label Größen

### Button-Größen ändern

```python
# Kleine Buttons
Button(text='Klein', size_hint_y=0.15)

# Mittlere Buttons
Button(text='Mittel', size_hint_y=0.25)

# Große Buttons
Button(text='Groß', size_hint_y=0.5)
```

### Label-Höhen koordinieren

```python
# Container mit fixem Verhältnis
GridLayout(cols=2, spacing=10)
    Label(text='Label 1', size_hint_y=0.5)
    Label(text='Label 2', size_hint_y=0.5)
```

## 5. Display-Bereich aufteilen

Das Standard-Display ist **1024x600 Pixel**.

### Typisches Layout

```
Header (15%)
├── Uhrzeit | Status
├─────────────────────────────
Content (70%)
├── Linke Seite (50%) | Rechte Seite (50%)
├─────────────────────────────
Footer (15%)
└── Info Text
```

### Im Code

```python
class MyScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Header
        header = BoxLayout(size_hint_y=0.15)
        self.add_widget(header)
        
        # Content
        content = BoxLayout(orientation='horizontal', size_hint_y=0.70)
        left = BoxLayout(size_hint_x=0.5)
        right = BoxLayout(size_hint_x=0.5)
        content.add_widget(left)
        content.add_widget(right)
        self.add_widget(content)
        
        # Footer
        footer = Label(size_hint_y=0.15)
        self.add_widget(footer)
```

## 6. Buttons und Symbole

### Button-Längen einstellen

```python
# Breite anpassen
Button(text='Text', size_hint_x=0.5)  # 50% der Breite
Button(text='Text', size_hint_x=0.3)  # 30% der Breite

# Höhe anpassen
Button(text='Text', size_hint_y=0.2)  # 20% der Höhe
Button(text='Text', size_hint_y=0.5)  # 50% der Höhe
```

### Mit Unicode-Symbolen

```python
Button(text='🟢 PUMPE: AN')
Button(text='🔴 PUMPE: AUS')
Button(text='⚙ EINSTELLUNGEN')
Button(text='📋 PUMPVERLAUF')
Button(text='🎮 MANUALBETRIEB')
Button(text='💾 SPEICHERN')
Button(text='← ZURÜCK')
```

## 7. Farben für Zustände

### Ein/Aus Konvention

```python
# Eingeschaltet/Aktiv
background_color=(0.2, 0.8, 0.2, 1)  # GRÜN

# Ausgeschaltet/Inaktiv
background_color=(0.8, 0.2, 0.2, 1)  # ROT

# Neutral/Info
background_color=(0.2, 0.2, 0.8, 1)  # BLAU

# Fehler
background_color=(1, 0.5, 0, 1)       # ORANGE
```

## 8. Abstand (Spacing) anpassen

```python
# Enger Abstand
spacing=5

# Normaler Abstand
spacing=10

# Großer Abstand
spacing=20

# Padding (innerer Rand)
padding=10
```

## 9. Text-Farben ändern

```python
Label(text='Text', color=(1, 1, 1, 1))      # Weiß
Label(text='Text', color=(0, 0, 0, 1))      # Schwarz
Label(text='Text', color=(0.7, 0.7, 0.7, 1))  # Grau
```

## 10. Praktische Beispiele

### Hauptmenü anpassen

**Datei:** `ui/main_screen.py`

#### Beispiel 1: Button größer machen

```python
# Vorher
settings_btn = Button(
    text='⚙ EINSTELLUNGEN',
    size_hint_y=0.2,
    font_size='14sp'
)

# Nachher (größer)
settings_btn = Button(
    text='⚙ EINSTELLUNGEN',
    size_hint_y=0.3,  # 30% statt 20%
    font_size='18sp'  # Größerer Text
)
```

#### Beispiel 2: Pump-Status Farben

```python
# Vorher
if status['pump_on']:
    self.pump_status_button.background_color = (0.2, 0.8, 0.2, 1)

# Nachher mit Blau-Ton
if status['pump_on']:
    self.pump_status_button.background_color = (0.2, 0.5, 0.9, 1)
```

#### Beispiel 3: Header-Layout ändern

```python
# Alle Elemente in eine Reihe
header = BoxLayout(orientation='horizontal', spacing=20)  # Horizontal statt vertikal
self.time_label = Label(text='', font_size='28sp', bold=True, size_hint_x=0.4)
self.status_label = Label(text='Status', font_size='16sp', size_hint_x=0.6)
header.add_widget(self.time_label)
header.add_widget(self.status_label)
```

### Einstellungen-Bildschirm anpassen

**Datei:** `ui/settings_screen.py`

#### Beispiel: Eingabe-Felder größer machen

```python
# Vorher
self.start_hour = Spinner(
    text=str(...),
    values=[...],
    size_hint_x=0.25
)

# Nachher
self.start_hour = Spinner(
    text=str(...),
    values=[...],
    size_hint_x=0.4  # Breiter
)
```

## 11. Neue Bildschirme erstellen

### Template

```python
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class NewScreen(BoxLayout):
    """Neue Bildschirm-Klasse"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Header
        header = Label(
            text='NEUER BILDSCHIRM',
            font_size='24sp',
            bold=True,
            size_hint_y=0.1
        )
        self.add_widget(header)
        
        # Content
        content = BoxLayout(size_hint_y=0.8)
        # Inhalte hinzufügen...
        self.add_widget(content)
        
        # Footer
        footer = Label(text='Info', size_hint_y=0.1)
        self.add_widget(footer)
```

## 12. Responsive Design Tips

### Für verschiedene Bildschirmgrößen

```python
# 7" Display (1024x600)
Window.size = (1024, 600)

# 5" Display (800x480)
Window.size = (800, 480)

# 10" Display (1280x800)
Window.size = (1280, 800)
```

In `main_new.py` oben die Größe anpassen:

```python
from kivy.core.window import Window
Window.size = (1024, 600)  # Hier ändern
```

## Zusammenfassung der wichtigsten Anpassungen

| Was | Wie | Datei |
|-----|-----|-------|
| Farben | `background_color = (R, G, B, 1)` | `ui/*.py` |
| Schriftgröße | `font_size='16sp'` | `ui/*.py` |
| Button-Größe | `size_hint_y=0.25` | `ui/*.py` |
| Abstand | `spacing=10` | `ui/*.py` |
| Layout | `orientation='vertical'` | `ui/*.py` |
| Display-Größe | `Window.size = (x, y)` | `main_new.py` |

Happy Coding! 🎨
