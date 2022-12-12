from math import pi
import pygame as pg

WALL_WIDTH = 100

class Config():
    """
    Contains constants for the game.
    TODO: init config from config file
    """
    WINDOW_SIZE = 1280 , 800 # value link to the size of the map before render is finished
    RES_X, RES_Y = WINDOW_SIZE
    FRAME_RATE = 120

    PLAYER_V = 0.5 # arbitraty value for good feeling
    PLAYER_ROT_SPEED = 0.004  # arbitrary value for good feeling. temporarily, waiting for mouse handling
    
    PLAYER_VERT_ROT_SPEED = 1
    PLAYER_MAX_VERT_ROT = 100
    
    # rendering-related constants
    WALL_HEIGHT = 200  # height of the wall that is above the player's point of view (e.g. for a height > VIEW_HEIGHT)
    FOV_X = 2*pi/3
    FOV_Y = 2*pi/3
    
    VIEW_HEIGHT = 75
    
    DISTANCE_FADING = 1.001
    
    TEXTURES_FOLDER = "assets/textures/"
