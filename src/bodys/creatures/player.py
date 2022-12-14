import pygame as pg
from math import cos, sin, hypot
from config import Config
from bodys import Creature
from weapons import *
from math import tau

class Player(Creature):
    """
    Controllable Creature with weapons.
    """
    def __init__(self, game, r):
        """
        Spawns a Player.
        
        Inputs:
            game : Game
            r : tuple
        
        Outputs:
            Player
        """
        super().__init__(game,r)
        self.heal_recovery_time = 10000 # valeur arbitraire
        self.color = 'blue'
        self.vorientation = 0
        # TODO add ammo data structure

        # weapons attributes
        self.weapons = []
        self.current_weapon = Weapon()
        self.ammo = 0 # may change to dict ?

    def update(self): # might be move into Creature or Body
        self.move()
        # heal
        # status, maybe buff / debuff
        # TODO : not logical to call self.get_inputs, call self.move() instead would be better
    
    
    def get_inputs(self):
        """
        Returns a force_vector based on the physical player's inputs.
        TODO maybye refactoring get inputs and mouvement call
        """
        moves = set()

        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            moves.add(2)
        if keys[pg.K_s]:
            moves.add(3)
        if keys[pg.K_q]:
            moves.add(1)
        if keys[pg.K_d]:
            moves.add(4)
        
        # sera géré par la souris plus tard
        if keys[pg.K_e]:
            self.rotate(-1)
        if keys[pg.K_a]:
            self.rotate(1)
        
        if keys[pg.K_o]:
            self.vorientation = min(self.vorientation + Config.PLAYER_VERT_ROT_SPEED, Config.PLAYER_MAX_VERT_ROT)
        if keys[pg.K_k]:
            self.vorientation = max(self.vorientation - Config.PLAYER_VERT_ROT_SPEED, -Config.PLAYER_MAX_VERT_ROT)
        
        left_click, _, _ = pg.mouse.get_pressed()
        if left_click:
            self.current_weapon.hit_scan(self.r, self.orientation, self.game.world.mobs)

        return moves
    
    def move(self):
        """
        TODO maybye refactoring get inputs and mouvement call
        Applies Newton's Second Principle then handles collisions
        with walls, props and mobs. FIXME text not true now
        direction meaning
          2
        1 + 4
          3
        
        Inputs:
            direction
        
        Output:
            Alter Creature position
        """

        moves = self.get_inputs()

        dt = self.game.delta_time # may be change to a const but there might be a use for it in future when framerate will be unsure
        speed = Config.PLAYER_V * dt 
        V_sin = sin(self.orientation) 
        V_cos = cos(self.orientation) 

        dx = 0
        dy = 0
        if 1 in moves:
            # gauche
            dx += V_sin 
            dy += -V_cos 
        if 2 in moves:
            # devant
            dx += V_cos 
            dy += V_sin 
        if 3 in moves:
            # derrière
            dx += -V_cos 
            dy += -V_sin 
        if 4 in moves:
            # droite
            dx += -V_sin 
            dy += V_cos
        
        if dx != 0 or dy != 0:
            k = speed * (1/hypot(dx, dy))
            dx = k * dx
            dy = k * dy
        ## collision stuff goes here
        # world = self.game.world.map.map
        # if world[int((y + dy)//100)][int((x + dx)//100)] == 0:
        #     self.r = x + dx, y + dy

        x_permission, y_permission = self.not_colliding(dx, dy)
        if x_permission:
            self.r.x += dx
        if y_permission:
            self.r.y += dy


    def rotate(self, direction):
        dt = self.game.delta_time # may be change to a const but there might be a use for it in future when framerate will be unsure
        self.orientation -= direction * Config.PLAYER_ROT_SPEED * dt
        self.orientation %= tau

    def draw(self, game): # might be move into Creature or Body
        traylenght = self.current_weapon.range
        pg.draw.line(game.window,'yellow', (self.r),
                     (self.r[0]+ traylenght * cos(self.orientation),
                      self.r[1] + traylenght * sin(self.orientation)),2) 
        pg.draw.circle(game.window, self.color, self.r,15)
        pg.draw.line(game.window, "red",(self.r.x - 25, self.r.y - self.size - 5), (self.r.x + 25, self.r.y - self.size - 5))
        pg.draw.line(game.window, "green",(self.r.x - 25, self.r.y - self.size - 5), (self.r.x -25 + self.health/2, self.r.y - self.size - 5))
