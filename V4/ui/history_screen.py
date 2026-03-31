"""
Pumpverlauf-Bildschirm
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class HistoryScreen(BoxLayout):
    """Pumpverlauf-Bildschirm mit Tabelle"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Header
        header = Label(
            text='📋 PUMPVERLAUF - LETZTE 10 VORGÄNGE',
            font_size='18sp',
            bold=True,
            size_hint_y=0.1
        )
        self.add_widget(header)
        
        # Content-Bereich mit Scroll
        content = ScrollView(size_hint_y=0.8)
        
        # Tabelle
        table_grid = GridLayout(cols=3, spacing=5, size_hint_y=None, padding=5)
        table_grid.bind(minimum_height=table_grid.setter('height'))
        
        # Header-Zeile
        header_cells = ['Startzeit', 'Stoppzeit', 'Dauer (min)']
        for cell_text in header_cells:
            cell = Label(
                text=cell_text,
                font_size='12sp',
                bold=True,
                size_hint_y=None,
                height=40,
                color=(0.2, 0.2, 0.8, 1)
            )
            table_grid.add_widget(cell)
        
        # Daten aus CSV laden
        events = self.app.pump_logger.get_last_pump_events(10)
        
        if events:
            for event in reversed(events):  # Neueste zuerst
                for field in ['Startzeit', 'Stoppzeit', 'Dauer (min)']:
                    cell = Label(
                        text=event.get(field, '-'),
                        font_size='10sp',
                        size_hint_y=None,
                        height=35
                    )
                    table_grid.add_widget(cell)
        else:
            no_data = Label(
                text='Noch keine Pumpvorgänge protokolliert',
                font_size='12sp',
                size_hint_y=None,
                height=40,
                color=(0.7, 0.7, 0.7, 1)
            )
            table_grid.add_widget(no_data)
        
        content.add_widget(table_grid)
        self.add_widget(content)
        
        # Buttons am unteren Ende
        button_footer = BoxLayout(spacing=10, size_hint_y=0.1)
        
        refresh_btn = Button(text='🔄 AKTUALISIEREN', size_hint_x=0.5)
        refresh_btn.bind(on_press=self.refresh)
        button_footer.add_widget(refresh_btn)
        
        back_btn = Button(text='← ZURÜCK', size_hint_x=0.5)
        back_btn.bind(on_press=self.go_back)
        button_footer.add_widget(back_btn)
        
        self.add_widget(button_footer)
    
    def refresh(self, widget):
        """Aktualisiert die Anzeige"""
        self.app.root.current = 'main'
        self.app.root.current = 'history'
    
    def go_back(self, widget):
        """Zurück zum Hauptmenü"""
        self.app.root.current = 'main'
