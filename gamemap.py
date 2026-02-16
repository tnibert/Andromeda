from events import EVT_TIMEOUT, EVT_MAP_PROGRESS
from gameobject import GameObject
from constants import SCREENH, SCREENW, SCROLLSPEED, MAXSCROLLSPEED, MAP_LAYER
from sprites.player import Player

VSCROLL_OFFSET = 2000

class GameMap(GameObject):
    def __init__(self, image):
        GameObject.__init__(self, 0, 0, image, layer=MAP_LAYER)
        self.changeover = 0
        self.bgoffset = 0
        self.ychng = 0
        self.scrollspeed = SCROLLSPEED
        self.statmodtimer = None

        self.total_progress = 0

    def update(self):
        super().update()

        if self.statmodtimer is not None:
            self.statmodtimer.tick()

        # change offset for vertical scroll
        progress_change = self.scrollspeed * self.frame_tick
        self.total_progress += progress_change
        if self.bgoffset > VSCROLL_OFFSET:
            self.bgoffset = 0
            self.changeover = 0
            self.ychng = 0
        else:
            self.bgoffset += progress_change

        if 2000 >= self.bgoffset > 2000 - SCREENH:
            self.ychng += progress_change
            self.changeover = 1

        self.notify(EVT_MAP_PROGRESS, progress_change=progress_change, total_progress=self.total_progress)

    def render(self, screen):
        # for seamless vertical scrolling
        if self.changeover == 0:
            screen.blit(self.image, (0, 0), (0, 2000 - SCREENH - self.bgoffset, SCREENW, 2000 - self.bgoffset))
        elif self.changeover == 1:
            screen.blit(self.image, (0, 0), (0, self.image.get_height() - self.ychng, SCREENW, 2000))
            screen.blit(self.image, (0, self.ychng), (0, 0, SCREENW, SCREENH - self.ychng))

    def increase_speed(self, event):
        if isinstance(event.kwargs.get("who"), Player):
            self.scrollspeed = MAXSCROLLSPEED
            self.statmodtimer = event.source.timer
            event.source.subscribe(EVT_TIMEOUT, self.reset_speed)

    def reset_speed(self, event):
        self.scrollspeed = SCROLLSPEED
        self.statmodtimer = None
