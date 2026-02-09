class BossCombatBehavior:
    def __init__(self, target):
        """
        :param target:
        """
        self.target = target
        self.fighting = False

    def act(self):
        if not self.fighting:
            self.target.combat_state_timer.startwatch(self.target.combat_state_change_time)
            self.fighting = True
        if self.fighting:
            self.target.combat_state_timer.tick()
            self.target.combat_move()
