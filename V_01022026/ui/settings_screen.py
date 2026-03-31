"""
Einstellungs-Bildschirm
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


class SettingsScreen(BoxLayout):
    """Einstellungs-Bildschirm für Uhrzeit, Datum und Pumpzeiten"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Header
        header = Label(
            text='⚙ EINSTELLUNGEN',
            font_size='24sp',
            bold=True,
            size_hint_y=0.1
        )
        self.add_widget(header)
        
        # Content-Bereich
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.8)
        
        # Pumpzeit-Einstellungen
        pump_settings = GridLayout(cols=3, spacing=10, size_hint_y=0.33)
        
        # Start-Zeit
        pump_settings.add_widget(Label(text='Start-Pumpzeit:', font_size='12sp'))
        self.start_hour = Spinner(
            text=str(self.app.pump_controller.pump_start_time.hour),
            values=[str(i).zfill(2) for i in range(24)],
            size_hint_x=0.25
        )
        self.start_minute = Spinner(
            text=str(self.app.pump_controller.pump_start_time.minute),
            values=[str(i).zfill(2) for i in range(0, 60, 5)],
            size_hint_x=0.25
        )
        start_box = BoxLayout(spacing=5, size_hint_x=0.5)
        start_box.add_widget(self.start_hour)
        start_box.add_widget(Label(text=':', size_hint_x=0.1))
        start_box.add_widget(self.start_minute)
        pump_settings.add_widget(start_box)
        pump_settings.add_widget(Label(text=''))  # Füllfläche
        
        # End-Zeit
        pump_settings.add_widget(Label(text='Ende-Pumpzeit:', font_size='12sp'))
        self.end_hour = Spinner(
            text=str(self.app.pump_controller.pump_end_time.hour),
            values=[str(i).zfill(2) for i in range(24)],
            size_hint_x=0.25
        )
        self.end_minute = Spinner(
            text=str(self.app.pump_controller.pump_end_time.minute),
            values=[str(i).zfill(2) for i in range(0, 60, 5)],
            size_hint_x=0.25
        )
        end_box = BoxLayout(spacing=5, size_hint_x=0.5)
        end_box.add_widget(self.end_hour)
        end_box.add_widget(Label(text=':', size_hint_x=0.1))
        end_box.add_widget(self.end_minute)
        pump_settings.add_widget(end_box)
        pump_settings.add_widget(Label(text=''))  # Füllfläche
        
        # Max Pumpzeit
        pump_settings.add_widget(Label(text='Max Pumpzeit (min):', font_size='12sp'))
        self.max_pump_input = TextInput(
            text=str(self.app.pump_controller.max_pump_duration),
            input_filter='int',
            size_hint_x=0.5,
            multiline=False
        )
        pump_settings.add_widget(self.max_pump_input)
        pump_settings.add_widget(Label(text=''))
        
        content.add_widget(pump_settings)
        
        # Buttons am unteren Ende
        button_box = BoxLayout(spacing=10, size_hint_y=0.2)
        
        save_btn = Button(text='💾 SPEICHERN', size_hint_x=0.5)
        save_btn.bind(on_press=self.save_settings)
        button_box.add_widget(save_btn)
        
        back_btn = Button(text='← ZURÜCK', size_hint_x=0.5)
        back_btn.bind(on_press=self.go_back)
        button_box.add_widget(back_btn)
        
        content.add_widget(button_box)
        self.add_widget(content)
    
    def save_settings(self, widget):
        """Speichert Einstellungen"""
        try:
            # Parse Zeiten
            start_time = f"{self.start_hour.text}:{self.start_minute.text}"
            end_time = f"{self.end_hour.text}:{self.end_minute.text}"
            max_pump = int(self.max_pump_input.text)
            
            # Speichere in Config
            self.app.config.set('pump_start_time', start_time)
            self.app.config.set('pump_end_time', end_time)
            self.app.config.set('max_pump_duration', max_pump)
            self.app.config.save_config()
            
            # Update Pump-Controller
            self.app.pump_controller.pump_start_time = self.app.config.get_pump_start_time()
            self.app.pump_controller.pump_end_time = self.app.config.get_pump_end_time()
            self.app.pump_controller.max_pump_duration = max_pump
            
            print("Einstellungen gespeichert!")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
        
        self.go_back()
    
    def go_back(self, widget=None):
        """Zurück zum Hauptmenü"""
        self.app.root.current = 'main'
