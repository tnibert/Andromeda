from endgamesignal import EndLevel


class EndLevelBehavior:
    def act(self):
        raise EndLevel({"state": "victory"})
