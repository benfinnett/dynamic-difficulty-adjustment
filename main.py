from time import sleep
from dda import GameMetricController
from game import Game

def print_round_info() -> None:
    print(f"""
Round {game.round}:
    Enemies: {game.get_round_enemies()} ({'' if enemies_difference < 0 else '+'}{enemies_difference})
    Enemy Health: {game.get_round_enemy_health()} ({'' if enemy_health_difference < 0 else '+'}{enemy_health_difference})
    Enemy Speed: {game.get_round_enemy_speed()} ({'' if enemy_speed_difference < 0 else '+'}{enemy_speed_difference})
    Coins: {game.player_coins}
    Lives: {game.lives * '♥️ '}
    """)

# Driver code - entry to program
if __name__ == "__main__":
    print("--------- Tower Defence Game ---------")
    game = Game()

    enemies_per_tower_dda = GameMetricController(
        metric=game.get_enemies_per_tower, 
        modifiers=[[game.set_enemies_modifier, 1]], 
        setpoint=10,
        kp=0.2,
        ki=0.1,
        kd=0.5
    )

    input("Press Enter to start!")
    dda_outputs: list[float] = []

    while True:
        print("===========================================")
        enemies_difference = game.get_round_enemies() - game.get_round_enemies(game.round - 1)
        enemy_health_difference = game.get_round_enemy_health() - game.get_round_enemy_health(game.round - 1)
        enemy_speed_difference = game.get_round_enemy_speed() - game.get_round_enemy_speed(game.round - 1)
        
        print_round_info()
        
        game.print_towers()

        # Add new towers
        while (game.player_coins > 0) and (input("\nAdd a new tower? (y/n)\n> ").lower() in ["y", "yes"]):
            print("--------------------------------------")
            print(f"Coins: {game.player_coins}")
            print("""\nSelect a tower to purchase:
    1) Normal (30 coins)
    2) Heavy (100 coins)
    3) Speed (50 coins)""")
            tower_costs = {
                1: 30, 
                2: 100, 
                3: 50
            }
            
            try:
                user_selection = int(input("> "))
            except ValueError:
                print("Invalid input!")
                continue

            if user_selection < 1 or user_selection > 3:
                print("Invalid input!")
                continue

            if game.player_coins >= tower_costs[user_selection]:
                game.player_coins -= tower_costs[user_selection]
            else:
                print("You don't have enough coins for that tower!")
                continue
            game.add_tower(user_selection)
            game.print_towers()

        game.distribute_towers()

        input("\nPress Enter to start the round.")

        game.generate_enemies()
        loop = 0
        game.enemies[loop].active = True
        enemy = None
        while (len(game.get_active_enemies()) > 0):
            # Adjust enemy positions
            for enemy in game.enemies:
                if not enemy.active:
                    continue

                enemy.move()

                # If an enemy goes beyond the map length, a life should be lost
                if enemy.position > game.map_length:
                    enemy.active = False
                    game.lives -= 1
                    life_plural = "life" if game.lives == 1 else "lives"
                    print(f"[GAME] An enemy made it through your defences! {game.lives} {life_plural} left!")

                    # The game ends when the player has no lives left
                    if game.lives == 0:
                        game.exit()
            
            # Calculate tower damage
            for tower in game.towers:
                if not enemy:
                    raise ValueError("Enemy not bound. Call Game.generate_enemies first.")

                nearby_enemies_condition = tower.location - tower.range <= enemy.position <= tower.location + tower.range
                nearby_enemies = [enemy for enemy in game.enemies if nearby_enemies_condition and enemy.active]
                targets = tower.attack(nearby_enemies)
                for target in targets:
                    if target.health <= 0:
                        target.active = False
                        game.player_coins += 1

            # Activate next enemy
            loop += 1
            if loop < len(game.enemies):
                game.enemies[loop].active = True
            
            # Print round info
            game.print_round_info()

            # Sleep for dramatic effect
            sleep(0.1)
        print("==============================================")
        print("Round complete!")
        game.player_coins += game.round * 10
        dda_outputs.append(enemies_per_tower_dda.evaluate_performance())
        enemies_per_tower_dda.update_modifiers()
        game.round += 1