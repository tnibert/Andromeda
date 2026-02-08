from behaviors.explosion import ExplodeBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from events import EVT_START_EXPLOSION
from sprite import Sprite
from constants import SCREENW, RIGHT, LEFT
from sprites.player import Player
from sprites.bullet import Bullet
import random

from statemachines.defaultenemy import default_enemy_state_graph
from typeset import NoElementPresent


class Enemy(Sprite):
    def __init__(self, img):
        Sprite.__init__(self, random.randrange(0, SCREENW),  # x location
                        -3 * img.get_height(),  # y location
                        img)
        explosion_behavior = ExplodeBehavior(self)
        self.state_machine = default_enemy_state_graph(self, explosion_behavior)

        self.exit_stage = False

        self.orig_image = self.image

    def update(self):
        super().update()

    def change_direction(self, direction):
        try:
            movement = self.state_machine.current_state.behaviors.retrieve_instance(TrajectoryMovementBehavior)
        except NoElementPresent:
            print("trajectory movement has been removed")
            return

        if direction == RIGHT and movement.degreeangle > 180:
            self.state_machine.current_state.queue_discard_behavior(TrajectoryMovementBehavior)
            self.state_machine.current_state.queue_attach_behavior(
                TrajectoryMovementBehavior(random.randrange(100, 160), random.randrange(60, 100), self))
        elif direction == LEFT and movement.degreeangle < 180:
            self.state_machine.current_state.queue_discard_behavior(TrajectoryMovementBehavior)
            self.state_machine.current_state.queue_attach_behavior(
                TrajectoryMovementBehavior(random.randrange(200, 260), random.randrange(60, 100), self))

    def respawn(self, event=None):
        """
        Respawn if not set to exit
        :return:
        """
        if self.exit_stage:
            self.notify("remove")

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if isinstance(event.source, Player):
                #print("on_collide player")
                self.notify(EVT_START_EXPLOSION)
            elif isinstance(event.source, Bullet):
                #print("on_collide bullet")
                self.notify(EVT_START_EXPLOSION)
                event.source.notify("remove")

    def leave(self):
        """
        Set flag to leave the game scene on screen exit
        :return:
        """
        self.exit_stage = True
