from sprite import Sprite
from constants import SCREENW, SCREENH

class Turret(Sprite):
    def __init__(self, img):
        Sprite.__init__(self,
                        SCREENW/2,
                        SCREENH/2,
                        img)
