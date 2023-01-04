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
    
    def update(self):
        picker = self.picker()
        if picker != None:
            picker.weapons.append(self.provided_weapon)
            return True
        return False


class PickableShotgun(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = Shotgun

        self.model = "shotgun.png"
        self.dims = 150, 40
    

class PickableRifle(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = Rifle

        self.model = "rifle.png"
        self.dims = 150, 40

class PickableSuperWeapon(PickableWeapon):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.provided_weapon = SuperWeapon

        self.model = "minigun.png"
        self.dims = 150, 40
