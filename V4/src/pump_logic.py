"""
Pumpensteuerungslogik
"""
import logging
from datetime import datetime, time
from src.gpio_handler import GPIOManager


class PumpController:
    """Implementiert die Pumpensteuerungslogik"""
    
    def __init__(self, gpio_manager: GPIOManager):
        self.gpio = gpio_manager
        self.is_automatic = True
        self.pump_start_time = time(22, 0)  # 22:00 Uhr
        self.pump_end_time = time(4, 0)      # 04:00 Uhr
        self.max_pump_duration = 30  # Minuten
        self.pump_start_datetime = None
    
    def is_within_pump_hours(self) -> bool:
        """Prüft ob aktuelle Zeit innerhalb Pumpzeitfenster liegt"""
        now = datetime.now().time()
        
        # Falls End-Zeit < Start-Zeit (über Mitternacht)
        if self.pump_start_time > self.pump_end_time:
            return now >= self.pump_start_time or now < self.pump_end_time
        else:
            return self.pump_start_time <= now < self.pump_end_time
    
    def check_error_condition(self) -> bool:
        """
        Prüft Fehlerbedingungen
        Fehler = LOW, kein Fehler = HIGH
        """
        brunnen_voll = self.gpio.get_input('BRUNNEN_VOLL').is_high()
        brunnen_leer = self.gpio.get_input('BRUNNEN_LEER').is_high()
        ibc_voll = self.gpio.get_input('IBC_VOLL').is_high()
        ibc_mitte = self.gpio.get_input('IBC_MITTE').is_high()
        ibc_leer = self.gpio.get_input('IBC_LEER').is_high()
        
        # Fehler wenn beide Sensoren gleichzeitig aktiv
        error = False
        
        # Brunnen: beide Sensoren gleichzeitig
        if brunnen_voll and brunnen_leer:
            error = True
            logging.warning("FEHLER: Brunnen VOLL und LEER gleichzeitig!")
        
        # IBC: MITTE und LEER gleichzeitig
        if ibc_mitte and ibc_leer:
            error = True
            logging.warning("FEHLER: IBC MITTE und LEER gleichzeitig!")
        
        # IBC: VOLL ohne MITTE
        if ibc_voll and not ibc_mitte:
            error = True
            logging.warning("FEHLER: IBC VOLL aber nicht MITTE!")
        
        # IBC: LEER aber nicht MITTE
        if ibc_leer and ibc_mitte:
            error = True
            logging.warning("FEHLER: IBC LEER und MITTE gleichzeitig!")
        
        return error
    
    def update_error_output(self):
        """Aktualisiert Fehler-Ausgang basierend auf Logik"""
        if self.check_error_condition():
            self.gpio.get_output('FEHLER').set_low()  # Fehler = LOW
        else:
            self.gpio.get_output('FEHLER').set_high()  # Kein Fehler = HIGH
    
    def calculate_pump_state_automatic(self) -> bool:
        """
        Berechnet ob Pumpe im Automatikbetrieb eingeschaltet sein soll
        
        Pumpe EIN (HIGH) wenn:
        - Zeit innerhalb Pumpzeit UND
        - Brunnen voll UND
        - NICHT IBC_MITTE
        
        Pumpe AUS (LOW) wenn:
        - Brunnen leer ODER
        - IBC voll
        """
        brunnen_voll = self.gpio.get_input('BRUNNEN_VOLL').is_high()
        brunnen_leer = self.gpio.get_input('BRUNNEN_LEER').is_high()
        ibc_voll = self.gpio.get_input('IBC_VOLL').is_high()
        ibc_mitte = self.gpio.get_input('IBC_MITTE').is_high()
        
        # Pumpe ausschalten
        if brunnen_leer or ibc_voll:
            return False
        
        # Pumpe einschalten
        if (self.is_within_pump_hours() and 
            brunnen_voll and 
            not ibc_mitte):
            return True
        
        return False
    
    def update_pump_automatic(self):
        """Aktualisiert Pumpen-Ausgang im Automatikbetrieb"""
        if not self.is_automatic:
            return
        
        should_pump = self.calculate_pump_state_automatic()
        pump = self.gpio.get_output('PUMPE')
        
        # Schalte Pumpe um wenn nötig
        if should_pump and not pump.is_high():
            pump.set_high()
            self.pump_start_datetime = datetime.now()
            logging.info(f"Pumpe eingeschaltet - {self.pump_start_datetime}")
        
        elif not should_pump and pump.is_high():
            pump.set_low()
            logging.info(f"Pumpe ausgeschaltet - {datetime.now()}")
        
        # Prüfe maximale Pumpzeit
        if pump.is_high() and self.pump_start_datetime:
            duration_minutes = (datetime.now() - self.pump_start_datetime).total_seconds() / 60
            if duration_minutes > self.max_pump_duration:
                pump.set_low()
                logging.warning(f"Pumpe aus - Maximale Pumpzeit ({self.max_pump_duration}min) überschritten!")
    
    def set_pump_manual(self, turn_on: bool):
        """Schaltet Pumpe im Manualbetrieb ein/aus"""
        pump = self.gpio.get_output('PUMPE')
        if turn_on:
            pump.set_high()
            self.pump_start_datetime = datetime.now()
        else:
            pump.set_low()
    
    def update(self):
        """Aktualisiert alle Steuerungslogiken"""
        self.update_error_output()
        if self.is_automatic:
            self.update_pump_automatic()
