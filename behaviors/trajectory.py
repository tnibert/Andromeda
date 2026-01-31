from constants import SCREENW
import math
import random

class TrajectoryMovementBehavior:
    def __init__(self, angle: int, target):
        # angle randomly ranges from 100 degrees to 260, 0 degrees is vertical axis
        self.degreeangle = angle
        self.target = target

    def act(self):
        # screen edge checking
        if (self.target.x > SCREENW - self.target.width and self.degreeangle > 180) or random.randrange(0, 2000) == 1467:
            self.degreeangle = random.randrange(100, 160)

        elif (self.target.x < 0 and self.degreeangle < 180) or random.randrange(0, 2000) == 200:
            self.degreeangle = random.randrange(200, 260)

        self.target.x -= (((math.degrees(math.sin(math.radians(self.degreeangle))) * self.target.speed) / 40) * self.target.frame_tick)
        self.target.y -= (((math.degrees(math.cos(math.radians(self.degreeangle))) * self.target.speed) / 40) * self.target.frame_tick)
