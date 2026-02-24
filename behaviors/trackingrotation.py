from events import EVT_PLAYER_POSITION
import math

class TrackingRotationBehavior:
    def __init__(self, target, player):
        """

        :param target: the object that is rotating
        :param player: the player to position track
        """
        self.target = target
        player.subscribe(EVT_PLAYER_POSITION, self.on_event)

    def act(self):
        pass

    def on_event(self, event):
        self.target.rotation = 90-math.degrees(math.atan2(self.target.y-event.kwargs.get("center").y, self.target.x-event.kwargs.get("center").x))
