from observe import Observable
from constants import GAMEOBJ_LAYER
from statemachine import State
from typeset import TypeSet


class GameObject(Observable):
    """
    A renderable object in the game
    """
    def __init__(self, x, y, img, state_graph=None, properties: set=None, layer=GAMEOBJ_LAYER):
        """

        :param x:
        :param y:
        :param img:
        :param state_graph:
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

        if state_graph is None:
            self.state_graph = State(self, TypeSet())
        else:
            self.state_graph = state_graph
        self.last_state = self.state_graph.name

        if properties is None:
            self.properties = TypeSet()
        else:
            self.properties = TypeSet(properties)

    def update(self):
        self.state_graph = self.state_graph.transition()
        if self.state_graph.name != self.last_state:
            print("state transition {} -> {}".format(self.last_state, self.state_graph.name))
            self.last_state = self.state_graph.name
        self.state_graph.behave()

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
