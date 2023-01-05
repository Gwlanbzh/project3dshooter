from weapons import Weapon
import pygame as pg
from config import *
from render import load_rifle

class Rifle(Weapon):
    def __init__(self):
        super().__init__()
        
        self.range = WALL_WIDTH * 15
        self.dmg = 50
        self.delay = 500  # ms
        self.time_between_sprites = 90

        self.model = "rifle"

        self.sprite = load_rifle()
