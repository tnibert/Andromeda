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

        self.next_state = self

    def state_transition_event(self, event: Event):
        """
        todo: this will currently be actioned even if the state is not the current state
        :param event:
        :return:
        """
        next_state = self.transitions.get(event.name)
        if next_state is not None:
            print("set next state {}".format(next_state.name))
            self.next_state = next_state

    def transition(self) -> State:
        for trigger, next_state in self.transitions.items():
            if callable(trigger) and trigger(self.target):
                print("next state via trigger {}".format(next_state.name))
                self.next_state = next_state

        # reset next state
        temp = self.next_state
        self.next_state = self
        return temp

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
