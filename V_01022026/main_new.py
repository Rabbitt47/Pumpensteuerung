#!/usr/bin/env python3
"""
Pumpensteuerung - Pump Control System für Raspberry Pi

Hardware: Strom PI, Waveshare 7-Zoll-LCD, DS3231 RTC
Eingänge: BRUNNEN_VOLL (HIGH), BRUNNEN_LEER (LOW), IBC_VOLL (HIGH), IBC_MITTE, IBC_LEER (LOW)
Ausgänge: Pumpe, Bewässerung, Fehler

Neue Architektur mit Kivy für Touch-Interface (1024x600)
"""

import logging
import sys
from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window

# Fenster-Größe für 7" Display
Window.size = (1024, 600)

from src.app import PumpControlApplication
from ui.main_screen import MainMenuScreen
from ui.settings_screen import SettingsScreen
from ui.manual_screen import ManualScreen
from ui.history_screen import HistoryScreen


# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ui.log'),
        logging.StreamHandler()
    ]
)


class PumpControlApp(App):
    """Hauptanwendungs-Klasse für Pumpensteuerung"""
    
    title = "Pumpensteuerung - Raspberry Pi"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pump_app = PumpControlApplication()
        self.screen_manager = None
    
    def build(self):
        """Erstellt die UI"""
        logging.info("=" * 50)
        logging.info("Starte Pumpensteuerungs-App")
        logging.info("=" * 50)
        
        # Screen Manager für Menü-Navigation
        self.screen_manager = ScreenManager()
        
        # Erstelle alle Screens
        main_screen = MainMenuScreen(self.pump_app)
        settings_screen = SettingsScreen(self.pump_app)
        manual_screen = ManualScreen(self.pump_app)
        history_screen = HistoryScreen(self.pump_app)
        
        # Erstelle Container-Screens
        main_container = Screen(name='main')
        main_container.add_widget(main_screen)
        
        settings_container = Screen(name='settings')
        settings_container.add_widget(settings_screen)
        
        manual_container = Screen(name='manual')
        manual_container.add_widget(manual_screen)
        
        history_container = Screen(name='history')
        history_container.add_widget(history_screen)
        
        # Füge Screens dem Manager hinzu
        self.screen_manager.add_widget(main_container)
        self.screen_manager.add_widget(settings_container)
        self.screen_manager.add_widget(manual_container)
        self.screen_manager.add_widget(history_container)
        
        # Update Loop starten (50ms für responsive UI)
        Clock.schedule_interval(self.update_logic, 0.05)
        
        logging.info("UI erfolgreich initialisiert")
        return self.screen_manager
    
    def update_logic(self, dt):
        """Update Loop für Pumpenlogik"""
        try:
            self.pump_app.update()
        except Exception as e:
            logging.error(f"Fehler in Update Loop: {e}")
    
    def on_stop(self):
        """Wird aufgerufen wenn App beendet wird"""
        logging.info("Fahre Anwendung herunter...")
        self.pump_app.cleanup()
        return True
    
    # Delegierte Methoden für einfachere UI-Zugriffe
    @property
    def gpio(self):
        return self.pump_app.gpio
    
    @property
    def pump_controller(self):
        return self.pump_app.pump_controller
    
    @property
    def config(self):
        return self.pump_app.config
    
    @property
    def pump_logger(self):
        return self.pump_app.pump_logger
    
    def get_status(self):
        return self.pump_app.get_status()


def main():
    """Einstiegspunkt der Anwendung"""
    try:
        app = PumpControlApp()
        app.run()
    except KeyboardInterrupt:
        logging.info("Anwendung durch Benutzer beendet")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Kritischer Fehler: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
