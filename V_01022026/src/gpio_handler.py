"""
GPIO Handler für Digitalein- und Ausgänge
"""
import logging
from typing import Dict, Callable

# Versuche RPi.GPIO zu importieren, fallback für Tests
try:
    import RPi.GPIO as GPIO
    ON_RASPBERRY = True
except (ImportError, RuntimeError):
    ON_RASPBERRY = False
    logging.warning("RPi.GPIO nicht verfügbar - Simulation Modus")


class DigitalInput:
    """Digitaler Eingang mit Callback-Unterstützung"""
    
    def __init__(self, pin: int, name: str, pull_up: bool = True):
        self.pin = pin
        self.name = name
        self.pull_up = pull_up
        self.state = False
        self.callbacks = []
        
        if ON_RASPBERRY:
            GPIO.setmode(GPIO.BCM)
            pull_mode = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
            GPIO.setup(pin, GPIO.IN, pull_up_down=pull_mode)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._on_change)
    
    def _on_change(self, pin):
        """Wird aufgerufen wenn sich der Pin-Zustand ändert"""
        self.read()
        for callback in self.callbacks:
            callback(self.name, self.state)
    
    def read(self) -> bool:
        """Liest aktuellen Zustand des Eingangs"""
        if ON_RASPBERRY:
            self.state = GPIO.input(self.pin) == GPIO.HIGH
        return self.state
    
    def add_callback(self, callback: Callable):
        """Registriert Callback für Zustandsänderungen"""
        self.callbacks.append(callback)
    
    def is_high(self) -> bool:
        """Gibt True zurück wenn Pin auf HIGH ist"""
        return self.read()


class DigitalOutput:
    """Digitaler Ausgang"""
    
    def __init__(self, pin: int, name: str):
        self.pin = pin
        self.name = name
        self.state = False
        
        if ON_RASPBERRY:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    
    def set_high(self):
        """Setzt Ausgang auf HIGH"""
        self.state = True
        if ON_RASPBERRY:
            GPIO.output(self.pin, GPIO.HIGH)
        logging.info(f"{self.name} eingeschaltet")
    
    def set_low(self):
        """Setzt Ausgang auf LOW"""
        self.state = False
        if ON_RASPBERRY:
            GPIO.output(self.pin, GPIO.LOW)
        logging.info(f"{self.name} ausgeschaltet")
    
    def is_high(self) -> bool:
        """Gibt True zurück wenn Ausgang auf HIGH ist"""
        return self.state
    
    def toggle(self):
        """Schaltet Ausgang um"""
        if self.state:
            self.set_low()
        else:
            self.set_high()
    
    def cleanup(self):
        """Räumt GPIO auf"""
        if ON_RASPBERRY:
            GPIO.output(self.pin, GPIO.LOW)


class GPIOManager:
    """Verwaltet alle digitalen Ein- und Ausgänge"""
    
    def __init__(self):
        self.inputs: Dict[str, DigitalInput] = {}
        self.outputs: Dict[str, DigitalOutput] = {}
        
        # Eingänge initialisieren (anpassbar in config)
        self.inputs['BRUNNEN_VOLL'] = DigitalInput(17, 'BRUNNEN_VOLL')
        self.inputs['BRUNNEN_LEER'] = DigitalInput(27, 'BRUNNEN_LEER')
        self.inputs['IBC_VOLL'] = DigitalInput(22, 'IBC_VOLL')
        self.inputs['IBC_MITTE'] = DigitalInput(23, 'IBC_MITTE')
        self.inputs['IBC_LEER'] = DigitalInput(24, 'IBC_LEER')
        
        # Ausgänge initialisieren (anpassbar in config)
        self.outputs['PUMPE'] = DigitalOutput(18, 'PUMPE')
        self.outputs['BEWAESSERUNG'] = DigitalOutput(25, 'BEWAESSERUNG')
        self.outputs['FEHLER'] = DigitalOutput(16, 'FEHLER')
    
    def get_input(self, name: str) -> DigitalInput:
        """Gibt Input-Objekt zurück"""
        return self.inputs.get(name)
    
    def get_output(self, name: str) -> DigitalOutput:
        """Gibt Output-Objekt zurück"""
        return self.outputs.get(name)
    
    def get_all_input_states(self) -> Dict[str, bool]:
        """Gibt alle Input-Zustände zurück"""
        return {name: inp.read() for name, inp in self.inputs.items()}
    
    def get_all_output_states(self) -> Dict[str, bool]:
        """Gibt alle Output-Zustände zurück"""
        return {name: out.is_high() for name, out in self.outputs.items()}
    
    def cleanup(self):
        """Räumt alle GPIO-Ressourcen auf"""
        for output in self.outputs.values():
            output.cleanup()
        if ON_RASPBERRY:
            GPIO.cleanup()
