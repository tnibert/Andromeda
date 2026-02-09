from constants import SAUCER_DEATH_SCORE_INC
from events import EVT_RESPAWN_FINISH


class EnemyRespawnBehavior:
    def __init__(self, target, xproc, yproc):
        """

        :param target:
        :param xproc: procedure to determine x position
        :param yproc: procedure to determine y position
        """
        self.target = target
        self.xproc = xproc
        self.yproc = yproc

    def act(self):
        self.target.notify("score_up", value=SAUCER_DEATH_SCORE_INC)
        self.target.image = self.target.orig_image
        self.target.x = self.xproc()
        self.target.y = self.yproc()
        self.target.notify(EVT_RESPAWN_FINISH)
