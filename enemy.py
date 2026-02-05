from behaviors.explosion import ExplodeBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from events import EVT_START_EXPLOSION
from sprite import Sprite
from constants import SCREENW, SCREENH, SAUCER_DEATH_SCORE_INC
from player import Player
from bullet import Bullet
import random

from typeset import NoElementPresent


class Enemy(Sprite):
    def __init__(self, img):
        explosion_behavior = ExplodeBehavior(self)
        Sprite.__init__(self, random.randrange(0, SCREENW),  # x location
                        -3 * img.get_height(),  # y location
                        img,
                        {TrajectoryMovementBehavior(random.randrange(100, 260), random.randrange(60, 100), self), explosion_behavior})
        self.subscribe(EVT_START_EXPLOSION, explosion_behavior.start_exploding)
        self.exit_stage = False
        self.dying = False  # todo: state machine
        self.orig_image = self.image

    def update(self):
        super().update()

        # todo: move edge detection to a behavior
        try:
            movement = self.behaviors.retrieve_instance(TrajectoryMovementBehavior)
            if self.x > SCREENW - self.width and movement.degreeangle > 180:
                self.queue_discard_behavior(TrajectoryMovementBehavior)
                self.queue_attach_behavior(TrajectoryMovementBehavior(random.randrange(100, 160), random.randrange(60, 100), self))
            elif self.x < 0 and movement.degreeangle < 180:
                self.queue_discard_behavior(TrajectoryMovementBehavior)
                self.queue_attach_behavior(TrajectoryMovementBehavior(random.randrange(200, 260), random.randrange(60, 100), self))
        except NoElementPresent:
            print("trajectory movement has been removed")

        # todo: randomly change direction mid screen

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
            self.queue_attach_behavior(TrajectoryMovementBehavior(random.randrange(100, 260), random.randrange(60, 100), self))
        else:
            self.notify("remove")

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if not self.dying:
                if isinstance(event.source, Player):
                    print("on_collide player")
                    self.dying = True
                    self.queue_discard_behavior(TrajectoryMovementBehavior)
                    self.notify(EVT_START_EXPLOSION)
                elif isinstance(event.source, Bullet):
                    print("on_collide bullet")
                    self.dying = True
                    self.queue_discard_behavior(TrajectoryMovementBehavior)
                    self.notify(EVT_START_EXPLOSION)
                    event.source.notify("remove")

    def leave(self):
        """
        Set flag to leave the game scene on screen exit
        :return:
        """
        self.exit_stage = True
