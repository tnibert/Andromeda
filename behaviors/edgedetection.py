from constants import SCREENW, LEFT, RIGHT


class EdgeDetectionBehavior:
    def __init__(self, edge_detect_handler, target):
        self.edge_detect_handler = edge_detect_handler
        self.target = target

    def act(self):
        # side detection
        if self.target.x > SCREENW - self.target.width:
            self.edge_detect_handler(RIGHT)
        elif self.target.x < 0:
            self.edge_detect_handler(LEFT)
