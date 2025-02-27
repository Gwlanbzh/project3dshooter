from weapons import Pistol, Shotgun, Rifle, SuperWeapon
from render.sprites import SpriteStruct
from bodys.pickables.pickable import Pickable


class PickableWeapon(Pickable):
    """
    Generic class for pickable weapons. Never instanciated itself.
    """
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = Pistol
        self.provided_ammo = 10
    
    def update(self):
        picker = self.picker()
        if picker != None:
            if self.provided_weapon not in picker.weapons:
                picker.weapons.add(self.provided_weapon)
            picker.ammo += self.provided_ammo
            picker.ammo = min(picker.ammo, picker.max_ammo)
            self.game.sound.play_sound("pickable", self.game.world.players[0].r, self.r)
            return True
        return False


class PickableShotgun(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = Shotgun
        self.provided_ammo = 20

        self.model = "shotgun.png"
        self.height = 40
    

class PickableRifle(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = Rifle
        self.provided_ammo = 20

        self.model = "rifle.png"
        self.height = 40

class PickableSuperWeapon(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = SuperWeapon
        self.provided_ammo = 40

        self.model = "minigun.png"
        self.height = 40
