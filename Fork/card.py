from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import pandas as pd
import os


class Card(Button, Widget):
    def __init__(self, **kwargs):
        self.card_id = None
        self.description = None
        self.name = None
        self.image = None
        self.cost_color = None
        self.cost_value = None
        self.actions = None
        self.in_play = False
        self.sound = None
        self.background_normal = None
        super(Card, self).__init__(**kwargs)

    def lazy_init(self, **kwargs):
        self.card_id = kwargs['id']
        self.description = kwargs['description']
        self.name = kwargs['title']
        self.image = kwargs['image_path']
        self.cost_color = kwargs['cost_color']
        self.cost_value = kwargs['cost_value']
        self.actions = kwargs['actions']
        self.background = kwargs['background']
        self.sound = SoundLoader.load(kwargs['sound'])

    def __repr__(self):
        return '{0} = {4}{1} ({2}/{3}) ({5})'.format(self.card_id, self.name,
                                                     self.cost_color, self.cost_value,
                                                     '-!-' if self.playable else '', self.description)

    def get_cost(self):
        return self.cost_color, self.cost_value

    def get_actions(self):

        pass

    def play_sound(self):
        self.sound.play()


class CardFabric(object):
    def __init__(self, card_db, images_path=None, sound_path=None, background_path=None):
        self.db = pd.read_csv(card_db)
        self.images_path = images_path or {'trump': 'assets/cards/trump',
                                           'hillary': 'assets/cards/hillary'}
        self.sound_path = sound_path or 'assets/stubs/Sounds/card.wav'
        self.background_path = background_path or 'assets/card00.png'

    def get_card(self, card_id, owner_id):
        card_data = dict(self.db.iloc[card_id - 1])
        card_data['description'] = card_data['description'].replace('*', '; ')
        if owner_id == 0:
            card_data['title'] = card_data['t_title'].replace('*', ' ')
            card_data['image_path'] = os.path.join(self.images_path['trump'], str(card_data['img_t'])) + '.png'
        elif owner_id == 1:
            card_data['title'] = card_data['h_title'].replace('*', ' ')
            card_data['image_path'] = os.path.join(self.images_path['hillary'], str(card_data['img_h'])) + '.png'
        else:
            raise ValueError('Wrong owner_id')
        actions = {'1': [card_data['act1_value'], card_data['act1_type'], card_data['act1_side']],
                   '2': [card_data['act2_value'], card_data['act2_type'], card_data['act2_side']],
                   '3': [card_data['act3_value'], card_data['act3_type'], card_data['act3_side']]}
        actions = filter(lambda (k, v): v[0] != 0, actions.items())
        card_data['actions'] = actions
        card_data['sound'] = self.sound_path
        card_data['background'] = self.background_path

        card = Card()
        card.lazy_init(**card_data)
        return card


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    cards = CardFabric(os.path.join(SCRIPT_DIR, 'cards.csv'))
    print cards.get_card(31, owner_id=0)
    print cards.get_card(31, owner_id=1)
