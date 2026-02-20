from sprite import Sprite
from constants import SCREENH, TURRET_DIMENSION

class Turret(Sprite):
    """
    Join images of base and rotating gun
    """
    def __init__(self, initial_x, initial_y, base_img, gun_img):
        Sprite.__init__(self,
                        initial_x,
                        initial_y,
                        base_img)
        self.base_img = Sprite(0, 0, base_img)
        gun_x, gun_y = center_image_within(base_img, gun_img)
        self.gun_img = Sprite(gun_x, gun_y, gun_img)

        self.rotation = 0 # testing

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.notify("remove") # todo: after removing from the scene, we still have a dangling notification to map_progress_event

        if self.rotation == 360:
            self.rotation = 0
        else:
            self.rotation += 1

    def render(self, screen):
        # overlay the base and the gun
        self.image = self.base_img.image.copy()
        gun_img = self.gun_img.rotated(self.rotation)
        #self.gun_img.render(self.image)
        self.image.blit(gun_img, (self.gun_img.x, self.gun_img.y))
        super().render(screen)

    def map_progress_event(self, event):
        self.y += event.kwargs.get("progress_change")

def center_image_within(environment_img, inside_img):
    """
    return position to center inside_img within environment_img
    """
    return environment_img.get_width()/2 - inside_img.get_width()/2, environment_img.get_height()/3 - inside_img.get_height()/2
    