from behaviors.collision import CollisionBehavior
from behaviors.explosion import ExplodeBehavior
from behaviors.trackingrotation import TrackingRotationBehavior
from events import EVT_EXPLOSION_FINISH, EVT_START_EXPLOSION
from statemachine import State, StateMachine
from typeset import TypeSet

def turret_state_graph(target, player) -> StateMachine:
    initial = State(target,
                    TypeSet({
                        CollisionBehavior(target),
                        TrackingRotationBehavior(target, player),
                    }),
                    name="initial")

    exploding = State(target,
                      TypeSet({ExplodeBehavior(target)}),
                      name="exploding")

    # todo: final state

    # todo: set up edges
    initial.transitions = {}
    exploding.transitions = {}

    state_machine = StateMachine(initial)
    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)

    return state_machine
