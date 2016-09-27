import kivy
import kwad
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from elections_game import ElectionsGame


class Icon(Button):
    def __init__(self, **kwargs):
        self.game = None
        self.name = None
        self.image = None
        super(Icon, self).__init__()

    def late_init(self, **kwargs):
        self.name = kwargs['name']
        self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        self.background_normal = self.image
        self.background_down = self.image

class StartScreen(Screen):
    POSITIONS_X = {0: 650 / 2048.0,
                   1: 1050 / 2048.0}
    POSITIONS_Y = {0: (1536.0 - 1000.0) / 1536.0,
                   1: (1536.0 - 1000.0) / 1536.0}


    def __init__(self, sm, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        trump_data = {'name': 'Trump', 'image': 'assets/Trump.png'}
        hillary_data = {'name': 'Hillary', 'image': 'assets/Hillary.png'}
        datas = [trump_data, hillary_data]
        self.icon_trump = self.ids['IconTrump']
        self.icon_hillary = self.ids['IconHillary']
        self.icons = [self.icon_trump, self.icon_hillary]

        self.game = ElectionsGame(name="electionsgame")
        self.sm = sm
        sm.add_widget(self)
        sm.add_widget(self.game)

        for i in [0, 1]:
            self.icons[i].late_init(**datas[i])
            self.icons[i].show()
            self.icons[i].pos_hint = {'x': self.POSITIONS_X[i],
                                      'y': self.POSITIONS_Y[i]}
            self.icons[i].render()

        self.icons[0].bind(on_press=self.pressed_trump)
        self.icons[1].bind(on_press=self.pressed_hillary)

    def pressed_trump(self, *args):
        self.game.set_bot('hillary')
        self.sm.current = "electionsgame"

    def pressed_hillary(self, *args):
        self.game.set_bot('trump')
        self.sm.current = "electionsgame"