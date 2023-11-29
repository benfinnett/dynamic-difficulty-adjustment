from random import randint

class Enemy:
    def __init__(self, id: int, health: int, movement_speed: int):
        self.id = id
        self.health = health
        self.movement_speed = movement_speed
        self.position = 0
        self.active = False

    def move(self) -> None:
        self.position += randint(self.movement_speed // 4, self.movement_speed)