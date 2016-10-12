from kivy.uix.screenmanager import Screen
import tracker

class BaseScreen(Screen):
    def on_enter(self):
        tracker.tracker.send(tracker
                             .ScreenViewBuilder()
                             .set(cd=type(self).__name__).build())
