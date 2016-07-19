from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


# class MyApp(App):
#
#     def build(self):
#         return LoginScreen()
#
#
# if __name__ == '__main__':
#     MyApp().run()

Builder.load_string("""
<MenuScreen>:
    GridLayout:
        cols:  1
        Button:
            text: 'Play'
            on_press: root.manager.current = 'field'
        Button:
            text: 'Settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'About...'
        Button:
            text: 'Quit'



<SettingsScreen>:
    GridLayout:
        cols: 1
        Button:
            text: 'STUB:My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'



<FieldScreen>:
    FloatLayout:
        Button:
            size_hint: None, None
            text: 'STUB:Stub button'
            size: 50, 50
            pos: 0, 0
        Button:
            size_hint: None, None
            size: 50, 50
            pos: 100, 100
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'


""")


# Declare both screens
class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class FieldScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager( transition=WipeTransition() )
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(FieldScreen(name='field'))


class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
