from constants import BOSS_DEATH_SCORE_INC


class BossDeathBehavior:
    def __init__(self, target):
        """
        :param target:
        """
        self.target = target

    def act(self):
        if not self.target.exploding:
            self.target.start_exploding()
            self.target.notify("death", value=BOSS_DEATH_SCORE_INC)

        for e in self.target.boom:
            e.update()

        # start next explosion if the previous is finished
        if not self.target.boom[self.target.trigger_index].exploding and self.target.trigger_index < len(self.target.boom) - 1:
            self.target.trigger_index += 1
            self.target.boom[self.target.trigger_index].start_exploding()

        # render explosions onto boss
        # todo: make sections of boss transparent after explosions
        self.target.image = self.target.orig_image.copy()
        for e in self.target.boom:
            e.render(self.target.image)

        # check if all explosions are finished
        #if self.trigger_index == len(self.boom) - 1 and not self.boom[self.trigger_index].exploding:
        #    self.game_state = BOSS_STATE_DEAD
        #    self.exploding = False
