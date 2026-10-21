import math
from .combat import Combatant, Hit
from .core import Dice

class Enemy(Combatant):
    def get_experience_reward(self) -> int: pass
    def roll_gold_reward(self) -> int: pass

class AbstractEnemy(Enemy):
    def __init__(self, code, name, max_health, min_damage, max_damage, exp_reward, gold_reward):
        self.code = code
        self.name = name
        self.max_health = max_health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.health = max_health

    def get_code(self) -> str: return self.code
    def get_name(self) -> str: return self.name
    def get_health(self) -> int: return self.health
    def get_max_health(self) -> int: return self.max_health
    def is_alive(self) -> bool: return self.health > 0
    def roll_damage(self) -> Hit: return Hit(Dice().roll(self.min_damage, self.max_damage), False)
    
    def receive_hit(self, damage: int) -> int:
        dealt = max(1, self.reduce_damage(damage))
        self.health = max(0, self.health - dealt)
        return dealt

    def reduce_damage(self, damage: int) -> int:
        return damage

    def roll_gold_reward(self) -> int:
        return Dice().roll(self.gold_reward // 2, self.gold_reward)

    def get_experience_reward(self) -> int:
        return self.exp_reward

class Goblin(AbstractEnemy):
    def __init__(self):
        super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)

class Skeleton(AbstractEnemy):
    def __init__(self):
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)

    def reduce_damage(self, damage: int) -> int:
        return round(damage * (1 - 0.3))

class Dragon(AbstractEnemy):
    def __init__(self):
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)

    def reduce_damage(self, damage: int) -> int:
        return round(damage * (1 - 0.25))

    def roll_damage(self) -> Hit:
        bite = super().roll_damage()
        if Dice().chance(0.25):
            return Hit(bite.damage * 2, True)
        return bite