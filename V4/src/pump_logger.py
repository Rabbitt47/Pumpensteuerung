"""
Logging von Pumpvorgängen in CSV-Format
"""
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict


class PumpLogger:
    """Speichert Pumpvorgänge in CSV-Datei"""
    
    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_pump_start = None
        self.current_pump_start_states = None
    
    def get_current_log_file(self) -> Path:
        """Gibt aktuelle Log-Datei zurück (eine pro Tag)"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.log_dir / f'pump_log_{today}.csv'
    
    def _ensure_csv_header(self):
        """Erstellt CSV-Header wenn Datei nicht existiert"""
        log_file = self.get_current_log_file()
        
        if not log_file.exists():
            try:
                with open(log_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow([
                        'Startzeit',
                        'BRUNNEN_VOLL_START',
                        'BRUNNEN_LEER_START',
                        'IBC_VOLL_START',
                        'IBC_MITTE_START',
                        'IBC_LEER_START',
                        'PUMPE_START',
                        'BEWAESSERUNG_START',
                        'Stoppzeit',
                        'BRUNNEN_VOLL_STOP',
                        'BRUNNEN_LEER_STOP',
                        'IBC_VOLL_STOP',
                        'IBC_MITTE_STOP',
                        'IBC_LEER_STOP',
                        'PUMPE_STOP',
                        'BEWAESSERUNG_STOP',
                        'Dauer (min)',
                    ])
                logging.info(f"CSV-Datei erstellt: {log_file}")
            except Exception as e:
                logging.error(f"Fehler beim Erstellen der CSV-Datei: {e}")
    
    def start_pump(self, input_states: Dict[str, bool], output_states: Dict[str, bool]):
        """Speichert Start eines Pumpvorgangs"""
        self.current_pump_start = datetime.now()
        self.current_pump_start_states = {
            'inputs': input_states.copy(),
            'outputs': output_states.copy(),
        }
        logging.info(f"Pumpenstart protokolliert: {self.current_pump_start}")
    
    def stop_pump(self, input_states: Dict[str, bool], output_states: Dict[str, bool]):
        """Speichert Stop eines Pumpvorgangs in CSV-Datei"""
        if self.current_pump_start is None:
            logging.warning("Pumpen-Stop ohne Pumpen-Start!")
            return
        
        stop_time = datetime.now()
        duration = (stop_time - self.current_pump_start).total_seconds() / 60
        
        # Stelle sicher, dass CSV-Header existiert
        self._ensure_csv_header()
        
        try:
            log_file = self.get_current_log_file()
            with open(log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                
                start_inputs = self.current_pump_start_states['inputs']
                start_outputs = self.current_pump_start_states['outputs']
                
                writer.writerow([
                    self.current_pump_start.strftime('%H:%M:%S'),
                    'H' if start_inputs.get('BRUNNEN_VOLL') else 'L',
                    'H' if start_inputs.get('BRUNNEN_LEER') else 'L',
                    'H' if start_inputs.get('IBC_VOLL') else 'L',
                    'H' if start_inputs.get('IBC_MITTE') else 'L',
                    'H' if start_inputs.get('IBC_LEER') else 'L',
                    'H' if start_outputs.get('PUMPE') else 'L',
                    'H' if start_outputs.get('BEWAESSERUNG') else 'L',
                    stop_time.strftime('%H:%M:%S'),
                    'H' if input_states.get('BRUNNEN_VOLL') else 'L',
                    'H' if input_states.get('BRUNNEN_LEER') else 'L',
                    'H' if input_states.get('IBC_VOLL') else 'L',
                    'H' if input_states.get('IBC_MITTE') else 'L',
                    'H' if input_states.get('IBC_LEER') else 'L',
                    'H' if output_states.get('PUMPE') else 'L',
                    'H' if output_states.get('BEWAESSERUNG') else 'L',
                    f'{duration:.1f}',
                ])
            
            logging.info(f"Pumpvorgang gespeichert: {duration:.1f} min")
            self.current_pump_start = None
            self.current_pump_start_states = None
        
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Pumpvorgangs: {e}")
    
    def get_last_pump_events(self, count: int = 10) -> list:
        """Liest letzte Pumpvorgänge aus CSV-Datei"""
        log_file = self.get_current_log_file()
        
        if not log_file.exists():
            return []
        
        try:
            events = []
            with open(log_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    events.append(row)
            
            # Gebe letzte 'count' Einträge zurück
            return events[-count:] if events else []
        
        except Exception as e:
            logging.error(f"Fehler beim Lesen der CSV-Datei: {e}")
            return []
