from components.enemy import Enemy

class Tower:
    def __init__(self, id:int, damage:int, fire_rate:int, range:int):
        self.id = id
        self.damage = damage 
        self.fire_rate = fire_rate
        self.range = range
        self.location = 0
    
    def attack(self, nearby_enemies: list[Enemy]) -> list[Enemy]:
        targets = sorted(nearby_enemies, key=lambda enemy: enemy.health)[:self.fire_rate]
        for target in targets:
            target.health -= self.damage
        return targets