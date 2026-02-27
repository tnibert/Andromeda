import random

from behaviors.collision import CollisionBehavior
from behaviors.edgedetection import EdgeDetectionBehavior
from behaviors.respawn import RespawnBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from constants import SCREENH, SCREENW
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION, EVT_RESPAWN_FINISH
from statemachine import State, StateMachine
from typeset import TypeSet


def default_enemy_state_graph(target) -> StateMachine:
    def respawn_proc():
        if target.exit_stage:
            target.notify("remove")

    # set up nodes
    respawn = State(target,
                    TypeSet({RespawnBehavior(target,
                                             target.image,
                                             lambda: random.randrange(0, SCREENW),
                                             lambda: -3 * target.image.get_height(),
                                             respawn_proc)}),
                    name="respawn")

    initial = State(target,
                    TypeSet({
                        TrajectoryMovementBehavior(random.randrange(100, 260), random.randrange(60, 100), target),
                        EdgeDetectionBehavior(target.change_direction, target),
                        CollisionBehavior(target),
                    }), name="initial")

    exploding = State(target,
                      TypeSet({ExplodeBehavior(target)}), name="exploding")

    exit_scene = State(target,
                       TypeSet({
                           TrajectoryMovementBehavior(180, random.randrange(60, 100), target)
                       }), name="exit scene")

    # set up edges
    initial.transitions = {
        lambda t: t.y > SCREENH: respawn,
        EVT_START_EXPLOSION: exploding,
        lambda t: t.exit_stage: exit_scene
    }
    respawn.transitions = {
        EVT_RESPAWN_FINISH: initial,
        lambda t: t.exit_stage: exit_scene
    }
    exploding.transitions = {
        EVT_EXPLOSION_FINISH: respawn,
        lambda t: t.exit_stage: exit_scene
    }

    state_machine = StateMachine(initial)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_RESPAWN_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)

    return state_machine
