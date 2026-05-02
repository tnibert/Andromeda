from events import EVT_TIMEOUT, EVT_MAP_PROGRESS, EVT_FIRE
from core.gamestrategy import Strategy
from gamemap import GameMap
from sprites.statusmodifiers import OneUp, Bomb, SpeedUp, MoreGuns
from core.utilfuncs import switch
from core.timer import Timer
from core.textelement import TextElement
from core.endgamesignal import EndLevel
from loadstaticres import oneupimg, moregunsimg, speedupimg, bombimg
from constants import SCREENW, SCREENH, TEXTCOLOR, LVL_START_FONT, LVL_START_TIME
import random


class Level(Strategy):
    """
    Strategy for managing progression of typical game level
    """
    def __init__(self, scene, mixer, config, universal):
        """
        Declare and assign variables
        :param scene: Scene object to manipulate
        :param mixer: pygame.mixer object
        :param config: dictionary of level specific resources
        :param universal: dictionary of objects that stay in use between levels
        """

        super().__init__(scene)
        self.mixer = mixer
        self.config = config

        # set up player
        self.ship = universal["ship"]

        # set up map
        self.game_map = GameMap(self.config["background"].convert())

        # add health and score labels
        self.health_label = universal["health_label"]
        self.score_label = universal["score_label"]
        self.level_start_label = TextElement(SCREENW/4, SCREENH/4, LVL_START_FONT, TEXTCOLOR, self.config["start_text"])

        self.start_text_timer = Timer()

        self.enemy_entry_config = self.config["enemy_config"](self.ship)

    def setup(self):
        """
        Attach objects to scene and set up subscriptions
        """
        # clear relevant subscriptions on shared objects from previous levels
        self.ship.remove_event(EVT_FIRE)
        self.ship.remove_event("player_respawn")

        # ensure ship is positioned correctly
        self.ship.respawn()

        # load up music
        self.mixer.music.load(self.config["bg_music_fname"])

        self.ship.subscribe(EVT_FIRE, lambda ev: self.scene.attach(ev.kwargs.get("bullet"))) # enable firing of bullets
        self.ship.subscribe("player_respawn", self.game_map.reset_speed) # so that map speed up resets on player death
        self.start_text_timer.subscribe(EVT_TIMEOUT, self.remove_start_text)
        self.game_map.subscribe(EVT_MAP_PROGRESS, self.map_progress_event)        

        self.scene.attach(self.ship)
        self.scene.attach(self.game_map)
        self.scene.attach(self.health_label)
        self.scene.attach(self.score_label)
        self.scene.attach(self.level_start_label)

        self.start_text_timer.startwatch(LVL_START_TIME)

    def run_game(self):
        try:
            if not self.mixer.music.get_busy():
                # start music on endless loop
                self.mixer.music.play(-1)

            if self.start_text_timer.is_timing():
                self.start_text_timer.tick()

            # determine if we should have a status modifier
            # so apparently there's no switch/case in python >_>
            # choose a random number, determine which powerup based on number
            for case in switch(random.randrange(0, 10000)):
                statmod = None
                if case(1):
                    statmod = OneUp(oneupimg)
                elif case(90):
                    statmod = Bomb(bombimg)
                elif case(1337):
                    statmod = SpeedUp(speedupimg)
                    statmod.subscribe("collision", self.game_map.increase_speed)
                elif case(511):
                    statmod = MoreGuns(moregunsimg)
                if statmod is not None:
                    self.scene.attach(statmod)

            super().run_game()

        # intercept the EndLevel signal, stop music, and attach score
        except EndLevel as e:
            self.mixer.music.stop()
            self.ship.stop_motion()
            info = e.args[0]
            info['score'] = self.score_label.get_value()
            raise EndLevel(info)

    def map_progress_event(self, event):
        cur_progress = event.kwargs.get("total_progress")

        while len(self.enemy_entry_config) > 0 and cur_progress > self.enemy_entry_config[0][0]:
            print("in enemy add: {}".format(cur_progress))
            scene_node = self.enemy_entry_config.pop(0)[1]

            if hasattr(scene_node, "pre_scene_attach"):
                scene_node.pre_scene_attach(self.scene, self.score_label, self.game_map)
            else:
                print("scene_node lacks attribute pre_scene_attach: {}", type(scene_node))

            self.scene.attach(scene_node)

    def remove_start_text(self, event):
        self.scene.remove(self.level_start_label)
