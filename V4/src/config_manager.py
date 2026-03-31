"""
Konfigurationsmanager für Einstellungen
"""
import json
import logging
from datetime import time
from pathlib import Path


class ConfigManager:
    """Verwaltet Anwendungskonfiguration"""
    
    DEFAULT_CONFIG = {
        'pump_start_time': '22:00',
        'pump_end_time': '04:00',
        'max_pump_duration': 30,
        'system_sleep_timeout': 10,  # Minuten nach Boot
        'pump_off_sleep_timeout': 10,  # Minuten nach Pump aus
        'wake_interval': 30,  # Minuten zwischen Aufweckungen
        'wake_duration': 5,  # Minuten aktiv nach Aufweckung
        'display_theme': 'dark',
        'date_format': '%d.%m.%Y',
        'time_format': '%H:%M:%S',
    }
    
    def __init__(self, config_path: str = 'config/settings.json'):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Lädt Konfiguration aus Datei oder erstellt default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Fehler beim Laden der Konfiguration: {e}")
        
        # Speichere default Konfiguration
        self.save_config(self.DEFAULT_CONFIG)
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: dict = None):
        """Speichert Konfiguration in Datei"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logging.info(f"Konfiguration gespeichert: {self.config_path}")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Konfiguration: {e}")
    
    def get(self, key: str, default=None):
        """Gibt Konfigurationswert zurück"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Setzt Konfigurationswert"""
        self.config[key] = value
    
    def get_pump_start_time(self) -> time:
        """Gibt Pump-Startzeit als time-Objekt zurück"""
        time_str = self.config.get('pump_start_time', '22:00')
        try:
            h, m = map(int, time_str.split(':'))
            return time(h, m)
        except:
            return time(22, 0)
    
    def get_pump_end_time(self) -> time:
        """Gibt Pump-Endzeit als time-Objekt zurück"""
        time_str = self.config.get('pump_end_time', '04:00')
        try:
            h, m = map(int, time_str.split(':'))
            return time(h, m)
        except:
            return time(4, 0)
    
    def set_pump_times(self, start_time: time, end_time: time):
        """Setzt Pump-Zeiten"""
        self.config['pump_start_time'] = start_time.strftime('%H:%M')
        self.config['pump_end_time'] = end_time.strftime('%H:%M')
        self.save_config()
    
    def set_max_pump_duration(self, minutes: int):
        """Setzt maximale Pumpzeit"""
        self.config['max_pump_duration'] = minutes
        self.save_config()
