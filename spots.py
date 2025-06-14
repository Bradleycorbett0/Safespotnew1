import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup


class SafeSpotsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.scrollview = ScrollView()
        self.spot_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        self.spot_list.bind(minimum_height=self.spot_list.setter('height'))
        self.scrollview.add_widget(self.spot_list)
        self.layout.add_widget(self.scrollview)

        back_btn = Button(
            text='Back to Home',
            size_hint=(1, 0.1),
            background_color=(0.6, 0.4, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.refresh_spots()

    def refresh_spots(self):
        self.spot_list.clear_widgets()

        spots_file = "/storage/emulated/0/safespot/saved_spots.json"
        if not os.path.exists(spots_file):
            self.spot_list.add_widget(Label(text="No spots saved yet.", size_hint_y=None, height=40))
            return

        try:
            with open(spots_file, "r") as f:
                spots = json.load(f)

            for index, spot in enumerate(sorted(spots, key=lambda x: x.get('name', '').lower())):
                name = spot.get('name', 'Unnamed')
                tag = spot.get('tag', '')
                desc = spot.get('description', '')

                full_text = f"[b]{name}[/b] ({tag})\n{desc}"

                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)

                lbl = Label(
                    text=full_text,
                    markup=True,
                    halign='left',
                    valign='middle',
                    font_size='16sp',
                    color=(0.1, 0.1, 0.1, 1)
                )
                lbl.bind(
                    width=lambda instance, value: setattr(instance, 'text_size', (value - 40, None))
                )

                delete_btn = Button(
                    text="Delete",
                    size_hint=(None, 1),
                    width=100,
                    background_color=(1, 0.3, 0.3, 1),
                    color=(1, 1, 1, 1)
                )
                delete_btn.bind(on_release=lambda btn, i=index: self.delete_spot(i))

                row.add_widget(lbl)
                row.add_widget(delete_btn)
                self.spot_list.add_widget(row)

        except Exception as e:
            self.spot_list.add_widget(Label(text="Error loading safe spots.", size_hint_y=None, height=40))
            print("Error loading saved_spots.json:", e)

    def delete_spot(self, index):
        spots_file = "/storage/emulated/0/safespot/saved_spots.json"
        try:
            with open(spots_file, "r") as f:
                spots = json.load(f)

            sorted_spots = sorted(spots, key=lambda x: x.get('name', '').lower())
            del sorted_spots[index]

            with open(spots_file, "w") as f:
                json.dump(sorted_spots, f, indent=2)

            self.refresh_spots()
        except Exception as e:
            print("Failed to delete spot:", e)