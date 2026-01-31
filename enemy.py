from behaviors.explosion import ExplodeBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from moveableobject import MoveableObject
from constants import SCREENW, SCREENH, SAUCER_DEATH_SCORE_INC
from player import Player
from bullet import Bullet
import random


class Enemy(MoveableObject):
    def __init__(self, img):
        explosion_behavior = ExplodeBehavior(self)
        MoveableObject.__init__(self, random.randrange(0, SCREENW), # x location
                                        -3 * img.get_height(),              # y location
                                        random.randrange(60, 100),          # speed
                                        img,
                                        [TrajectoryMovementBehavior(random.randrange(100, 260), self), explosion_behavior])
        self.subscribe("start_explosion", explosion_behavior.start_exploding)
        self.exit_stage = False
        self.dying = False

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.respawn()

    def respawn(self, event=None):
        """
        Respawn if not set to exit
        :return:
        """
        self.notify("score_up", value=SAUCER_DEATH_SCORE_INC)
        self.dying = False
        if not self.exit_stage:
            self.image = self.orig_image
            self.x = random.randrange(0, SCREENW)
            self.y = -3 * self.image.get_height()
            self.speed = random.randrange(60, 100)
        else:
            self.notify("remove")

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if not self.dying:
                if isinstance(event.source, Player):
                    print("on_collide player")
                    self.dying = True
                    self.notify("start_explosion")
                elif isinstance(event.source, Bullet):
                    print("on_collide bullet")
                    self.dying = True
                    self.notify("start_explosion")
                    event.source.notify("remove")

    def leave(self):
        """
        Set flag to leave the game scene on screen exit
        :return:
        """
        self.exit_stage = True
