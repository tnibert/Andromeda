from gameobject import GameObject

# all sprites inherit from this class
class MoveableObject(GameObject):
    def __init__(self, x, y, img, behaviors=None):
        GameObject.__init__(self, x, y, img, behaviors)
