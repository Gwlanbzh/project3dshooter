import pygame as pg
from pygame import Vector2 as v2
from math import hypot, atan, acos, cos, sin, tau, pi
from render.ray import Ray
from render import *
from config import Config
from random import choice

pi_2 = pi / 2

class Weapon():
    def __init__(self):
        self.dmg = 10
        self.delay = 500 # en ms
        self.range = 100 # 100 -> largeur d'un carré

        self.last_shot_time = - self.delay # moment at which the last shot was fired
                                           # - self.delay to avoid animation at init of the game
        self.play_sound_time = - self.delay
        
        self.time_between_sprites = 200 # ms
        self.sprite = load_weapon() # from render.weapons
        self.image_index = 0

        self.ammo_sound = [pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/debug_ammo.mp3")]
        self.no_ammo_sound = [pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/debug_no_ammo.mp3")]

    
    def shoot(self, entity, mob_list):
        """
        check if a mob is touch on click and act in consequence.
        """
        t = pg.time.get_ticks()
        if t - self.last_shot_time > self.delay: # 100 ms between shots 
            if entity.ammo > 0:
                self.last_shot_time = t
                entity.ammo = max(0, entity.ammo - 1)
                self.hit_scan(entity.game.world.map.grid, entity.r, entity.orientation, mob_list)
                self.play_sound()
            else:
                self.play_sound(no_ammo=True)
            print(entity.ammo)
            print("shoot")
    
    def hit_scan(self, map, pos, orientation, mob_list):

        sorted_mob_list = [(self.dist(pos, mob), mob) for mob in mob_list if mob.health > 0]
        sorted_mob_list = sorted(sorted_mob_list, key=lambda x : x[0])

        for dist, mob in sorted_mob_list:
            # test mur
            direction = v2(cos(orientation), sin(orientation))
            rayon = Ray(pos, direction, map)

            if dist > self.range or rayon.distance < dist:
                return # la liste étant triée, il ne sert plus à rien de tester le reste des mobs
            else:
                teta_max = atan(mob.size/dist) # la marge d'erreur pour l'angle de tir du joueur.
                
                x, y = mob.r - pos
                if y == 0 and x < 0:
                    angle_p_m = pi
                else:
                    angle_p_m = 2 * atan(y/(x + dist)) % tau

                teta = orientation - angle_p_m
                # cas limite -> l'angle est très proche de 2pi, il faut tester pour un angle qui tend vers 2pi et pour un angle qui tend vers 0
                if y == 0:
                    if abs(teta) < teta_max:
                        mob.hurt(self.dmg)
                        return
                    
                    teta = tau - teta
                    if abs(teta) < teta_max:
                        mob.hurt(self.dmg)
                        return

                if abs(teta) < teta_max:
                    mob.hurt(self.dmg)
                    return # on interromp la boucle, sinon les balles peuvent traverser les mobs.

    def dist(self, pos, mob):
        """
        test if a mob can be shot by a player
        """
        x, y = pos - mob.r
        dist = hypot(x, y)

        return dist

    def draw(self, window):
        width, height = self.sprite[self.image_index].get_size()
        top_left = (
            (Config.RES_X / 2) - (width / 2),
            Config.RES_Y - height
        )
        self.update_image()
        window.blit(self.sprite[self.image_index], top_left)

    def draw2d(self, window, r, teta):
        traylength = self.range
        pg.draw.line(
            window,'yellow', (r),
            (r[0]+ traylength * cos(teta), r[1] + traylength * sin(teta)),
            2
        )

    def update_image(self):
        i = int((pg.time.get_ticks() - self.last_shot_time) / self.time_between_sprites)
        self.image_index = i if i < len(self.sprite) else 0

    def play_sound(self, no_ammo=False):
        if Config.NO_SOUND:
            return

        t = pg.time.get_ticks()
        if no_ammo:
            if t - self.play_sound_time > self.delay:
                self.play_sound_time = t
                choice(self.no_ammo_sound).play()
        else:
            choice(self.ammo_sound).play()
