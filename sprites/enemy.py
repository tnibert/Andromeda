from behaviors.trajectory import TrajectoryMovementBehavior
from events import EVT_START_EXPLOSION, EVT_SCORE_UP
from core.sprite import Sprite
from constants import SCREENW, RIGHT, LEFT
from sprites.player import Player
from sprites.bullet import Bullet
import random

from core.typeset import NoElementPresent


class Enemy(Sprite):
    def __init__(self, img, initial_x, state_graph_fn):
        Sprite.__init__(self, initial_x, -3 * img.get_height(), img)
        self.state_machine = state_graph_fn(self)

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

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if isinstance(event.source, Player):
                self.notify(EVT_START_EXPLOSION)
            elif isinstance(event.source, Bullet):
                self.notify(EVT_START_EXPLOSION)
                event.source.notify("remove")

    def pre_scene_attach(self, scene, score_label, game_map):
        self.subscribe(EVT_SCORE_UP, score_label.update_value)
