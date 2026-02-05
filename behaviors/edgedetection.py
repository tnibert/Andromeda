from constants import SCREENW


class EdgeDetectionBehavior:
    def __init__(self, edge_detect_handler, target):
        self.edge_detect_handler = edge_detect_handler
        self.target = target

    def act(self):
        # side detection
        if self.target.x > SCREENW - self.target.width or self.target.x < 0:
            self.edge_detect_handler()
