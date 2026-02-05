import math

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
        self.target.x -= (((math.degrees(math.sin(math.radians(self.degreeangle))) * self.speed) / 40) * self.target.frame_tick)
        self.target.y -= (((math.degrees(math.cos(math.radians(self.degreeangle))) * self.speed) / 40) * self.target.frame_tick)
