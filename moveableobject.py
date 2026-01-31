from constants import EXPLOSION_FRAME_UPDATE_WAIT
from loadstaticres import explosion
from gameobject import GameObject
from timer import Timer


# all sprites inherit from this class
class MoveableObject(GameObject):
    def __init__(self, x, y, speed, img, behaviors=None):
        GameObject.__init__(self, x, y, img, behaviors)
        self.orig_image = self.image
        self.speed = speed
