import random

from behaviors.collision import CollisionBehavior
from behaviors.edgedetection import EdgeDetectionBehavior
from behaviors.enemy.respawn import EnemyRespawnBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from constants import SCREENH
from events import EVT_TIMEOUT, EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION, EVT_RESPAWN_FINISH
from statemachine import State
from typeset import TypeSet


def default_enemy_state_graph(target, explosion_behavior: ExplodeBehavior) -> State:
    # set up nodes
    respawn = State(target,
                    TypeSet({EnemyRespawnBehavior(target)}), name="respawn")

    initial = State(target,
                    TypeSet({
                        TrajectoryMovementBehavior(random.randrange(100, 260), random.randrange(60, 100), target),
                        EdgeDetectionBehavior(target.change_direction, target),
                        CollisionBehavior(target),
                    }), name="initial")

    exploding = State(target,
                      TypeSet({explosion_behavior}), name="exploding")

    exit_scene = State(target,
                       TypeSet({}), name="exit scene")

    # set up edges
    initial.transitions = {
        lambda t: t.y > SCREENH: respawn,
        EVT_START_EXPLOSION: exploding,
        lambda t: t.exit_stage: exit_scene
    }
    target.subscribe(EVT_START_EXPLOSION, initial.state_transition_event)
    respawn.transitions = {
        EVT_RESPAWN_FINISH: initial,
        lambda t: t.exit_stage: exit_scene
    }
    target.subscribe(EVT_RESPAWN_FINISH, respawn.state_transition_event)
    exploding.transitions = {
        EVT_EXPLOSION_FINISH: respawn,
        lambda t: t.exit_stage: exit_scene
    }
    target.subscribe(EVT_EXPLOSION_FINISH, exploding.state_transition_event)

    return initial
