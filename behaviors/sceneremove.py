class SceneRemoveBehavior:
    def __init__(self, target):
        """
        :param target:
        """
        self.target = target
        self.removed = False

    def act(self):
        if not self.removed:
            print("scene exit")
            self.target.notify("remove")
            self.removed = True
