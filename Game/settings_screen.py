from kivy.uix.screenmanager import ScreenManager, Screen


class SettingsScreen(Screen):

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(SettingsScreen, self).__init__(**kwargs)
        self.sm = sm
        self.name = kwargs['name']