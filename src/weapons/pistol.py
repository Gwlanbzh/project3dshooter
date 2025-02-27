import pygame as pg
from weapons import Weapon
from config import *


class Pistol(Weapon):
    def __init__(self):
        super().__init__()
        
        self.dmg = 15
        self.delay = 500 # en ms
        self.range = 10 * WALL_WIDTH

        self.last_shot_time = - self.delay # moment at which the last shot was fired
                                           # - self.delay to avoid animation at init of the game
        
        self.time_between_sprites = 75
        self.image_index = 0
        self.model = "pistol"
        self.key = 2
