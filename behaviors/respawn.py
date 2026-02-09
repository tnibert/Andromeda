from constants import SAUCER_DEATH_SCORE_INC
from events import EVT_RESPAWN_FINISH


class RespawnBehavior:
    def __init__(self, target, orig_image, xproc, yproc, respawn_proc=None):
        """

        :param target:
        :param orig_image
        :param xproc: procedure to determine x position
        :param yproc: procedure to determine y position
        :param respawn_proc: additional modifications on respawn
        """
        self.target = target
        self.xproc = xproc
        self.yproc = yproc
        self.orig_image = orig_image
        if respawn_proc is not None:
            self.respawn_proc = respawn_proc
        else:
            self.respawn_proc = lambda: None

    def act(self):
        self.target.notify("score_up", value=SAUCER_DEATH_SCORE_INC)
        self.target.image = self.orig_image
        self.target.x = self.xproc()
        self.target.y = self.yproc()
        self.respawn_proc()
        self.target.notify(EVT_RESPAWN_FINISH)
