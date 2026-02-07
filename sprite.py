from gameobject import GameObject
from properties import PROP_COLLISION


class Sprite(GameObject):
    def __init__(self, x, y, img, state_machine=None):
        GameObject.__init__(self, x, y, img, state_machine, {PROP_COLLISION})
