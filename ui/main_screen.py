"""
Kivy-basierte Benutzeroberfläche für Touch-Display
Waveshare 7" LCD mit kapazitivem Touchscreen (1024x600)
"""
import logging
from datetime import datetime, time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle


# Fenster-Größe für 7" Display
Window.size = (1024, 600)


class ColoredButton(Button):
    """Button mit konfigurierbaren Farben"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(state=self.on_state)
    
    def on_state(self, widget, value):
        """Ändert Farbe basierend auf Zustand"""
        if value == 'down':
            self.background_color = (0.2, 0.6, 0.2, 1)  # Grün
        else:
            self.background_color = (0.5, 0.5, 0.5, 1)  # Grau


class MainMenuScreen(BoxLayout):
    """Hauptmenü-Bildschirm"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Header mit Uhrzeit und Status
        header = BoxLayout(size_hint_y=0.15, spacing=10)
        self.time_label = Label(text='', font_size='28sp', bold=True)
        self.status_label = Label(text='Status: Automatik', font_size='14sp')
        header.add_widget(self.time_label)
        header.add_widget(self.status_label)
        self.add_widget(header)
        
        # Hauptbereich mit Inhalten
        content = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.70)
        
        # Linke Seite: Pump-Status und Zeiten
        left_panel = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)
        
        # Pump-Status anzeige
        pump_status = BoxLayout(orientation='vertical', spacing=5)
        pump_label = Label(text='PUMPEN-STATUS', font_size='16sp', bold=True, size_hint_y=0.2)
        self.pump_status_button = Button(
            text='PUMPE: AUS',
            font_size='24sp',
            background_color=(0.8, 0.2, 0.2, 1),  # Rot
            size_hint_y=0.8
        )
        pump_status.add_widget(pump_label)
        pump_status.add_widget(self.pump_status_button)
        left_panel.add_widget(pump_status)
        
        # Digitale Ein-/Ausgänge Anzeige
        io_section = BoxLayout(orientation='vertical', spacing=5)
        io_label = Label(text='E/A ZUSTÄNDE', font_size='14sp', bold=True, size_hint_y=0.2)
        self.io_grid = GridLayout(cols=2, spacing=5, size_hint_y=0.8)
        io_section.add_widget(io_label)
        io_section.add_widget(self.io_grid)
        left_panel.add_widget(io_section)
        
        content.add_widget(left_panel)
        
        # Rechte Seite: Zeiten und Buttons
        right_panel = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)
        
        # Pumpzeiten anzeige
        times_box = BoxLayout(orientation='vertical', spacing=5)
        times_title = Label(text='PUMPZEITEN', font_size='14sp', bold=True, size_hint_y=0.15)
        self.start_time_label = Label(text='Start: 22:00', font_size='12sp', size_hint_y=0.25)
        self.end_time_label = Label(text='Ende: 04:00', font_size='12sp', size_hint_y=0.25)
        max_time = Label(
            text=f'Max: {self.app.pump_controller.max_pump_duration}min',
            font_size='12sp',
            size_hint_y=0.25
        )
        times_box.add_widget(times_title)
        times_box.add_widget(self.start_time_label)
        times_box.add_widget(self.end_time_label)
        times_box.add_widget(max_time)
        right_panel.add_widget(times_box)
        
        # Buttons für Menüs und Betriebsmodi
        button_grid = GridLayout(cols=1, spacing=10, size_hint_y=0.85)
        
        # Automatik/Manuell Toggle
        self.mode_button = ToggleButton(
            text='Modus: AUTOMATIK',
            size_hint_y=0.2,
            background_color=(0.2, 0.2, 0.8, 1),
            font_size='14sp'
        )
        self.mode_button.bind(on_press=self.toggle_mode)
        button_grid.add_widget(self.mode_button)
        
        # Einstellungen Button
        settings_btn = Button(
            text='⚙ EINSTELLUNGEN',
            size_hint_y=0.2,
            font_size='14sp'
        )
        settings_btn.bind(on_press=self.show_settings)
        button_grid.add_widget(settings_btn)
        
        # Verlauf Button
        history_btn = Button(
            text='📋 PUMPVERLAUF',
            size_hint_y=0.2,
            font_size='14sp'
        )
        history_btn.bind(on_press=self.show_history)
        button_grid.add_widget(history_btn)
        
        # Manualbetrieb Button
        manual_btn = Button(
            text='🎮 MANUALBETRIEB',
            size_hint_y=0.2,
            font_size='14sp'
        )
        manual_btn.bind(on_press=self.show_manual)
        button_grid.add_widget(manual_btn)
        
        right_panel.add_widget(button_grid)
        content.add_widget(right_panel)
        
        self.add_widget(content)
        
        # Footer mit Info
        footer = Label(
            text='Touch-Bildschirm | Raspberry Pi Pumpensteuerung',
            font_size='10sp',
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(footer)
        
        # Update-Timer starten
        Clock.schedule_interval(self.update_display, 0.5)
    
    def update_display(self, dt=None):
        """Aktualisiert die Anzeige mit aktuellen Daten"""
        status = self.app.get_status()
        
        # Zeit aktualisieren
        self.time_label.text = status['timestamp'].strftime('%H:%M:%S')
        
        # Pump-Status aktualisieren
        if status['pump_on']:
            self.pump_status_button.text = '🟢 PUMPE: AN'
            self.pump_status_button.background_color = (0.2, 0.8, 0.2, 1)  # Grün
        else:
            self.pump_status_button.text = '🔴 PUMPE: AUS'
            self.pump_status_button.background_color = (0.8, 0.2, 0.2, 1)  # Rot
        
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
        
        # Status-Text aktualisieren
        mode_text = 'Automatik' if status['is_automatic'] else 'Manuell'
        self.status_label.text = f'Status: {mode_text} | Zeitfenster: {"Ja" if status["within_pump_hours"] else "Nein"}'
    
    def toggle_mode(self, widget):
        """Wechselt zwischen Automatik und Manualbetrieb"""
        self.app.pump_controller.is_automatic = not self.app.pump_controller.is_automatic
        
        if self.app.pump_controller.is_automatic:
            self.mode_button.text = 'Modus: AUTOMATIK'
            # Pumpe ausschalten beim Wechsel zu Automatik
            self.app.gpio.get_output('PUMPE').set_low()
        else:
            self.mode_button.text = 'Modus: MANUELL'
            # Pumpe ausschalten beim Wechsel zu Manuell
            self.app.gpio.get_output('PUMPE').set_low()
    
    def show_settings(self, widget):
        """Öffnet Einstellungs-Dialog"""
        self.app.root.current = 'settings'
    
    def show_history(self, widget):
        """Öffnet Pumpverlauf-Dialog"""
        self.app.root.current = 'history'
    
    def show_manual(self, widget):
        """Öffnet Manualbetrieb-Dialog"""
        self.app.root.current = 'manual'
