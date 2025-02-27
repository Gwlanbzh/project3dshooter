from pygame import Vector2 as v2
import pygame as pg
from math import *
from bodys import Body
from config import *
from weapons import *
from render import SpriteStruct

class Creature(Body):
    """
    Body with implemented physics, life etc.
    """
    def __init__(self, game, r : tuple):
        """
        Spawns a Creature.
        
        Inputs:
            game: Game
            r : tuple
        
        Output:
            Creature
        """
        super().__init__(game, r) 
        self.orientation = 0 # arbitrary value for init
        self.max_health = 200
        self.health = self.max_health
        self.current_weapon = Pistol()

        # graphics 
        self.dead_model = "dead_mob.png"
        self.model = "grunt"

        #  required for walking animation sprites animations*
        self.walking = False
        self.walking_frame_time = 0
        self.img_index = 0
        
        # timings to paralyze mob when he is touched
        self.hurt_time = -1000
        self.hurt_time_duration = 200


    def in_wall(self, pos):
        x , y = pos
        world = self.game.world.map.grid
        return world[int((y)//100)][int((x)//100)] not in [0, 9]

    def not_colliding(self, dx, dy):
        """
        return a tuple :
            first element is x_permission for moving
            second element is y_permission for moving
        """
        x, y = self.r
        # respectivly signe of dx and dy 
        sdx = (copysign(1,dx))
        sdy = (copysign(1,dy))
        sqrt2 = 0.80
        #     2
        #   1   3
        # 4       6
        #   7   9
        #     8
        posx13  = (x + sqrt2*(sdx*self.size) , y + sqrt2*(sdx*self.size))
        posx79  = (x + sqrt2*(sdx*self.size) , y - sqrt2*(sdx*self.size))
        posy13  = (x + sqrt2*(sdy*self.size) , y + sqrt2*(sdy*self.size))
        posy79  = (x - sqrt2*(sdy*self.size) , y + sqrt2*(sdy*self.size))
        posx46 = (x + sdx*(self.size+5) , y) 
        posy28 = (x , y + sdy*(self.size+5))


        # print (dy,dx,sdy,sdx)
        if self.game.draw2d:
            pg.draw.line(self.game.window,'purple', (self.r),(posx46),10) 
            pg.draw.line(self.game.window,'purple', (self.r),(posy28),10) 
            pg.draw.line(self.game.window,'orange', (self.r),(posx13),5) 
            pg.draw.line(self.game.window,'pink', (self.r),(posx79),5) 
            pg.draw.line(self.game.window,'brown', (self.r),(posy13),5) 
            pg.draw.line(self.game.window,'cyan', (self.r),(posx79),5) 


        return (
            not (self.in_wall(posx46) 
                or self.in_wall(posx13) 
                or self.in_wall(posx79)
                ),
            not (self.in_wall(posy28) 
                or self.in_wall(posy13) 
                or self.in_wall(posy79)
                )
        )

    def is_dead(self):
        return self.health == 0

    def hurt(self, damages):
        self.hurt_time = pg.time.get_ticks()
        self.health = max(0, self.health - damages)
        is_p = (self.model == "player")
        if self.health == 0:
            self.game.sound.play_sound(f"{self.model}_death", self.game.world.players[0].r, self.r, is_player=is_p)
        else:
            self.game.sound.play_sound(f"{self.model}_hurt", self.game.world.players[0].r, self.r, is_player=is_p)

    def draw(self, game): # might be move into Creature or Body
        render_pos = super().draw(game)

        # vie
        pg.draw.line(game.window, "red",(render_pos.x - self.max_health/4, render_pos.y - self.size - 5), (render_pos.x + self.max_health/4, render_pos.y - self.size - 5), 3)
        pg.draw.line(game.window, "green",(render_pos.x - self.max_health/4, render_pos.y - self.size - 5), (render_pos.x - self.max_health/4 + self.health/2, render_pos.y - self.size - 5), 3)

        self.current_weapon.draw2d(game.window, render_pos, self.orientation)
    
    def get_sprite(self):
        h = self.height
        if self.is_dead():
            data = self.game.world.ressources.static_sprites[f"{self.model}/dead.png"]
            w = len(data) * h / data[0].get_height()
            return SpriteStruct(data, h, w)

        t = pg.time.get_ticks()
        if t - self.hurt_time < self.hurt_time_duration:
            data = self.game.world.ressources.static_sprites[f"{self.model}/shooted.png"]
            w = len(data) * h / data[0].get_height()
            return SpriteStruct(data, h, w)
        
        if t - self.current_weapon.last_shot_time < 100:
            data = self.game.world.ressources.static_sprites[f"{self.model}/firing.png"]
            w = len(data) * h / data[0].get_height()
            return SpriteStruct(data, h, w)

        if self.walking:
            frames = self.game.world.ressources.animated_sprites[f"{self.model}/walking"]
            if t - self.walking_frame_time > 100:
                self.walking_frame_time = t
                self.img_index = (self.img_index + 1)%len(frames)
            data = frames[self.img_index]
            w = len(data) * h / data[0].get_height()
            return SpriteStruct(data, h, w)
        
        data = self.game.world.ressources.static_sprites[f"{self.model}/static.png"]
        w = len(data) * h / data[0].get_height()
        return SpriteStruct(data, h, w)
