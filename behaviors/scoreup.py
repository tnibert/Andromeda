from constants import SAUCER_DEATH_SCORE_INC
from events import EVT_SCORE_UP

class ScoreUpBehavior:
    def __init__(self, target):
        """
        :param target:
        """
        self.target = target
        self.done = False

    def act(self):
        if not self.done:
            self.target.notify(EVT_SCORE_UP, value=SAUCER_DEATH_SCORE_INC)
            self.done = True
