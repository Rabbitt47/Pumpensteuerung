"""
Strom PI Integration - RTC und Sleep Mode Management
"""
import logging
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path


class StromPIManager:
    """Verwaltet RTC und Sleep-Mode des Strom PI"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.last_pump_stop = datetime.now()
        self.boot_time = datetime.now()
        self.rtc_available = self._check_rtc()
        
        if self.rtc_available:
            logging.info("Strom PI RTC erkannt")
            self._sync_rtc()
    
    def _check_rtc(self) -> bool:
        """Prüft ob RTC-Modul verfügbar ist"""
        try:
            # Versuche i2c_detect für RTC-Modul zu laufen
            result = subprocess.run(
                ['i2cdetect', '-y', '1'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # DS3231 wird normalerweise bei 0x68 angezeigt
            if '68' in result.stdout:
                return True
        except Exception as e:
            logging.warning(f"RTC-Check fehlgeschlagen: {e}")
        
        return False
    
    def _sync_rtc(self):
        """Synchronisiert Systemzeit mit RTC"""
        try:
            # Versuche Systemzeit von RTC zu setzen
            subprocess.run(
                ['hwclock', '--hctosys'],
                check=True,
                timeout=5
            )
            logging.info(f"Systemzeit synchronisiert: {datetime.now()}")
        except Exception as e:
            logging.warning(f"RTC-Sync fehlgeschlagen: {e}")
    
    def get_current_time(self) -> datetime:
        """Gibt aktuelle Zeit zurück (von RTC wenn verfügbar)"""
        if self.rtc_available:
            try:
                # Lese Zeit direkt von RTC
                result = subprocess.run(
                    ['hwclock', '--show'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                # Parse output: "2024-02-01 14:30:45 +0000"
                time_str = result.stdout.strip().split()[0] + ' ' + result.stdout.strip().split()[1]
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                logging.warning(f"RTC-Abfrage fehlgeschlagen: {e}")
        
        return datetime.now()
    
    def set_system_time(self, dt: datetime):
        """Setzt Systemzeit (für Einstellungs-Menü)"""
        try:
            # Setze Systemzeit
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            subprocess.run(
                ['sudo', 'date', '-s', time_str],
                check=True,
                timeout=5
            )
            
            # Synchronisiere RTC
            if self.rtc_available:
                subprocess.run(
                    ['sudo', 'hwclock', '--systohc'],
                    check=True,
                    timeout=5
                )
            
            logging.info(f"Systemzeit gesetzt: {time_str}")
        except Exception as e:
            logging.error(f"Fehler beim Setzen der Zeit: {e}")
    
    def on_pump_stopped(self):
        """Wird aufgerufen wenn Pumpe ausgeschaltet wird"""
        self.last_pump_stop = datetime.now()
    
    def should_enter_sleep(self) -> bool:
        """Prüft ob System in den Sleep-Mode gehen sollte"""
        boot_timeout = self.config.get('system_sleep_timeout', 10) * 60
        pump_timeout = self.config.get('pump_off_sleep_timeout', 10) * 60
        
        # Prüfe Zeit seit Boot
        time_since_boot = (datetime.now() - self.boot_time).total_seconds()
        if time_since_boot < boot_timeout:
            return False
        
        # Prüfe Zeit seit Pump-Stop
        time_since_pump_stop = (datetime.now() - self.last_pump_stop).total_seconds()
        if time_since_pump_stop < pump_timeout:
            return False
        
        return True
    
    def enter_sleep_mode(self):
        """Versetzt System in den Sleep-Mode über Strom PI"""
        try:
            logging.info("Fahre in Sleep-Mode...")
            
            # Berechne Aufweckungszeit
            wake_interval = self.config.get('wake_interval', 30)
            wake_time = datetime.now() + timedelta(minutes=wake_interval)
            
            # Setze RTC-Alarm (falls Strom PI unterstützt)
            if self.rtc_available:
                self._set_rtc_alarm(wake_time)
            
            # Fahre System herunter (Strom PI wird es wieder hochfahren)
            subprocess.run(
                ['sudo', 'systemctl', 'suspend'],
                check=False,
                timeout=5
            )
            
            logging.info(f"Sleep-Mode beendet - Wiederaufweckung geplant für {wake_time}")
        except Exception as e:
            logging.error(f"Sleep-Mode Fehler: {e}")
    
    def _set_rtc_alarm(self, wake_time: datetime):
        """Setzt RTC-Alarm für Aufweckung"""
        try:
            # Setze RTC-Alarm für die gewünschte Zeit
            # Dies ist hardware-spezifisch und hängt vom Strom PI ab
            
            # Beispiel für DS3231:
            # - Alarm 1 auf wake_time setzen
            # - Enable Alarm Interrupt
            
            # Die genaue Implementierung hängt von der Hardware ab
            logging.info(f"RTC-Alarm würde auf {wake_time} gesetzt")
        except Exception as e:
            logging.warning(f"RTC-Alarm Fehler: {e}")
    
    def get_wake_duration_remaining(self) -> int:
        """Gibt verbleibende aktive Zeit nach Aufweckung zurück (Minuten)"""
        wake_duration = self.config.get('wake_duration', 5) * 60
        elapsed = (datetime.now() - self.boot_time).total_seconds()
        
        remaining = int((wake_duration - elapsed) / 60)
        return max(0, remaining)
    
    def get_sleep_status(self) -> dict:
        """Gibt Sleep-Modus Status zurück"""
        return {
            'rtc_available': self.rtc_available,
            'current_time': self.get_current_time(),
            'time_since_boot': (datetime.now() - self.boot_time).total_seconds() / 60,
            'time_since_pump_stop': (datetime.now() - self.last_pump_stop).total_seconds() / 60,
            'should_sleep': self.should_enter_sleep(),
            'boot_timeout': self.config.get('system_sleep_timeout', 10),
            'pump_timeout': self.config.get('pump_off_sleep_timeout', 10),
        }


# Installation Instructions für Strom PI RTC

"""
STROM PI INSTALLATION:

