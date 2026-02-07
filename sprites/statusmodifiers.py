from behaviors.trajectory import TrajectoryMovementBehavior
from sprite import Sprite
from constants import SCREENW, SCREENH, STATMOD_DURATION, PLAYERSPEED, PLAYERMAXSPEED, STATMOD_SPEED
from statemachine import State
from timer import Timer
import random

from typeset import TypeSet


# todo: handling of timers with acquisition of multiple power ups in player and gamemap
# is a bit out of whack
# If you receive multiple power ups, the status will be reset at the end of the timer of
# the first power up received

# todo: restore bouncing off sides of screen?

# power ups and downs, to be inherited from
class StatusModifier(Sprite):
    def __init__(self, img):
        Sprite.__init__(self, random.randrange(0, SCREENW), -1 * img.get_height(), img,
                        State(self, TypeSet({TrajectoryMovementBehavior(random.randrange(100, 260), STATMOD_SPEED, self)})))

    def payload(self, target):
        self.notify("remove")

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.notify("remove")


class TimeableStatmod(StatusModifier):
    def __init__(self, img):
        super().__init__(img)
        self.timer = Timer(self)

    def payload(self, target):
        self.timer.startwatch(STATMOD_DURATION)
        super().payload(target)


# +1 life
class OneUp(StatusModifier):
    def payload(self, target):
        # add some sort of happy animation
        target.oneup()
        super().payload(target)


# bomb booby trap, -1 life
class Bomb(StatusModifier):
    def payload(self, target):
        target.die()  # initiate explosion
        super().payload(target)


# double background and ship speed
class SpeedUp(TimeableStatmod):
    def payload(self, target):
        target.speed = PLAYERMAXSPEED
        super().payload(target)

    def reverse(self, target):
        target.speed = PLAYERSPEED


# shoot from 3 locations
class MoreGuns(TimeableStatmod):
    def payload(self, target):
        target.bamfmode = True
        super().payload(target)

    def reverse(self, target):
        target.bamfmode = False
