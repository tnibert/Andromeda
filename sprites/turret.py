from sprite import Sprite
from constants import SCREENH

class Turret(Sprite):
    def __init__(self, initial_x, initial_y, img):
        Sprite.__init__(self,
                        initial_x,
                        initial_y,
                        img)

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.notify("remove") # todo: after removing from the scene, we still have a dangling notification to map_progress_event

    def map_progress_event(self, event):
        self.y += event.kwargs.get("progress_change")
