import pygame as pg
from config import *
from math import hypot
from random import choice
from os import listdir

class Sound():
    def __init__(self) -> None:
        debug_dry_fire_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/debug_no_ammo.mp3")
        ]
        
        debug_weapon_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/debug_ammo.mp3")
        ]
        
        dry_fire_sound = [ 
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/dryfire_pistol.mp3"),
        ]

        pistol_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/fire_pistol.mp3")
        ]

        rifle_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/uzi_fire.mp3"),
        ]

        punch_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/punch.wav")
        ]

        shotgun_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/shotgun_fire.ogg"),
        ]

        superweapon_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "weapons/superweapon_sound.mp3")
        ]

        pickable_generic = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "pickables/generic.ogg")
        ]

        mine_sound = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + "pickables/mine_exp.mp3")
        ]

        grunt_hurt = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/grunt/pain{i}.ogg") for i in range(4)
        ]

        heavy_hurt = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/heavy/pain{i}.ogg") for i in range(4)
        ]

        boss_hurt = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/boss/pain{i}.ogg") for i in range(4)
        ]

        player_hurt = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/player/pain{i}.ogg") for i in range(3)
        ]

        grunt_death = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/grunt/death{i}.ogg") for i in range(3)
        ]

        heavy_death = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/heavy/death{i}.ogg") for i in range(3)
        ]

        boss_death = [
            pg.mixer.Sound(Config.SOUNDS_FOLDER + f"ennemies/boss/death{i}.ogg") for i in range(3)
        ]

        player_death = player_hurt


        self.sound_ids = {
            "weapon" : debug_weapon_sound,
            "dry_weapon" : debug_dry_fire_sound,
            "dryfire" : dry_fire_sound,
            "pistol" : pistol_sound,
            "rifle" : rifle_sound,
            "punch" : punch_sound,
            "shotgun" : shotgun_sound,
            "superweapon" : superweapon_sound,

            "pickable": pickable_generic,
            "mine": mine_sound,

            "grunt_hurt": grunt_hurt,
            "heavy_hurt": heavy_hurt,
            "boss_hurt": boss_hurt,
            "player_hurt": player_hurt,

            "grunt_death": grunt_death,
            "heavy_death": heavy_death,
            "boss_death": boss_death,
            "player_death": player_death,
        }

        self.musics = listdir(Config.SOUNDS_FOLDER + "musics")
        self.end_music_time = -1
        self.current_music = choice(self.musics)
        self.musics.remove(self.current_music)
        pg.mixer.music.set_volume(.7)

        self.effect_volume = 1

        self.player_channel = pg.mixer.find_channel()
    

    def play_sound(self, id, player_pos, sound_pos, is_player=False):
        s = choice(self.sound_ids[id])
        
        if is_player:
            self.player_channel.play(s)
            return
        
        hearing_sound_dist = WALL_WIDTH * 10
        x, y = player_pos - sound_pos
        dist_player_sound = hypot(x, y)

        volume = (hearing_sound_dist - dist_player_sound)/hearing_sound_dist
        volume *= self.effect_volume
        volume = 0 if volume < 0 else volume

        s.set_volume(volume)

        s.play()

    def update_music(self):
        if pg.mixer.music.get_pos() == -1:
            self.next_music()
    
    def pause_music(self):
        pg.mixer.music.pause()
    
    def resume_music(self):
        pg.mixer.music.unpause()

    def next_music(self):
        old = self.current_music
        try:
            self.current_music = choice(self.musics)
            self.musics.remove(self.current_music)
            self.musics.append(old)
        except IndexError: # only one music in the folder
            pass
        
        music_path = Config.SOUNDS_FOLDER + "musics/" + self.current_music
        pg.mixer.music.load(music_path)
        pg.mixer.music.play()

    def set_music_volume(self, vol):
        """vol between 0 and 1, other values mean 1 for pygame"""
        pg.mixer.music.set_volume(vol)
    
    def shut_music(self):
        self.set_music_volume(0)

    def set_effect_volume(self, vol):
        self.player_channel.set_volume(vol)
        if vol < 0 or vol > 1:
            self.effect_volume = 1
        else:
            self.effect_volume = vol
