import random

from behaviors.collision import CollisionBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.sceneremove import SceneRemoveBehavior
from behaviors.scoreup import ScoreUpBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from constants import SCREENH, LEFT, DOWN
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION, EVT_RESPAWN_FINISH, EVT_SCORE_UP
from core.statemachine import State, StateMachine
from core.typeset import TypeSet


def cut_cross_enemy_state_graph(target) -> StateMachine:
    """
    Moves like:
         |
         |
    ------
    |
    |
    """
    # set up nodes
    down = State(target,
                    TypeSet({
                        TrajectoryMovementBehavior(DOWN, random.randrange(60, 100), target),
                        CollisionBehavior(target),
                    }), name="down")

    left = State(target,
                    TypeSet({
                        TrajectoryMovementBehavior(LEFT, random.randrange(60, 100), target),
                        CollisionBehavior(target),
                    }), name="left")

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
    down.transitions = {
        lambda t: t.y > SCREENH: exit_scene,
        lambda t: t.y > SCREENH/2 and t.x > 100: left,
        EVT_START_EXPLOSION: exploding,
    }

    left.transitions = {
        lambda t: t.x <= 100: down,
        EVT_START_EXPLOSION: exploding,
    }

    exploding.transitions = {
        EVT_EXPLOSION_FINISH: score_up,
    }

    score_up.transitions = {
        EVT_SCORE_UP: exit_scene,
    }

    state_machine = StateMachine(down)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_RESPAWN_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_SCORE_UP, state_machine.state_transition_event)

    return state_machine
