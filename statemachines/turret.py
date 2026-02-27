from behaviors.collision import CollisionBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.trackingrotation import TrackingRotationBehavior
from behaviors.fire import FireBehavior
from behaviors.sceneremove import SceneRemoveBehavior
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION
from statemachine import State, StateMachine
from typeset import TypeSet
from constants import SCREENH

def turret_state_graph(target, player) -> StateMachine:
    # states
    initial = State(target,
                    TypeSet({
                        CollisionBehavior(target),
                        TrackingRotationBehavior(target, player),
                        FireBehavior(target),
                    }),
                    name="initial")

    exploding = State(target,
                      TypeSet({ExplodeBehavior(target)}),
                      name="exploding")

    exit_scene = State(target,
                       TypeSet({SceneRemoveBehavior(target)}),
                       name="exit_state")

    # edges
    initial.transitions = {
        EVT_START_EXPLOSION: exploding,
        lambda t: t.y > SCREENH: exit_scene
    }
    exploding.transitions = {
        EVT_EXPLOSION_FINISH: exit_scene
    }

    state_machine = StateMachine(initial)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)

    return state_machine
