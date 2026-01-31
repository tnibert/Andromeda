from constants import EXPLOSION_FRAME_UPDATE_WAIT
from loadstaticres import explosion
from observe import Observable
from timer import Timer

class ExplodeBehavior(Observable):
    """
    todo: boss explosions
    """
    def __init__(self, target):
        Observable.__init__(self)
        self.exploding = False
        self.explosion_index = 0

        self.explosion_timer = Timer()
        self.explosion_timer.subscribe("timeout", self.update_explosion)

        self.target = target
        self.subscribe("explosion_finish", self.target.respawn)

    def act(self):
        if self.exploding:
            self.explosion_timer.tick()

    def start_exploding(self, event):
        """
        Start the explosion sequence
        queues up update_explosion calls on explosion_timer timeout event
        NB: If this is called again while the explosion is occurring, the sequence will reset
        """
        print("start_exploding")
        self.exploding = True
        self.target.image = explosion[self.explosion_index]
        self.target.speed = 0
        self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)

    def update_explosion(self, event):
        """
        Event handler to update the explosion, called from the explosion timer
        :param event: the timer notify event
        :return: True if explosion is complete, False if not
        """
        print("update_explosion")
        if self.explosion_index < len(explosion)-1:
            self.explosion_index += 1
            self.target.image = explosion[self.explosion_index]
            self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)
        else:
            self.explosion_index = 0
            self.exploding = False
            self.notify("explosion_finish")
