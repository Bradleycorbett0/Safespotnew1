from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

# Optional: Set a warm background color
Window.clearcolor = (0.98, 0.94, 0.9, 1)  # Soft warm beige

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.go_to_home, 2.5)

    def go_to_home(self, *args):
        self.manager.current = 'home'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        # Big centered logo
        logo = Image(
            source='logo.png',
            allow_stretch=True,
            size_hint=(1, 0.5)
        )

        # Warm welcome label
        welcome = Label(
            text='Welcome to SafeSpot!',
            font_size='28sp',
            color=(0.2, 0.2, 0.2, 1)  # Dark brown text
        )

        layout.add_widget(logo)
        layout.add_widget(welcome)
        self.add_widget(layout)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Home Screen'))

class SafeSpotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    SafeSpotApp().run()