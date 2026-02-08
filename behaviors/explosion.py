from constants import EXPLOSION_FRAME_UPDATE_WAIT
from events import EVT_TIMEOUT, EVT_EXPLOSION_FINISH
from loadstaticres import explosion
from observe import Observable
from timer import Timer

class ExplodeBehavior(Observable):
    """
    todo: boss explosions
    """
    def __init__(self, target):
        Observable.__init__(self)
        self.target = target
        self.reset()

    def reset(self):
        self.exploding = False
        self.explosion_index = 0

        self.explosion_timer = Timer()
        self.explosion_timer.subscribe(EVT_TIMEOUT, self.update_explosion)

    def act(self):
        if not self.exploding:
            self.start_exploding()
        if self.exploding:
            self.explosion_timer.tick()

    def start_exploding(self, event=None):
        """
        Start the explosion sequence
        queues up update_explosion calls on explosion_timer timeout event
        NB: If this is called again while the explosion is occurring, the sequence will reset
        """
        self.exploding = True
        self.target.image = explosion[self.explosion_index]
        self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)

    def update_explosion(self, event):
        """
        Event handler to update the explosion, called from the explosion timer
        :param event: the timer notify event
        :return: True if explosion is complete, False if not
        """
        if self.explosion_index < len(explosion)-1:
            self.explosion_index += 1
            self.target.image = explosion[self.explosion_index]
            self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)
        else:
            self.reset()
            self.target.notify(EVT_EXPLOSION_FINISH)
