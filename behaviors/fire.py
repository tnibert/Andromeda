from timer import Timer
from loadstaticres import bulletimg
from events import EVT_TIMEOUT, EVT_FIRE
from sprites.bullet import Bullet
import random

class FireBehavior:
    def __init__(self, target):
        """
        todo: the trigger behavior needs to be made generic to apply this behavior to different sprites
        :param target:
        """
        self.target = target
        self.timer = Timer()
        self.timer.subscribe(EVT_TIMEOUT, self.fire_bullet)
        self.timer.startwatch(random.randrange(1, 5))

    def act(self):
        self.timer.tick()

    def fire_bullet(self, event):
        print("fire bullet")
        bullet = Bullet(self.target.x, self.target.y, bulletimg, self.target.rotation, self.target)
        self.target.notify(EVT_FIRE, bullet=bullet)
        self.timer.startwatch(random.randrange(1, 5))
