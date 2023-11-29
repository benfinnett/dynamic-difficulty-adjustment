from pprint import pformat
from numpy import linspace
from components.enemy import Enemy
from components.tower import Tower

class Game:
    """
    Tower Defence Game

    Demonstrates the use of PID controllers to create a dynamic difficulty 
    adjustment system.
    """
    def __init__(self):
        # Game properties
        self.map_length = 1000
        self.round = 1
        self.lives = 3
        self.player_coins = 60
        self.towers: list[Tower] = []

        # Enemy properities
        self.enemies = []
        self.min_enemies = 10
        self.min_enemy_health = 60
        self.min_enemy_speed = 20
        self.enemies_modifier = [0, 0] # [previous_value, current_value]
        self.enemy_health_modifier = [0, 0]
        self.enemy_speed_modifier = [0, 0]

    def add_tower(self, tower_type: int) -> None:
        if tower_type == 1: # Normal
            self.towers.append(Tower(len(self.towers), 25, 2, 50))
        elif tower_type == 2: # Heavy
            self.towers.append(Tower(len(self.towers), 70, 1, 100))
        elif tower_type == 3: # Speed
            self.towers.append(Tower(len(self.towers), 10, 10, 75))

    def get_active_enemies(self) -> list:
        return [enemy for enemy in self.enemies if enemy.active]

    def distribute_towers(self):
        # Distribute towers equally along the map
        locations = linspace(0, self.map_length, num=len(self.towers))
        for i, tower in enumerate(self.towers):
            tower.location = round(locations[i])

    def generate_enemies(self):
        self.enemies = [
            Enemy(
                id, 
                self.get_round_enemy_health(), 
                self.get_round_enemy_speed()
            ) 
            for id in range(self.get_round_enemies())
        ]
        
    def get_round_enemies(self, game_round: int = 0) -> int:
        if game_round <= 0:
            game_round = self.round
            return self.min_enemies + round(.7 * (game_round - 1)) + self.enemies_modifier[-1]
        else:
            return self.min_enemies + round(.7 * (game_round - 1)) + self.enemies_modifier[0]
    
    def get_round_enemy_health(self, game_round: int = 0) -> int:
        if game_round <= 0:
            game_round = self.round
        return self.min_enemy_health + ((game_round - 1) * 10)
    
    def get_round_enemy_speed(self, game_round: int = 0) -> int:
        if game_round <= 0:
            game_round = self.round
        return self.min_enemy_speed  + ((game_round - 1) * 3)
    
    def get_enemies_per_tower(self) -> float:
        return self.get_round_enemies() / len(self.towers)
    
    def set_enemies_modifier(self, value: float):
        self.enemies_modifier.append(round(value))
        del self.enemies_modifier[0]
    
    def set_enemy_health_modifier(self, value: float):
        self.enemy_health_modifier.append(round(value))
        del self.enemy_health_modifier[0]
    
    def set_enemy_speed_modifier(self, value: float):
        self.enemy_speed_modifier.append(round(value))
        del self.enemy_speed_modifier[0]

    def exit(self):
        print("===========================================")
        print("GAME OVER!")
        print(f"Rounds survived: {self.round}")
        print(f"Towers built: {len(self.towers)}")
        raise SystemExit

    def print_towers(self):
        pretty_towers = '\n- '.join([pformat(tower.__dict__) for tower in self.towers])
        print(f"\nTowers:\n- {pretty_towers}")
    
    def print_round_info(self):
        last_enemy_position = min(self.get_active_enemies(), key=lambda enemy: enemy.position).position if self.get_active_enemies() else "N/A"
        output = f"""Round {self.round} Info:
    Enemies Alive: {len(self.get_active_enemies())}
    Lives Left: {self.lives * '♥️ '}
    Coins: {self.player_coins}
    Last Enemy Position: {last_enemy_position}
        """
        print(output)