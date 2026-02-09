from behaviors.explosion import ExplodeBehavior
from behaviors.respawn import RespawnBehavior
from events import EVT_EXPLOSION_FINISH, EVT_RESPAWN_FINISH, EVT_START_EXPLOSION
from statemachine import StateMachine, State
from typeset import TypeSet


def default_player_state_graph(target, explosion_behavior: ExplodeBehavior) -> StateMachine:
    player_initial = State(target, TypeSet({}), name="player_initial")
    explode = State(target, TypeSet({explosion_behavior}), name="player_explode")

    spawn_x = target.x
    spawn_y = target.y
    respawn = State(target,
                    TypeSet({RespawnBehavior(target,
                                             target.image,
                                             lambda: spawn_x,
                                             lambda: spawn_y,
                                             target.respawn)}),
                    name="player_respawn")

    state_machine = StateMachine(player_initial)

    # set up edges
    player_initial.transitions = {
        EVT_START_EXPLOSION: explode,
    }
    respawn.transitions = {
        EVT_RESPAWN_FINISH: player_initial,
    }
    explode.transitions = {
        EVT_EXPLOSION_FINISH: respawn,
    }

    target.subscribe(EVT_START_EXPLOSION, state_machine.state_transition_event)
    target.subscribe(EVT_RESPAWN_FINISH, state_machine.state_transition_event)
    target.subscribe(EVT_EXPLOSION_FINISH, state_machine.state_transition_event)

    return state_machine