1. Hardware-Setup:
   - Strom PI auf Raspberry Pi aufstecken
   - DS3231 RTC-Modul ist auf dem Strom PI enthalten
   
2. Software-Installation:
   
   a) I2C aktivieren:
      sudo raspi-config
      -> Interfacing Options -> I2C -> Yes
   
   b) I2C Tools installieren:
      sudo apt-get install i2c-tools
   
   c) DS3231 Kernel-Modul laden:
      sudo nano /etc/modules
      -> Füge hinzu: rtc-ds3231
      -> Ctrl+X, Y, Enter
   
   d) Device Tree Overlay aktivieren:
      sudo nano /boot/config.txt
      -> Füge hinzu:
         dtoverlay=i2c-rtc,ds3231
      -> Ctrl+X, Y, Enter
   
   e) Neustart:
      sudo reboot
   
3. RTC synchronisieren:
   
   sudo hwclock --show          # Zeige RTC-Zeit
   sudo hwclock --hctosys       # RTC -> System
   sudo hwclock --systohc       # System -> RTC
   
4. Sleep-Mode testen:
   
   sudo systemctl suspend       # System suspend
   # Strom PI weckt nach konfig Zeit auf

STROM PI SLEEP-MODE:

Der Strom PI kann das System nach konfigurierbaren Zeiten aufwecken:
- Nach 10 Min Boot
- Nach 10 Min Pump-Stop
- Weckung alle 30 Min für 5 Min Aktivität

Konfiguration in config/settings.json:
- system_sleep_timeout: Zeit nach Boot bis Sleep (Min)
- pump_off_sleep_timeout: Zeit nach Pump-Stop bis Sleep (Min)
- wake_interval: Interval zwischen Aufweckungen (Min)
- wake_duration: Aktiv-Dauer nach Aufweckung (Min)
"""
