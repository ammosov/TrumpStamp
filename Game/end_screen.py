from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
import start_screen


class NewGameIcon(Button):
    def __init__(self, **kwargs):
        self.image = None
        super(NewGameIcon, self).__init__()

    def late_init(self, **kwargs):
        self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        self.background_normal = self.image
        self.background_down = self.image


class EndScreen(Screen):
    POSITIONS_X = {0: 700 / 2048.0}
    POSITIONS_Y = {0: 697 / 1536.0}

    SIZES = {0: (640 / 2048.0, 170 / 1536.0)}

    def __init__(self, sm, winner_name, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        self.winner_name = winner_name
        trump_wins = {'image': 'assets/Trump.png'}
        hillary_wins = {'image': 'assets/Hillary.png'}
        new_game_icon_image = {'image': 'assets/out.png'}
        self.new_game_icon = self.ids['NewGame']

        self.sm = sm

        self.new_game_icon.late_init(**new_game_icon_image)
        self.new_game_icon.show()
        self.new_game_icon.pos_hint = {'x': self.POSITIONS_X[0],
                                       'y': self.POSITIONS_Y[0]}
        self.new_game_icon.size_hint = self.SIZES[0]
        self.new_game_icon.render()

        self.new_game_icon.bind(on_press=self.pressed_new_game)

    def pressed_new_game(self, *args):
        start_screen_ = start_screen.StartScreen(self.sm, name="startscreen")
        self.sm.switch_to(start_screen_)