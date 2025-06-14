import os
import json
import shutil

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle

try:
    from plyer import camera
    PLYER_CAMERA_AVAILABLE = True
except ImportError:
    PLYER_CAMERA_AVAILABLE = False


class ImageGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)  # Warm beige
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

        # Search bar
        self.search_input = TextInput(
            hint_text="Search by spot name...",
            multiline=False,
            size_hint_y=None,
            height=80,
            font_size='18sp',
            padding=[10, 10],
            foreground_color=(0, 0, 0, 1),
            background_color=(1, 1, 1, 1)
        )
        self.search_input.bind(text=self.update_filter)
        self.layout.add_widget(self.search_input)

        # ScrollView
        self.scroll = ScrollView(size_hint=(1, 1))
        self.grid = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        # Buttons
        button_row = BoxLayout(size_hint_y=None, height=50, spacing=10)

        upload_btn = Button(
            text="Upload",
            background_color=(0.3, 0.5, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        upload_btn.bind(on_release=self.open_file_chooser)

        camera_btn = Button(
            text="Take Photo",
            background_color=(0.4, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        camera_btn.bind(on_release=self.take_photo)

        button_row.add_widget(upload_btn)
        button_row.add_widget(camera_btn)
        self.layout.add_widget(button_row)

        # Back button
        back_btn = Button(
            text="Back to Home",
            size_hint_y=None,
            height=50,
            background_color=(0.4, 0.3, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.load_images()

    def load_images(self, filter_text=""):
        self.grid.clear_widgets()
        file_path = "saved_spots.json"

        if not os.path.exists(file_path):
            self.grid.add_widget(Label(text="No saved spots found."))
            return

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            self.grid.add_widget(Label(text=f"Error reading spots: {e}"))
            return

        sorted_spots = sorted(data, key=lambda x: x["name"].lower())

        for spot in sorted_spots:
            if filter_text.lower() not in spot["name"].lower():
                continue

            spot_name = spot.get("name", "Unnamed Spot")
            image_file = spot.get("image_path", "placeholder.png")
            image_path = os.path.join("images", image_file)

            if not os.path.exists(image_path):
                image_path = "placeholder.png"

            image = Image(
                source=image_path,
                size_hint_y=None,
                height=200,
                allow_stretch=True
            )
            label = Label(
                text=spot_name,
                size_hint_y=None,
                height=40,
                font_size='18sp',
                color=(0, 0, 0, 1)
            )

            self.grid.add_widget(image)
            self.grid.add_widget(label)

    def update_filter(self, instance, value):
        self.load_images(filter_text=value)

    def open_file_chooser(self, instance):
        chooser = FileChooserIconView(path="/storage/emulated/0/", filters=["*.png", "*.jpg", "*.jpeg"])
        box = BoxLayout(orientation='vertical')
        box.add_widget(chooser)

        btn = Button(text="Select Image", size_hint_y=None, height=50)

        def save_selected(*args):
            selection = chooser.selection
            if selection:
                self.copy_image_to_folder(selection[0])
            popup.dismiss()

        btn.bind(on_release=save_selected)
        box.add_widget(btn)

        popup = Popup(title="Choose an image", content=box, size_hint=(0.95, 0.95))
        popup.open()

    def copy_image_to_folder(self, source_path):
        if not os.path.exists("images"):
            os.makedirs("images")

        filename = os.path.basename(source_path)
        dest_path = os.path.join("images", filename)

        try:
            shutil.copy(source_path, dest_path)
            self.update_spot_image(filename)
            self.load_images(self.search_input.text)
        except Exception as e:
            print(f"Failed to upload image: {e}")

    def update_spot_image(self, filename):
        spot_name = self.search_input.text.strip().lower()
        if not spot_name:
            return

        file_path = "saved_spots.json"
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        updated = False
        for spot in data:
            if spot_name in spot["name"].lower():
                spot["image_path"] = filename
                updated = True

        if updated:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

    def take_photo(self, instance):
        if not PLYER_CAMERA_AVAILABLE:
            popup = Popup(
                title="Camera Not Available",
                content=Label(text="Camera module (plyer) not installed."),
                size_hint=(0.7, 0.3)
            )
            popup.open()
            return

        filename = "photo_from_camera.jpg"
        dest_path = os.path.join("images", filename)
        try:
            camera.take_picture(filename=dest_path, on_complete=lambda x: self.on_camera_complete(filename))
        except Exception as e:
            popup = Popup(
                title="Camera Error",
                content=Label(text=f"Failed to take photo: {e}"),
                size_hint=(0.8, 0.3)
            )
            popup.open()

    def on_camera_complete(self, filename):
        self.update_spot_image(filename)
        self.load_images(self.search_input.text)