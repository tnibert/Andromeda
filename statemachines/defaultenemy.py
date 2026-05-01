import random

from behaviors.collision import CollisionBehavior
from behaviors.edgedetection import EdgeDetectionBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.sceneremove import SceneRemoveBehavior
from behaviors.scoreup import ScoreUpBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from constants import SCREENH
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION, EVT_RESPAWN_FINISH, EVT_SCORE_UP
from statemachine import State, StateMachine
from typeset import TypeSet


def default_enemy_state_graph(target) -> StateMachine:
    # set up nodes
    initial = State(target,
                    TypeSet({
                        TrajectoryMovementBehavior(random.randrange(100, 260), random.randrange(60, 100), target),
                        EdgeDetectionBehavior(target.change_direction, target),
                        CollisionBehavior(target),
                    }), name="initial")

    exploding = State(target,
                      TypeSet({ExplodeBehavior(target)}),
                      name="exploding")

    score_up = State(target,
                     TypeSet({ScoreUpBehavior(target)}),
                     name="score_up")

    exit_scene = State(target,
                       TypeSet({SceneRemoveBehavior(target)}),
                       name="exit_state")

    # set up edges
    initial.transitions = {
        lambda t: t.y > SCREENH: exit_scene,
        EVT_START_EXPLOSION: exploding,
    }

    exploding.transitions = {
        EVT_EXPLOSION_FINISH: score_up,
    }

    score_up.transitions = {
        EVT_SCORE_UP: exit_scene,
    }

    state_machine = StateMachine(initial)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_RESPAWN_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_SCORE_UP, state_machine.state_transition_event)

    return state_machine
