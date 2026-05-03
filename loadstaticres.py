from core.utilfuncs import toframes
from constants import TURRET_DIMENSION
import pygame

"""
This file loads the static resources so that other modules can import them.
"""

introscreen = pygame.image.load("assets/intro1.png")

explosion = toframes(pygame.image.load("assets/explode1.png"), 5, 120)

shipimg = pygame.image.load("assets/spaceship1.png")
bulletimg = pygame.image.load("assets/bullet1.png")

# status modifier images
oneupimg = pygame.image.load("assets/plus102.png")
bombimg = pygame.image.load("assets/bomb.png")
speedupimg = pygame.image.load("assets/speed.png")
moregunsimg = pygame.image.load("assets/guns.png")

blank = pygame.Surface((1, 1))

turretimg = pygame.transform.scale(pygame.image.load("assets/td_basic_towers/PNG/Tower.png"), (TURRET_DIMENSION, TURRET_DIMENSION))
gunimg = pygame.transform.scale(pygame.image.load("assets/td_basic_towers/PNG/Cannon.png"), (TURRET_DIMENSION/1.5, TURRET_DIMENSION/1.5))

# enemies
surf_alien = pygame.transform.scale(pygame.image.load("assets/w/surf_alien.png"), (TURRET_DIMENSION, TURRET_DIMENSION))
earth_alien_boss_img = pygame.transform.scale(pygame.image.load("assets/w/earth_alien.png"), (TURRET_DIMENSION*5, TURRET_DIMENSION*5))
lantern_saucer_img = pygame.image.load("assets/magykal_level/saucer.png")
magykal_boss_img = pygame.image.load("assets/magykal_level/boss.png")
simple_saucer_img = pygame.image.load("assets/simple_level/saucer.png")
invader_boss_image = pygame.image.load("assets/simple_level/invader.png")

# maps
magykal_map = pygame.image.load("assets/magykal_level/map.png")
simple_map = pygame.image.load("assets/simple_level/map.png")
