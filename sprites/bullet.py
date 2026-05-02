from behaviors.trajectory import TrajectoryMovementBehavior
from core.sprite import Sprite
from constants import BULLETSPEED, SCREENH
from core.statemachine import State, StateMachine
from core.typeset import TypeSet


class Bullet(Sprite):
    def __init__(self, x, y, img, direction, origin=None):
        """

        :param x:
        :param y:
        :param img:
        :param direction: The direction the bullet is traveling
        :param origin: the object that fired the bullet, prevents us from damaging ourselves
        """
        super().__init__(x, y, img, StateMachine(State(self, TypeSet({TrajectoryMovementBehavior(direction, BULLETSPEED, self)}))))
        self.origin = origin

    def update(self):
        super().update()
        if self.y+self.image.get_height() > SCREENH or self.y < 0:
            self.notify("remove")

    def on_collide(self, event):
        pass
