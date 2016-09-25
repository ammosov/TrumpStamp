from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import pandas as pd
import os
import kwad


class Card(Button):
    def __init__(self, **kwargs):
        self.game = kwargs['game']
        self.card_id = kwargs['id']
        self.owner_id = kwargs['owner_id']
        self.description = kwargs['description']
        self.name = kwargs['title']
        self.image = kwargs['image_path']
        self.cost_color = kwargs['cost_color']
        self.cost_value = kwargs['cost_value']
        self.actions = kwargs['actions']
        self.background = kwargs['background']
        self.background_normal = self.background
        self.background_down = self.background
        self.sound = SoundLoader.load(kwargs['sound'])
        self.counter_for_expand = 0
        self.touch_moving = False
        super(Card, self).__init__()

    def __repr__(self):
        return '{0} = {4}{1} ({2}/{3})'.format(self.card_id, self.name,
                                               self.cost_color, self.cost_value,
                                               self.description)

    def __eq__(self, other):
        return isinstance(other, Card) and other.card_id == self.card_id and other.owner_id == self.owner_id

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))
            self.game.add_widget(self)


    def show(self):
        self.background_normal = self.image
        self.background_down = self.image

    def hide(self):
        self.background_normal = self.background

    def get_owner(self):
        return self.owner_id

    def get_cost(self):
        return self.cost_color, self.cost_value

    # def on_press(self):
    #     #this counter don't trigger on time((
    #     self.counter_for_expand += 1
    #     self.game.resize_card(self, self.counter_for_expand)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("DOWN from {} touch {}".format(self.name, touch))
            self.orig_pos = touch.pos
            self.touch_moving = True
            return True

    def on_touch_move(self, touch):
        if self.touch_moving:
            print("MOVE from {} touch {}".format(self.name, touch))
            return True

    def on_touch_up(self, touch):
        if self.touch_moving:
            print("UP from {} touch {}".format(self.name, touch))
            if ((touch.pos[0] - self.orig_pos[0]) ** 2 +
                (touch.pos[1] - self.orig_pos[1]) ** 2) < 25:
                self.counter_for_expand += 1
                self.game.resize_card(self, self.counter_for_expand)                
            if touch.pos[1] - self.orig_pos[1] > 20:
                print("Clicked")
                self.game.card_clicked(self)
            if self.orig_pos[1] - touch.pos[1] > 20:
                if self.game.card_dropped(self):
                    print("Dropped")
                    self.drop_anim()
            self.touch_moving = False
            return True

    def drop_anim(self):
        def on_complete(obj, widget):
            self.game.remove_widget(self)
        x, y = self.pos_hint["x"], self.pos_hint["y"]
        anim = Animation(pos_hint={"x": x, "y": y - 0.1}, duration=0.2) + \
               Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=on_complete)
        anim.start(self)
        self.play_sound()

    def on_drop(self):
        print 'Card dropped'
        self.game.card_dropped(self)

    def move(self):
        print 'Card move to the board'
        anim = Animation(pos_hint={'x': 900.0 / 2048.0, 'y': (1536.0 - 1000.0) / 1536.0}, duration=0.5)
               #Animation(size_hint=(300.0 / 2048.0, self.size_hint[1]), duration=0.5) & \
               #Animation(pos_hint={'x': 1125.0 / 2048.0, 'y': (1536.0 - 888.0) / 1536.0}, duration=0.5)
        anim.start(self)
        self.play_sound()

    def deny(self):
        print 'Card deny playing'

    def get_actions(self):  # {'player': [(type, value), (type, value)], 'opponent': [(type, value)]}
        actions = {'player': [],
                   'opponent': []}
        for action in self.actions:
            action_value = action[0]
            action_type = action[1]
            action_affects = action[2]
            action_ = (action_type, action_value)
            if action_affects == 0:
                actions['player'].append(action_)
            elif action_affects == 1:
                actions['opponent'].append(action_)
            else:
                actions['player'].append(action_)
                actions['opponent'].append(action_)
        return actions

    def play_sound(self):
        self.sound.play()


class CardFabric(object):
    def __init__(self, game, card_db, images_path=None, sound_path=None, background_path=None):
        self.db = pd.read_csv(card_db, dtype={'img_t': str, 'img_h': str})
        self.images_path = images_path or {'trump': 'assets/cards/trump',
                                           'hillary': 'assets/cards/hillary'}
        self.sound_path = sound_path or 'assets/stubs/Sounds/card.wav'
        self.background_path = background_path or 'assets/card00.png'
        self.game = game

    def get_card(self, card_id, owner_id):
        card_data = dict(self.db.iloc[card_id - 1])
        card_data['owner_id'] = owner_id
        card_data['description'] = card_data['description'].replace('*', '; ')
        if owner_id == 0:
            card_data['title'] = card_data['t_title'].replace('*', ' ')
            card_data['image_path'] = os.path.join(self.images_path['trump'], card_data['img_t']) + '.png'
        elif owner_id == 1:
            card_data['title'] = card_data['h_title'].replace('*', ' ')
            card_data['image_path'] = os.path.join(self.images_path['hillary'], card_data['img_h']) + '.png'
        else:
            raise ValueError('Wrong owner_id')
        actions = [[card_data['act1_value'], card_data['act1_type'], card_data['act1_side']],
                   [card_data['act2_value'], card_data['act2_type'], card_data['act2_side']],
                   [card_data['act3_value'], card_data['act3_type'], card_data['act3_side']]]
        card_data['actions'] = actions
        card_data['sound'] = self.sound_path
        card_data['background'] = self.background_path

        card = Card(game=self.game, **card_data)
        return card


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    cards = CardFabric(None, os.path.join(SCRIPT_DIR, 'cards.csv'))