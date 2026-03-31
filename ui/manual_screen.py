"""
Manualbetrieb-Bildschirm
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class ManualScreen(BoxLayout):
    """Manualbetrieb-Bildschirm"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Header
        header = Label(
            text='🎮 MANUALBETRIEB',
            font_size='24sp',
            bold=True,
            size_hint_y=0.1
        )
        self.add_widget(header)
        
        # Content-Bereich
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.8)
        
        # Digitale Ein-/Ausgänge Anzeige
        io_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.4)
        
        io_title = Label(
            text='DIGITALE EIN-/AUSGÄNGE',
            font_size='16sp',
            bold=True,
            size_hint_y=0.1
        )
        io_grid.add_widget(io_title)
        io_grid.add_widget(Label(text=''))
        
        # Eingänge
        for name, state in self.app.gpio.get_all_input_states().items():
            label = Label(text=f'{name}:', size_hint_y=0.4, font_size='12sp')
            color = (0.2, 0.8, 0.2, 1) if state else (0.8, 0.2, 0.2, 1)
            state_btn = Button(
                text='HIGH' if state else 'LOW',
                background_color=color,
                size_hint_y=0.4
            )
            io_grid.add_widget(label)
            io_grid.add_widget(state_btn)
        
        content.add_widget(io_grid)
        
        # Pump-Steuerung
        pump_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        pump_label = Label(
            text='PUMPEN-STEUERUNG',
            font_size='16sp',
            bold=True,
            size_hint_y=0.15
        )
        pump_box.add_widget(pump_label)
        
        # Pump-Buttons
        button_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.85)
        
        pump_on_btn = Button(
            text='🟢 PUMPE EIN',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='14sp'
        )
        pump_on_btn.bind(on_press=self.pump_on)
        button_grid.add_widget(pump_on_btn)
        
        pump_off_btn = Button(
            text='🔴 PUMPE AUS',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='14sp'
        )
        pump_off_btn.bind(on_press=self.pump_off)
        button_grid.add_widget(pump_off_btn)
        
        pump_box.add_widget(button_grid)
        content.add_widget(pump_box)
        
        self.add_widget(content)
        
        # Buttons am unteren Ende
        button_footer = BoxLayout(spacing=10, size_hint_y=0.1)
        
        back_btn = Button(text='← ZURÜCK', size_hint_x=1)
        back_btn.bind(on_press=self.go_back)
        button_footer.add_widget(back_btn)
        
        self.add_widget(button_footer)
    
    def pump_on(self, widget):
        """Schaltet Pumpe ein"""
        if not self.app.pump_controller.is_automatic:
            self.app.pump_controller.set_pump_manual(True)
            print("Pumpe eingeschaltet (Manualbetrieb)")
        else:
            print("Manualbetrieb ist deaktiviert - Wechsle zum Manualbetrieb")
    
    def pump_off(self, widget):
        """Schaltet Pumpe aus"""
        if not self.app.pump_controller.is_automatic:
            self.app.pump_controller.set_pump_manual(False)
            print("Pumpe ausgeschaltet (Manualbetrieb)")
        else:
            print("Manualbetrieb ist deaktiviert - Wechsle zum Manualbetrieb")
    
    def go_back(self, widget):
        """Zurück zum Hauptmenü"""
        self.app.root.current = 'main'
