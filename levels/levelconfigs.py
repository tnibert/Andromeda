import random

from constants import SCROLLSPEED, TURRET_DIMENSION, SCREENW
from loadstaticres import turretimg, gunimg
from sprites import boss
import pygame

from sprites.enemy import Enemy
from sprites.turret import Turret
from statemachines.cutcrossenemy import cut_cross_enemy_state_graph
from statemachines.defaultenemy import default_enemy_state_graph


def l1_enemy_config(ship):
    saucer_img = pygame.image.load("assets/magykal_level/saucer.png")
    boss_image = pygame.image.load("assets/magykal_level/boss.png")

    # todo: enemy factory?
    entry_config = [
        (SCROLLSPEED * 1, Enemy(saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 5, Enemy(saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 10, Enemy(saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 15,
         Turret(40, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 15,
         Turret(SCREENW - TURRET_DIMENSION - 40, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 25, boss.MagykalBossBehave(SCREENW / 2 - boss_image.get_width() / 2, -1200, boss_image, ship))
    ]
    entry_config.sort(key=lambda tup: tup[0])  # ensure ordered from earliest to latest
    return entry_config

def l2_enemy_config(ship):
    saucer_img = pygame.image.load("assets/simple_level/saucer.png")
    saucer_img2 = pygame.image.load("assets/magykal_level/saucer.png")
    boss_image = pygame.image.load("assets/simple_level/invader.png")

    entry_config = [
        (SCROLLSPEED * 10, Enemy(saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(saucer_img2, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 15,
         Turret(SCREENW/2 - TURRET_DIMENSION/2, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 25, boss.InvaderBossBehave(SCREENW / 2 - boss_image.get_width() / 2, -1200, boss_image, ship))
    ]
    entry_config.sort(key=lambda tup: tup[0])  # ensure ordered from earliest to latest
    return entry_config

# configurations for each level, in order
level_configs = [
    {
        "background": pygame.image.load("assets/magykal_level/map.png"),
        "bg_music_fname": "assets/JaricoIsland.ogg",
        "start_text": "LEVEL 1",
        "enemy_config": l1_enemy_config
    },
    {
        "background": pygame.image.load("assets/simple_level/map.png"),
        "bg_music_fname": "assets/JaricoLandscape.ogg",
        "start_text": "LEVEL 2",
        "enemy_config": l2_enemy_config
    }
]
