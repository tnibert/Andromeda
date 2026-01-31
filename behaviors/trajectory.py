from constants import SCREENW
import math
import random

class TrajectoryMovementBehavior:
    def __init__(self, angle: int):
        # angle randomly ranges from 100 degrees to 260, 0 degrees is vertical axis
        self.degreeangle = angle

    def act(self, event):
        # get target
        target = event.kwargs["sprite"]

        # screen edge checking
        if (target.x > SCREENW - target.width and self.degreeangle > 180) or random.randrange(0, 2000) == 1467:
            self.degreeangle = random.randrange(100, 160)

        elif (target.x < 0 and self.degreeangle < 180) or random.randrange(0, 2000) == 200:
            self.degreeangle = random.randrange(200, 260)

        target.x -= (((math.degrees(math.sin(math.radians(self.degreeangle))) * target.speed) / 40) * target.frame_tick)
        target.y -= (((math.degrees(math.cos(math.radians(self.degreeangle))) * target.speed) / 40) * target.frame_tick)
