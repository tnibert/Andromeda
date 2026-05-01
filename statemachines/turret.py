from behaviors.collision import CollisionBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.scoreup import ScoreUpBehavior
from behaviors.trackingrotation import TrackingRotationBehavior
from behaviors.fire import TimedFireBehavior
from behaviors.sceneremove import SceneRemoveBehavior
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION, EVT_SCORE_UP
from statemachine import State, StateMachine
from typeset import TypeSet
from constants import SCREENH

def turret_state_graph(target, player) -> StateMachine:
    # states
    initial = State(target,
                    TypeSet({
                        CollisionBehavior(target),
                        TrackingRotationBehavior(target, player),
                        TimedFireBehavior(target),
                    }),
                    name="initial")

    exploding = State(target,
                      TypeSet({ExplodeBehavior(target)}),
                      name="exploding")

    score_up = State(target,
                     TypeSet({ScoreUpBehavior(target)}),
                     name="score_up")

    exit_scene = State(target,
                       TypeSet({SceneRemoveBehavior(target)}),
                       name="exit_state")

    # edges
    initial.transitions = {
        EVT_START_EXPLOSION: exploding,
        lambda t: t.y > SCREENH: exit_scene
    }
    exploding.transitions = {
        EVT_EXPLOSION_FINISH: score_up,
    }
    score_up.transitions = {
        EVT_SCORE_UP: exit_scene,
    }

    state_machine = StateMachine(initial)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_SCORE_UP, state_machine.state_transition_event)

    return state_machine
