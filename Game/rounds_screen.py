from __future__ import print_function
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
import elections_game
import os
import csv
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.widget import Widget
from functools import partial

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

states_csv = os.path.join(SCRIPT_DIR, 'db_states.csv')


class RoundsIcon(Button):
    """Icon class."""

    def __init__(self, **kwargs):
        """Init icon."""
        self.name = None  # kwargs['name']
        super(RoundsIcon, self).__init__()

    def late_init(self, **kwargs):
        """Populate icon."""
        self.name = kwargs['name']
        # self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        """Set background image."""
        pass


class StatesScroll(ScrollView):
    def __init__(self, **kwargs):
        super(StatesScroll, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

    def late_init(self, dist_scroll, **kwargs):
        self.dist_scroll = dist_scroll
        self.states_db = kwargs['states_db']
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

        states = np.unique(np.array([self.states_db[i]['state'] for i in range(len(self.states_db))]))
        # states = np.unique(np.array(states_db[[1]]))
        for i in range(len(states)):
            btn = Button(text=str(states[i]), size_hint_y=None, height=40, font_size=22, background_color=[1,1,1,0.])
            #g = TextInput(i)

            buttoncallback = partial(self.on_press, i)
            btn.bind(on_press=buttoncallback)
            self.layout.add_widget(btn)
        self.add_widget(self.layout)

    def on_press(self, *args):
        self.dist_scroll.update_widgets(self.states_db[args[0]]['state'])


class DistrictsScroll(ScrollView):
    def __init__(self, **kwargs):
        super(DistrictsScroll, self).__init__(**kwargs)
        self.layouts = None

    def update_widgets(self, state_name):
        for child in self.children[:]:
            self.remove_widget(child)
        curr_state_layout = self.layouts[state_name]

        self.add_widget(curr_state_layout)

    def late_init(self, desc_scroll, **kwargs):
        self.desc_scroll = desc_scroll
        self.states_db = kwargs['states_db']
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

        states = np.unique(np.array([self.states_db[i]['state'] for i in range(len(self.states_db))]))

        self.layouts = {states[i]: GridLayout(cols=1, spacing=10, size_hint_y=None) for i in range(len(states))}
        for state_name, layout in self.layouts.items():
            layout.bind(minimum_height=layout.setter('height'))
            areas = [self.states_db[i]['district'] for i in range(len(self.states_db)) if
                     self.states_db[i]['state'] == state_name]
            print (len(areas))
            for i in range(len(areas)):
                btn = Button(text=str(areas[i]), size_hint_y=None, height=40, font_size=22, background_color=[1,1,1,0.])
                # btn.bind(on_press=setattr(self.desc_scroll, '_district_selected', self.states_db[i]['state']))
                layout.add_widget(btn)

class DescriptionScroll(ScrollView):
    def __init__(self, **kwargs):
        super(DescriptionScroll, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)

    def late_init(self, **kwargs):
        self.states_db = kwargs['states_db']
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

class RoundsScreen(Screen):

    POSITIONS_X = {0: 328 / 2048.0,
                   1: 1228 / 2048.0}
    POSITIONS_Y = {0: (1536. - 1400) / 1536.0}
    SIZES = {0: (730 / 2048.0, (1536 - 1340) / 1536.0)}

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(RoundsScreen, self).__init__(**kwargs)
        self.sm = sm
        self.name = kwargs['name']
        self.menu_screen = kwargs['menu']

        self.back_button = self.ids['Back']

        self.back_button.late_init(**{'name': 'Back', 'image': 'assets/settings/btn_back_active.png'})
        self.back_button.bind(on_press=self.pressed_back)
        self.back_button.pos_hint = {'x': self.POSITIONS_X[0],
                                     'y': self.POSITIONS_Y[0]}
        self.back_button.size_hint = self.SIZES[0]
        self.back_button.render()
        self.back_button.show()

        self.play_button = self.ids['Play']
        self.play_button.late_init(**{'name': 'Play'})
        self.play_button.bind(on_press=self.pressed_play)
        self.play_button.pos_hint = {'x': self.POSITIONS_X[1],
                                     'y': self.POSITIONS_Y[0]}
        self.play_button.size_hint = self.SIZES[0]

        self.game = None
        states_db = []
        with open(states_csv) as states_file:
            reader = csv.DictReader(states_file)
            for row in reader:
                row_ = {k: v for k, v in row.iteritems()}
                states_db.append(row_)

        self.states_scroll = self.ids['StatesScroll']
        self.dist_scroll = self.ids['DistrictsScroll']
        self.descr_scroll = self.ids['DescriptionScroll']

        self.state_selected = None
        self.area_selected = None
        # self.states_scroll.late_init(size=(Window.width / 4, Window.height/ 2), pos=(Window.width / 6, Window.height/ 3))
        self.descr_scroll.late_init(size_hint=(((2048.0 - 400) / 3) / 2048.0, 880 / 2048.0),
                                    pos_hint={'x': (138 + 2 * ((2048.0 - 400) / 3) + 120) / 2048.0,
                                              'y': 400.0 / 1536.0},
                                    states_db=states_db)
        self.dist_scroll.late_init(self.descr_scroll, size_hint=(((2048.0 - 400) / 3) / 2048.0, 880 / 2048.0),
                                   pos_hint={'x': (138 + ((2048.0 - 400) / 3) + 60) / 2048.0, 'y': 400.0 / 1536.0},
                                   states_db=states_db)
        self.states_scroll.late_init(self.dist_scroll, size_hint=(((2048.0 - 400) / 3) / 2048.0, 880 / 2048.0),
                                     pos_hint={'x': 138 / 2048.0, 'y': 400.0 / 1536.0},
                                     states_db=states_db)
      
        self.set_new_game()

    def pressed_back(self, *args):
        # self.sm.add_widget(self.menu_screen)
        self.sm.current = 'startscreen'
        # print "pressed back"
        # self.sm.switch_to(self.menu_screen)

    def set_new_game(self):
        self.game = elections_game.ElectionsGame(self.sm, name="electionsgame")

    def set_bot(self, bot_name):
        self.game.set_bot(bot_name)

    def pressed_play(self, *args):
        self.sm.switch_to(self.game)

    def set_round(self, round_id):
        self.game.set_round(round_id)
