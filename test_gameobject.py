import pygame
pygame.init()

from behaviors.trajectory import TrajectoryMovementBehavior
from gameobject import GameObject


# todo: game object should not require image, should only be relevant for sprite
class MockImage:
    def get_width(self):
        return 2

    def get_height(self):
        return 2

def test_discard_behavior():
    game_object = GameObject(0, 0, MockImage(), {TrajectoryMovementBehavior(0, 0, 0)})
    assert len(game_object.behaviors) == 1
    game_object.discard_behavior(TrajectoryMovementBehavior)
    assert len(game_object.behaviors) == 0

def test_attach_behavior():
    game_object = GameObject(0, 0, MockImage())
    assert len(game_object.behaviors) == 0
    game_object.attach_behavior(TrajectoryMovementBehavior(0, 0, 0))
    assert len(game_object.behaviors) == 1
