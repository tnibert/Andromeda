from events import EVT_START_EXPLOSION
from sprite import Sprite
from sprites.bullet import Bullet
from constants import SCREENW, SCREENH, PLAYERHEALTH, UP, LEFT, RIGHT, PLAYERSPEED
from sprites.statusmodifiers import StatusModifier, TimeableStatmod
from behaviors.explosion import ExplodeBehavior
from loadstaticres import bulletimg
from sprites.boss import Boss
from endgamesignal import EndLevel
from timer import Timer
import pygame


OFF_SCREEN = -2000
PLAYER_RESPAWN_DELAY = 3


class Player(Sprite):
    def __init__(self, img, eventqueue):
        explosion_behavior = ExplodeBehavior(self)

        Sprite.__init__(self, SCREENW / 2 - img.get_width() / 2, SCREENH - img.get_height() - 5, img, {explosion_behavior})

        self.subscribe(EVT_START_EXPLOSION, explosion_behavior.start_exploding)

        self.speed = PLAYERSPEED
        self.health = PLAYERHEALTH
        self.spawnX = self.x
        self.spawnY = self.y
        # bamf mode - shoot three bullets at a time
        self.bamfmode = False

        # for more precise keyboard input
        self.goright = False
        self.goleft = False
        self.goup = False
        self.godown = False

        # for processing input events
        self.eventqueue = eventqueue
        self.statmods = []

        self.dying = False
        self.orig_image = self.image

        # timer for respawn delay after explosion
        #self.respawn_timer = Timer()
        #self.respawn_timer.subscribe("timeout", self.respawn)

    def update(self):
        super().update()
        #if self.respawn_timer.is_timing():
        #    self.respawn_timer.tick()

        # handle user input
        while not self.eventqueue.empty():
            event = self.eventqueue.get_nowait()

            if not hasattr(event, 'key'):
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.x >= 0:
                    self.goleft = True
                elif event.key == pygame.K_RIGHT and self.x + self.width <= SCREENW:
                    self.goright = True
                elif event.key == pygame.K_UP and self.y >= 0:
                    self.goup = True
                elif event.key == pygame.K_DOWN and self.y + self.height <= SCREENH:
                    self.godown = True
                elif event.key == pygame.K_SPACE:
                    self.fire(bulletimg)
                    if self.bamfmode:
                        self.fire(bulletimg, LEFT)
                        self.fire(bulletimg, RIGHT)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.goleft = False
                elif event.key == pygame.K_RIGHT:
                    self.goright = False
                elif event.key == pygame.K_UP:
                    self.goup = False
                elif event.key == pygame.K_DOWN:
                    self.godown = False

        # for smoothness and border checks
        # todo: normalize diagonals
        distance = self.speed * self.frame_tick
        if self.goright is True and self.x + self.width <= SCREENW:
            self.x += distance
        elif self.goleft is True and self.x >= 0:
            self.x -= distance
        if self.goup is True and self.y >= 0:
            self.y -= distance
        elif self.godown is True and self.y + self.height <= SCREENH:
            self.y += distance

        # handle status modifiers
        # [:] to iterate over copy of list (can remove from tick() Event handling)
        for mod in self.statmods[:]:
            mod.timer.tick()

    def fire(self, img, turret=UP):
        if turret == LEFT:
            bullet = Bullet(self.x + 15, self.y + 40, img, UP, self)
        elif turret == RIGHT:
            bullet = Bullet(self.x + self.image.get_width() - 15, self.y + 40, img, UP, self)
        else:
            bullet = Bullet(self.x + (self.image.get_width() / 2), self.y - 10, img, UP, self)

        self.notify("fire", bullet=bullet)

    def stop_motion(self):
        """
        Stop all momentum of  player.
        This should be called when ship changes scenes to prevent
        frame_tick value from launching ship off screen (since it
        is a time diff between ticks).
        """
        self.frame_tick = 0
        self.goright = False
        self.goleft = False
        self.goup = False
        self.godown = False

    def die(self):
        if not self.dying:
            self.dying = True
            self.health -= 1
            self.notify(EVT_START_EXPLOSION)
            self.notify("alterhealth", value=-1)

    def oneup(self):
        self.health += 1
        self.notify("alterhealth", value=1)

    def respawn(self, event=None):
        if self.health <= 0:
            self.speed = 0
            raise EndLevel({"state": "failure"})
        else:
            self.dying = False
            self.x = self.spawnX
            self.y = self.spawnY
            self.speed = PLAYERSPEED
            self.image = self.orig_image
            self.bamfmode = False
            self.notify("player_respawn")

    #def explosion_finish(self, event):
    #    self.respawn_timer.startwatch(PLAYER_RESPAWN_DELAY)

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if isinstance(event.source, StatusModifier):
                event.source.payload(self)
                if isinstance(event.source, TimeableStatmod):
                    event.source.subscribe("timeout", self.receive_signals)
                    self.statmods.append(event.source)
            elif "Enemy" in str(event.source):
                self.die()
            elif isinstance(event.source, Boss):
                self.die()
            elif isinstance(event.source, Bullet):
                if event.source.origin is not self:
                    self.die()

    def receive_signals(self, event):
        if event.name == "timeout" and isinstance(event.source, TimeableStatmod):
            event.source.reverse(self)
            self.statmods.remove(event.source)
