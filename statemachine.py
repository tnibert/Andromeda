from typeset import TypeSet


class State:
    """
    Node in state graph to implement a state machine
    """
    def __init__(self, target, behaviors: TypeSet, transitions: dict):
        self.target = target

        # edges of state graph
        self.transitions = transitions

        self.behaviors = behaviors
        self.behavior_attach_queue = []
        self.behavior_discard_queue = []

    def transition(self) -> State:
        for trigger, next_state in self.transitions.items():
            if trigger(self.target):
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
