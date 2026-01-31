from moveableobject import MoveableObject
from events import EVT_ACT
from behaviors.trajectory import TrajectoryMovementBehavior
import random


class TrajectoryMovingObject(MoveableObject):
    """
    A gameobject that moves on a trajectory
    """
    def __init__(self, x, y, speed, img):
        MoveableObject.__init__(self, x, y, speed, img)
        self.subscribe(EVT_ACT, TrajectoryMovementBehavior(random.randrange(100, 260)).act)

    def move(self):
        self.notify(EVT_ACT, sprite=self)

    def update(self):
        super().update()
        self.move()
