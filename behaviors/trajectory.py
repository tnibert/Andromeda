from constants import SCREENW
import math
import random

class TrajectoryMovementBehavior:
    def __init__(self, angle: int, speed, target):
        """

        :param angle: in degrees, 0 is vertical axis
        :param speed:
        :param target:
        """
        self.degreeangle = angle
        self.target = target
        self.speed = speed

    def act(self):
        # todo: move trajectory changing behavior to enemy.py, and/or an edge checking behavior
        # screen edge checking
        if (self.target.x > SCREENW - self.target.width and self.degreeangle > 180) or random.randrange(0, 2000) == 1467:
            self.degreeangle = random.randrange(100, 160)

        elif (self.target.x < 0 and self.degreeangle < 180) or random.randrange(0, 2000) == 200:
            self.degreeangle = random.randrange(200, 260)

        self.target.x -= (((math.degrees(math.sin(math.radians(self.degreeangle))) * self.speed) / 40) * self.target.frame_tick)
        self.target.y -= (((math.degrees(math.cos(math.radians(self.degreeangle))) * self.speed) / 40) * self.target.frame_tick)
