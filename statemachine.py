from observe import Event
from typeset import TypeSet


class State:
    """
    Node in state graph to implement a state machine
    """
    def __init__(self, target, behaviors: TypeSet, transitions: dict=None, name: str=""):
        self.target = target
        self.name = name

        # edges of state graph
        if transitions is None:
            self.transitions = dict()
        else:
            self.transitions = transitions

        self.behaviors = behaviors
        self.behavior_attach_queue = []
        self.behavior_discard_queue = []

    def transition(self) -> State:
        for trigger, next_state in self.transitions.items():
            if callable(trigger) and trigger(self.target):
                print("next state via trigger {}".format(next_state.name))
                return next_state
        return self

    def behave(self):
        for behavior in self.behaviors:
            behavior.act()

        # process updates to the behavior set
        for behavior_type in self.behavior_discard_queue:
            self.discard_behavior(behavior_type)
        self.behavior_discard_queue = []
        for behavior in self.behavior_attach_queue:
            self.attach_behavior(behavior)
        self.behavior_attach_queue = []

    def queue_discard_behavior(self, behavior_type):
        self.behavior_discard_queue.append(behavior_type)

    def queue_attach_behavior(self, behavior):
        self.behavior_attach_queue.append(behavior)

    def discard_behavior(self, behavior_type):
        """

        :param behavior_type: the type of behavior to remove
        :return:
        """
        self.behaviors.discard(behavior_type)

    def attach_behavior(self, behavior):
        self.behaviors.add(behavior)


class StateMachine:
    def __init__(self, initial: State):
        self.current_state = initial
        self.last_state = ""

    def state_transition_event(self, event: Event):
        """
        :param event:
        :return:
        """
        next_state = self.current_state.transitions.get(event.name)
        if next_state is not None:
            print("set next state {}".format(next_state.name))
            self.current_state = next_state

    def iteration(self):
        self.current_state = self.current_state.transition()
        if self.current_state.name != self.last_state:
            print("state transition {} -> {}".format(self.last_state, self.current_state.name))
            self.last_state = self.current_state.name
        self.current_state.behave()