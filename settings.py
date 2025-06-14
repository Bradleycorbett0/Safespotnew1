from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        self.bind(size=self.update_background, pos=self.update_background)

        # Set calm warm background color
        with self.canvas.before:
            self.bg_color = Color(1.0, 0.96, 0.89, 1)  # Light beige
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # Title
        self.title_label = Label(
            text='Settings',
            font_size='24sp',
            size_hint=(1, 0.1),
            color=(0.2, 0.2, 0.2, 1)  # Dark brown
        )
        self.layout.add_widget(self.title_label)

        # Notifications Toggle
        notif_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        notif_label = Label(
            text='Notifications',
            halign='left',
            color=(0.3, 0.2, 0.2, 1)
        )
        notif_switch = Switch(active=True)
        notif_layout.add_widget(notif_label)
        notif_layout.add_widget(notif_switch)
        self.layout.add_widget(notif_layout)

        # Back Button
        back_btn = Button(
            text='Back to Home',
            size_hint=(1, 0.1),
            background_color=(0.85, 0.6, 0.4, 1),  # Soft orange
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size