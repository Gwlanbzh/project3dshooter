from render.sprites import SpriteStruct
from bodys.pickables.pickable import Pickable


class HealthPack5(Pickable):
    def __init__(self, game, r):
        super().__init__(game, r)
        self.heal_value = 15

        self.model = "health_mini.png"
        self.height = 40
    
    def update(self):
        picker = self.picker()
        if picker != None and picker.health < picker.max_health:
            picker.health += self.heal_value
            picker.health = min(picker.health, picker.max_health)
            self.game.sound.play_sound("pickable", self.game.world.players[0].r, self.r)
            return True
        return False

class HealthPack25(HealthPack5):
    def __init__(self, game, r):
        super().__init__(game, r)
        self.heal_value = 60

        self.model = "health_mega.png"
        self.height = 60
