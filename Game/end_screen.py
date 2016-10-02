from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
import start_screen


class EndGameIcon(Button):
    def __init__(self, **kwargs):
        self.image = None
        super(EndGameIcon, self).__init__()

    def late_init(self, **kwargs):
        self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        self.background_normal = self.image
        self.background_down = self.image


class EndScreen(Screen):
    POSITIONS_X = {0: 653 / 2048.0,
                   1: 668 / 2048.0}
    POSITIONS_Y = {0: 643 / 1536.0,
                   1: 980 / 1536.0}

    SIZES = {0: (740 / 2048.0, 240 / 1536.0),
             1: (715 / 2048.0, 157 / 1536.0)}

    def __init__(self, sm, winner_name, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        self.winner_name = winner_name
        new_game_image = {'image': 'assets/out.png'}
        winner_image = dict()
        if winner_name == 'Trump':
            winner_image['image'] = 'assets/out_trump.png'
        elif winner_name == 'Hillary':
            winner_image['image'] = 'assets/out_hillary.png'
        self.new_game_icon = self.ids['NewGame']
        self.winner_icon = self.ids['Winner']

        self.sm = sm

        self.new_game_icon.late_init(**new_game_image)
        self.new_game_icon.show()
        self.new_game_icon.pos_hint = {'x': self.POSITIONS_X[0],
                                       'y': self.POSITIONS_Y[0]}
        self.new_game_icon.size_hint = self.SIZES[0]
        self.new_game_icon.render()

        self.new_game_icon.bind(on_press=self.pressed_new_game)

        self.winner_icon.late_init(**winner_image)
        self.winner_icon.show()
        self.winner_icon.pos_hint = {'x': self.POSITIONS_X[1],
                                     'y': self.POSITIONS_Y[1]}
        self.winner_icon.size_hint = self.SIZES[1]
        self.winner_icon.render()

    def pressed_new_game(self, *args):
        start_screen_ = start_screen.StartScreen(self.sm, name="startscreen")
        self.sm.switch_to(start_screen_)