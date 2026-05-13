import math

from constants import SCREENW

CENTER = SCREENW/2

class CurveMovementBehavior:
    def __init__(self, speed, target):
        """

        :param speed:
        :param target:
        """
        self.target = target
        self.speed = speed

        self.amplitude_x = 100
        self.amplitude_y = 100

    def act(self):
        self.target.y += self.speed * self.target.frame_tick
        self.target.x = CENTER + math.sin(self.target.y / self.amplitude_y) * (-self.amplitude_x)
