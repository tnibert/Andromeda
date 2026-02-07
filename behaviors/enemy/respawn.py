import random

from constants import SCREENW, SAUCER_DEATH_SCORE_INC
from events import EVT_RESPAWN_FINISH


class EnemyRespawnBehavior:
    def __init__(self, target):
        """

        :param target:
        """
        self.target = target

    def act(self):
        self.target.notify("score_up", value=SAUCER_DEATH_SCORE_INC)
        self.target.image = self.target.orig_image
        self.target.x = random.randrange(0, SCREENW)
        self.target.y = -3 * self.target.image.get_height()
        self.target.notify(EVT_RESPAWN_FINISH)
