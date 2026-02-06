from statemachine import State
from typeset import TypeSet


class TestTarget:
    def __init__(self):
        self.i = 0
        self.j = 0

class TestBehavior1:
    def __init__(self, target):
        self.target = target

    def act(self):
        self.target.i += 1

class TestBehavior2:
    def __init__(self, target):
        self.target = target

    def act(self):
        self.target.j += 1

def test_transition_and_behave():
    target = TestTarget()
    b1 = TestBehavior1(target)
    b2 = TestBehavior2(target)
    state = State(target, TypeSet({b1}), {
        lambda t: t.i == 2: State(target, TypeSet({b2}), {
            lambda t: t.j == 2: State(target, TypeSet({}), dict())
        }),
    })

    state = state.transition()
    state.behave()
    assert target.i == 1
    assert target.j == 0
    state = state.transition()
    state.behave()
    assert target.i == 2
    assert target.j == 0
    state = state.transition()
    state.behave()
    assert target.i == 2
    assert target.j == 1
    state = state.transition()
    state.behave()
    assert target.i == 2
    assert target.j == 2
    state = state.transition()
    state.behave()
    assert target.i == 2
    assert target.j == 2