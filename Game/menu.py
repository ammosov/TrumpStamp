from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Ellipse, Rectangle


class MenuWindow(Widget):
    def __init__(self, **kwargs):
        super(MenuWindow, self).__init__(**kwargs)


class MenuButton(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        # self.sm = sm
        super(MenuButton, self).__init__(**kwargs)

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def on_press(self):
        with self.canvas:
            Ellipse(source='assets/buttons/btn_menu_active.png', pos=self.pos, size=self.size)
        window = MenuWindow()
        with window.canvas:
            Rectangle(source='assets/menu/menu_00.png',
                      size=(0.5 * self.parent.size[0], 0.5 * self.parent.size[1]),
                      pos=(0.25 * self.parent.size[0], 0.25 * self.parent.size[1]))
        self.parent.add_widget(window)


