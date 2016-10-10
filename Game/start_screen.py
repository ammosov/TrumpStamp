"""Start screen module."""
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
import elections_game
from settings_screen import SettingsScreen
from credits_screen import CreditScreen
from kivy.uix.behaviors import ButtonBehavior


class Icon(Button):
    """Icon class."""
    def __init__(self, **kwargs):
        """Init icon."""
        self.name = None
        self.image = ""
        self.pos_hint = {'x': None, 'y': None}
        self.size_hint = (None, None)
        super(Icon, self).__init__()

    def late_init(self, **kwargs):
        """Populate icon."""
        self.name = kwargs['name']
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        """Set background image."""
        pass


class StartScreen(Screen):
    """Start screen class."""

    POSITIONS_X = {0: 1128 / 2048.0,
                   1: 190 / 2048.0,
                   2: 680 / 2048.,
                   3: 680 / 2048.}
    POSITIONS_Y = {0: (1536.0 - 730.0) / 1536.0,
                   1: (1536.0 - 730.0) / 1536.0,
                   2: (1536 - 1150) / 1536.,
                   3: (1536 - 1400) / 1536.}

    SIZE = (730 / 2048.0, (1536 - 1340) / 1536.0)

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(StartScreen, self).__init__(**kwargs)

        names = ['Trump', 'Hillary', 'Settings', 'Credit']
        self.icons = [self.ids['Trump'], self.ids['Hillary'], self.ids['Settings'], self.ids['Credit']]

        for i in range(0,4):
            self.icons[i].late_init(**{'name': names[i],
                                       'pos_hint': {'x': self.POSITIONS_X[i], 'y': self.POSITIONS_Y[i]},
                                       'size_hint': self.SIZE})
            self.icons[i].show()

        self.game = elections_game.ElectionsGame(sm, name="electionsgame")
        self.settings = SettingsScreen(sm, name='settings', menu=self)
        self.credit = CreditScreen(sm, name='credit', menu=self)
        self.sm = sm

        self.icons[0].bind(on_press=self.pressed_trump)
        self.icons[1].bind(on_press=self.pressed_hillary)
        self.icons[2].bind(on_press=self.pressed_setting)
        self.icons[3].bind(on_press=self.pressed_credit)

    def pressed_trump(self, *args):
        """Trump choice callback."""
        self.game.set_bot('hillary')
        self.sm.switch_to(self.game)


    def pressed_hillary(self, *args):
        """Hillary choice callback."""
        self.game.set_bot('trump')
        self.sm.switch_to(self.game)


    def pressed_setting(self, *args):
        if not self.sm.has_screen('settings'):
            self.sm.add_widget(self.settings)
        self.sm.current = 'settings'


    def pressed_credit(self, *args):
        if not self.sm.has_screen('credit'):
            self.sm.add_widget(self.credit)

        self.sm.current = 'credit'