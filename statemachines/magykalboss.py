from behaviors.boss.bosscombatbehavior import BossCombatBehavior
from behaviors.boss.bossdeathbehavior import BossDeathBehavior
from behaviors.boss.endlevelbehavior import EndLevelBehavior
from behaviors.trajectory import TrajectoryMovementBehavior
from statemachine import StateMachine, State
from typeset import TypeSet


def magykal_boss_graph(target) -> StateMachine:
    boss_state_entering = State(target, TypeSet({
        TrajectoryMovementBehavior(180, target.speed, target)
    }))
    boss_state_fighting = State(target, TypeSet({BossCombatBehavior(target)}))
    boss_state_dying = State(target, TypeSet({BossDeathBehavior(target)}))
    boss_state_dead = State(target, TypeSet({EndLevelBehavior}))

    boss_state_entering.transitions = {
        lambda t: t.y >= 5: boss_state_fighting
    }
    boss_state_fighting.transitions = {
        lambda t: t.health <= 0: boss_state_dying
    }
    boss_state_dying.transitions = {
        lambda t: t.trigger_index == len(t.boom)-1 and not t.boom[t.trigger_index].exploding: boss_state_dead
    }

    state_machine = StateMachine(boss_state_entering)
    return state_machine