from observe import Observable
from constants import GAMEOBJ_LAYER
from typeset import TypeSet


class GameObject(Observable):
    """
    A renderable object in the game
    """
    def __init__(self, x, y, img, behaviors: set=None, properties: set=None, layer=GAMEOBJ_LAYER):
        """

        :param x:
        :param y:
        :param img:
        :param behaviors: set of behaviors for game object
        :param properties: set of properties for game object
        :param layer:
        """
        Observable.__init__(self)

        self.x = x
        self.y = y
        self.image = img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.layer = layer

        # allows for movement speed independent of frame rate
        self.frame_tick = 0

        if behaviors is None:
            self.behaviors = TypeSet()
        else:
            self.behaviors = TypeSet(behaviors)
        self.behavior_attach_queue = []
        self.behavior_discard_queue = []

        if properties is None:
            self.properties = TypeSet()
        else:
            self.properties = TypeSet(properties)

    def update(self):
        for behavior in self.behaviors:
            behavior.act()

        # process updates to the behavior set
        for behavior_type in self.behavior_discard_queue:
            self.discard_behavior(behavior_type)
        self.behavior_discard_queue = []
        for behavior in self.behavior_attach_queue:
            self.attach_behavior(behavior)
        self.behavior_attach_queue = []

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def on_tick(self, event):
        """
        Event handler for clock ticks
        :param event:
        :return:
        """
        diff = event.kwargs.get("diff")
        if diff is not None:
            self.frame_tick = diff
        else:
            self.frame_tick = 0

    def on_collide(self, event):
        """
        Event handler for collisions
        :param event:
        :return:
        """
        pass

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
