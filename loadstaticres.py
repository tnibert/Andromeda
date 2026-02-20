from utilfuncs import toframes
from constants import TURRET_DIMENSION
import pygame


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