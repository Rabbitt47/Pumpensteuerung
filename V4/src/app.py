"""
Hauptanwendung und Event-Loop
"""
import logging
import time
from datetime import datetime

from src.gpio_handler import GPIOManager
from src.pump_logic import PumpController
from src.config_manager import ConfigManager
from src.pump_logger import PumpLogger
from src.strom_pi_manager import StromPIManager


# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)


class PumpControlApplication:
    """Hauptanwendung für Pumpensteuerung"""
    
    def __init__(self):
        self.config = ConfigManager('config/settings.json')
        self.gpio = GPIOManager()
        self.pump_controller = PumpController(self.gpio)
        self.pump_logger = PumpLogger('logs')
        self.strom_pi = StromPIManager(self.config)
        
        # UI-Verweis wird später gesetzt
        self.ui = None
        
        # Übernahme der Konfiguration
        self.pump_controller.pump_start_time = self.config.get_pump_start_time()
        self.pump_controller.pump_end_time = self.config.get_pump_end_time()
        self.pump_controller.max_pump_duration = self.config.get('max_pump_duration', 30)
        
        logging.info("Pumpensteuerung gestartet")
    
    def set_ui(self, ui):
        """Setzt UI-Referenz für Updates"""
        self.ui = ui
    
    def on_pump_state_changed(self):
        """Wird aufgerufen wenn sich Pumpenstatus ändert"""
        pump_on = self.gpio.get_output('PUMPE').is_high()
        
        if pump_on:
            input_states = self.gpio.get_all_input_states()
            output_states = self.gpio.get_all_output_states()
            self.pump_logger.start_pump(input_states, output_states)
        else:
            input_states = self.gpio.get_all_input_states()
            output_states = self.gpio.get_all_output_states()
            self.pump_logger.stop_pump(input_states, output_states)
        
        # UI aktualisieren
        if self.ui:
            self.ui.update_display()
    
    def update(self):
        """Aktualisiert Steuerungslogik"""
        # Speichere alten Zustand
        old_pump_state = self.gpio.get_output('PUMPE').is_high()
        
        # Aktualisiere Logik
        self.pump_controller.update()
        
        # Prüfe ob sich Pumpe geändert hat
        new_pump_state = self.gpio.get_output('PUMPE').is_high()
        if old_pump_state != new_pump_state:
            self.on_pump_state_changed()
        
        # UI aktualisieren
        if self.ui:
            self.ui.update_display()
    
    def get_status(self) -> dict:
        """Gibt aktuellen Status zurück"""
        pump = self.gpio.get_output('PUMPE')
        return {
            'timestamp': datetime.now(),
            'is_automatic': self.pump_controller.is_automatic,
            'pump_on': pump.is_high(),
            'pump_start_time': self.pump_controller.pump_start_time,
            'pump_end_time': self.pump_controller.pump_end_time,
            'max_pump_duration': self.pump_controller.max_pump_duration,
            'input_states': self.gpio.get_all_input_states(),
            'output_states': self.gpio.get_all_output_states(),
            'within_pump_hours': self.pump_controller.is_within_pump_hours(),
        }
    
    def cleanup(self):
        """Räumt Ressourcen auf"""
        logging.info("Fahre Anwendung herunter")
        self.gpio.cleanup()
