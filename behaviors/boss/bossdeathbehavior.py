import random

from behaviors.explosion import ExplodeBehavior
from constants import BOSS_DEATH_SCORE_INC, NUM_BOSS_EXPLOSIONS
from events import EVT_EXPLOSION_FINISH, EVT_DEATH
from loadstaticres import blank, explosion
from core.sprite import Sprite


class BossDeathBehavior:
    def __init__(self, target):
        """
        :param target:
        """
        self.target = target
        self.boom = []

        # oh the audacity
        self.trigger_index = 0
        def inc_trigger_index(event):
            self.trigger_index += 1

        for i in range(NUM_BOSS_EXPLOSIONS):
            self.boom.append(
                ExplodeBehavior(
                    Sprite(
                        random.randrange(self.target.image.get_width() - explosion[0].get_width()),
                        random.randrange(self.target.image.get_height() - explosion[0].get_height()),
                        blank
                    )
                )
            )
            self.boom[i].target.subscribe(EVT_EXPLOSION_FINISH, inc_trigger_index)


    def act(self):
        try:
            self.boom[self.trigger_index].act()
        except IndexError:  # if the index is out of range, explosions are collectively finished
            self.target.notify(EVT_DEATH, value=BOSS_DEATH_SCORE_INC)

        # render explosions onto boss
        # todo: make sections of boss transparent after explosions
        self.target.image = self.target.orig_image.copy()
        for e in self.boom:
            e.target.render(self.target.image)
