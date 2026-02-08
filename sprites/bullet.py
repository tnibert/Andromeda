from behaviors.trajectory import TrajectoryMovementBehavior
from sprite import Sprite
from constants import UP, BULLETSPEED, SCREENH
from sprites import boss
from statemachine import State, StateMachine
from typeset import TypeSet


class Bullet(Sprite):
    def __init__(self, x, y, img, direction, origin=None):
        """

        :param x:
        :param y:
        :param img:
        :param direction: The direction the bullet is traveling
        :param origin: the object that fired the bullet, prevents us from damaging ourselves
        """
        super().__init__(x, y, img, StateMachine(State(self, TypeSet({TrajectoryMovementBehavior(0 if direction == UP else 180, BULLETSPEED, self)}))))
        self.origin = origin

    def update(self):
        super().update()
        if self.y+self.image.get_height() > SCREENH or self.y < 0:
            self.notify("remove")

    def on_collide(self, event):
        pass
        # if isinstance(event.source, boss.Boss) \
        #         and event.kwargs.get("who") is self \
        #         and not self.exploding \
        #         and self.origin is not event.source:
        #     self.start_exploding()
        #     self.x = self.x - self.image.get_width()/2
        #     self.y = self.y - self.image.get_height()/2
        #
        #     # best to not divide actions between boss and bullet
        #     # any scenario where the bullet explodes should be handled in this function
        #     if event.source.health > 0:
        #         event.source.health -= 1
        #         event.source.notify("health_down", value=-1)
