import random

from constants import SCROLLSPEED, TURRET_DIMENSION, SCREENW
from loadstaticres import turretimg, gunimg, invader_boss_image, surf_alien, lantern_saucer_img, magykal_boss_img, \
    simple_saucer_img, earth_alien_boss_img, magykal_map, simple_map
from sprites import boss
from sprites.enemy import Enemy
from sprites.turret import Turret
from statemachines.cutcrossenemy import cut_cross_enemy_state_graph
from statemachines.defaultenemy import default_enemy_state_graph


def l1_enemy_config(ship):
    # todo: enemy factory?
    entry_config = [
        (SCROLLSPEED * 1, Enemy(surf_alien, SCREENW/2, default_enemy_state_graph)),
        (SCROLLSPEED * 5, Enemy(surf_alien, random.randrange(0, SCREENW), default_enemy_state_graph)),

        # three in a row follow each other
        (SCROLLSPEED * 10, Enemy(lantern_saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 11, Enemy(lantern_saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 12, Enemy(lantern_saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),

        (SCROLLSPEED * 15, Enemy(lantern_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(simple_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(lantern_saucer_img, SCREENW - 100, cut_cross_enemy_state_graph)),

        # turrets at same vertical level together
        (SCROLLSPEED * 15,
         Turret(40, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 15,
         Turret(SCREENW - TURRET_DIMENSION - 40, -TURRET_DIMENSION, turretimg, gunimg, ship)),

        # centered turret
        (SCROLLSPEED * 20,
         Turret(SCREENW / 2 - TURRET_DIMENSION / 2, -TURRET_DIMENSION, turretimg, gunimg, ship)),

        (SCROLLSPEED * 21, Enemy(surf_alien, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 21, Enemy(simple_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 21, Enemy(lantern_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),

        (SCROLLSPEED * 23, Enemy(lantern_saucer_img, SCREENW - 200, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 24, Enemy(lantern_saucer_img, SCREENW - 200, cut_cross_enemy_state_graph)),

        (SCROLLSPEED * 25,
         Turret(40, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 25,
         Turret(SCREENW - TURRET_DIMENSION - 40, -TURRET_DIMENSION, turretimg, gunimg, ship)),

        (SCROLLSPEED * 30, Enemy(lantern_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 30, Enemy(lantern_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 30, Enemy(lantern_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),

        # boss
        (SCROLLSPEED * 35,
         boss.MagykalBossBehave(SCREENW / 2 - magykal_boss_img.get_width() / 2, -1200, magykal_boss_img, ship))
    ]
    entry_config.sort(key=lambda tup: tup[0])  # ensure ordered from earliest to latest
    return entry_config

def l2_enemy_config(ship):
    entry_config = [
        (SCROLLSPEED * 10, Enemy(simple_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(simple_saucer_img, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(lantern_saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),

        # centered turret
        (SCROLLSPEED * 15,
         Turret(SCREENW/2 - TURRET_DIMENSION/2, -TURRET_DIMENSION, turretimg, gunimg, ship)),

        (SCROLLSPEED * 25,
         boss.InvaderBossBehave(SCREENW / 2 - invader_boss_image.get_width() / 2, -1200, invader_boss_image, ship))
    ]
    entry_config.sort(key=lambda tup: tup[0])  # ensure ordered from earliest to latest
    return entry_config

def l3_enemy_config(ship):
    entry_config = [
        (SCROLLSPEED * 10, Enemy(surf_alien, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(surf_alien, random.randrange(0, SCREENW), default_enemy_state_graph)),
        (SCROLLSPEED * 15, Enemy(lantern_saucer_img, SCREENW - 80, cut_cross_enemy_state_graph)),
        (SCROLLSPEED * 15,
         Turret(SCREENW / 2 - TURRET_DIMENSION / 2, -TURRET_DIMENSION, turretimg, gunimg, ship)),
        (SCROLLSPEED * 25,
         boss.MagykalBossBehave(SCREENW / 2 - earth_alien_boss_img.get_width() / 2, -1200, earth_alien_boss_img, ship))
    ]
    entry_config.sort(key=lambda tup: tup[0])  # ensure ordered from earliest to latest
    return entry_config

# configurations for each level, in order
level_configs = [
    {
        "background": magykal_map,
        "bg_music_fname": "assets/JaricoIsland.ogg",
        "start_text": "LEVEL 1",
        "enemy_config": l1_enemy_config
    },
    {
        "background": simple_map,
        "bg_music_fname": "assets/JaricoLandscape.ogg",
        "start_text": "LEVEL 2",
        "enemy_config": l2_enemy_config
    },
    {
        "background": magykal_map,
        "bg_music_fname": "assets/JaricoLandscape.ogg",
        "start_text": "LEVEL 3",
        "enemy_config": l3_enemy_config
    }
]
