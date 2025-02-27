from render.sprites import SpriteStruct
from bodys.pickables.pickable import Pickable


class AmmoPack10(Pickable):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.supply_value = 5
        
        self.model = "ammo_mini.png"
        self.height = 35
    
    def update(self):
        picker = self.picker()
        if picker != None and picker.ammo < picker.max_ammo:
            picker.ammo += self.supply_value
            picker.ammo = min(picker.ammo, picker.max_ammo)
            self.game.sound.play_sound("pickable", self.game.world.players[0].r, self.r)
            return True
        return False

class AmmoPack50(AmmoPack10):
    def __init__(self, game, r):
        super().__init__(game, r)
        
        self.supply_value = 25

        self.model = "ammo_mega.png"
        self.height = 50
