from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition


# class LoginScreen(GridLayout):
#
#     def __init__(self, **kwargs):
#         super(LoginScreen, self).__init__(**kwargs)
#         self.cols = 2
#         self.add_widget(Label(text='User Name'))
#         self.username = TextInput(multiline=False)
#         self.add_widget(self.username)
#         self.add_widget(Label(text='password'))
#         self.password = TextInput(password=True, multiline=False)
#         self.add_widget(self.password)


# class MyApp(App):
#
#     def build(self):
#         return LoginScreen()
#
#
# if __name__ == '__main__':
#     MyApp().run()

gui_kv_string = """
#: import WipeTransition kivy.uix.screenmanager.WipeTransition
ScreenManager:
    transition: WipeTransition()
    MenuScreen:
        name: 'menu'
    SettingsScreen:
        name: 'settings'
    FieldScreen:
        name: 'field'


<MenuScreen@Screen>:
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
            on_release: exit()



<SettingsScreen@Screen>:
    GridLayout:
        cols: 1
        Button:
            text: 'STUB:My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'



<FieldScreen@Screen>:
    FloatLayout:
        canvas:
            Color:
                rgb: 1, 1, 1
            Rectangle:
                source: 'assets/field-mockup1.png'
                size: self.size
        Button:
            size_hint: 0.1, 0.1
            text: 'STUB:Stub button'
            #size: 50, 50
            #pos: 0, 0
            pos_hint: {'x':.2, 'y':.2}
        Button:
            size_hint: 0.1, 0.1
            #size: 50, 50
            pos: 100, 100
            # pos_hint: 0.2, 0.2
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'


"""


# Declare both screens
# class MenuScreen(Screen):
#     pass
#
#
# class SettingsScreen(Screen):
#     pass
#
#
# class FieldScreen(Screen):
#     pass


class TrumpStampApp(App):
    def build(self):
        # Create the screen manager
        rw = Builder.load_string( gui_kv_string)
        # sm = ScreenManager(transition=WipeTransition())
        # sm.add_widget(MenuScreen(name='menu'))
        # sm.add_widget(SettingsScreen(name='settings'))
        # sm.add_widget(FieldScreen(name='field'))
        # return sm
        return rw

if __name__ == '__main__':
    TrumpStampApp().run()
