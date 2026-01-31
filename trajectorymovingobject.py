from moveableobject import MoveableObject
from events import EVT_ACT
from behaviors.trajectory import TrajectoryMovementBehavior
import random


class TrajectoryMovingObject(MoveableObject):
    """
    A gameobject that moves on a trajectory
    todo: this is still used for status modifiers
    """
    def __init__(self, x, y, speed, img):
        MoveableObject.__init__(self, x, y, speed, img, [TrajectoryMovementBehavior(random.randrange(100, 260), self)])
