import pygame as pg
from config import *

def scale(image_list, ratio):
    scaled_images = []
    for img in image_list:
        size_x, size_y = img.get_size()
        new = pg.transform.scale(img, (size_x * ratio, size_y * ratio))
        scaled_images.append(new)
    return scaled_images

def load_weapon():
    weapon_images = [
        pg.image.load(f"src/assets/visual/sprites/weapon_debug/{i}.png").convert_alpha() for i in range(4)
    ]

    punch_images = [
        pg.image.load(Config.SPRITES_DIR + f"weapons/pun/pun{i}.png").convert_alpha() for i in range(4)
    ] 
    
    pistol_images = [
        pg.image.load(Config.SPRITES_DIR + f"weapons/pis/pis{i}.png").convert_alpha() for i in range(5)
    ]
    
    shotgun_images = [
        pg.image.load(Config.SPRITES_DIR + f"weapons/sht/sht{i}.png").convert_alpha() for i in range(8)
    ] 

    rifle_images = [
        pg.image.load(Config.SPRITES_DIR + f"weapons/rifle/rifle{i}.png").convert_alpha() for i in range(4)
    ]

    superweapons_images = {
        0 : scale([pg.image.load(Config.SPRITES_DIR + f"weapons/superweapon/0.png").convert_alpha(), pg.image.load(Config.SPRITES_DIR + f"weapons/superweapon/state1_firing.png").convert_alpha() ], 2),
        1 : scale([pg.image.load(Config.SPRITES_DIR + f"weapons/superweapon/1.png").convert_alpha(), pg.image.load(Config.SPRITES_DIR + f"weapons/superweapon/state2_firing.png").convert_alpha()], 2)
    }
    
    ids = {
        "debug" : weapon_images,
        "punch" : scale(punch_images, 3),
        "pistol" : scale(pistol_images, 4),
        "shotgun" : scale(shotgun_images, 3),
        "rifle" : scale(rifle_images, 4),
        "superweapon" : superweapons_images
    }

    return ids
