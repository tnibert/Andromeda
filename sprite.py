from gameobject import GameObject
from properties import PROP_COLLISION

import pygame

class Sprite(GameObject):
    def __init__(self, x, y, img, state_machine=None):
        GameObject.__init__(self, x, y, img, state_machine, {PROP_COLLISION})

    def rotated(self, degrees):
        """
        return the sprite image rotated by degrees
        """
        return pygame.transform.rotate(self.image, degrees)
