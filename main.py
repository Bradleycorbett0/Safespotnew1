import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

# Import screens
from screens.login import LoginScreen
from screens.permission import PermissionScreen
from screens.home import HomeScreen
from screens.add import AddSpotScreen
from screens.spots import SafeSpotsScreen
from screens.emergency import EmergencyContactsScreen
from screens.events import EventsScreen
from screens.settings import SettingsScreen
from screens.about import AboutScreen
from screens.comments import CommentsScreen
from screens.gallery import ImageGalleryScreen
from screens.adpermission import AdPermissionScreen  # ✅ Include the new screen

class SafeSpotApp(App):
    def build(self):
        self.title = "SafeSpot"
        self.logged_in = False
        self.data_file = os.path.join(self.user_data_dir, 'userdata.json')

        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PermissionScreen(name='permission'))
        sm.add_widget(AdPermissionScreen(name='adpermission'))  # ✅ Added
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddSpotScreen(name='add'))
        sm.add_widget(SafeSpotsScreen(name='spots'))
        sm.add_widget(EmergencyContactsScreen(name='emergency'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(CommentsScreen(name='comments'))
        sm.add_widget(ImageGalleryScreen(name='gallery'))

        sm.current = 'login'
        return sm

    # ✅ Save user settings (like ad_consent)
    def save_user_data(self, key, value):
        data = self.load_user_data()
        data[key] = value
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    # ✅ Load user data safely
    def load_user_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

if __name__ == '__main__':
    SafeSpotApp().run()