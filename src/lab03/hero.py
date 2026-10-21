import math
from .combat import Combatant, Hit
from .item import Item, Weapon, Armor
from .kit import StarterKitFactory, WarriorKitFactory, RangerKitFactory, MageKitFactory
from .core import UnknownCodeException

class HeroClass:
    def __init__(self, code, display_name, base_health, kit_factory_class):
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self.kit_factory_class = kit_factory_class

    def get_starter_kit(self, catalog) -> StarterKitFactory:
        return self.kit_factory_class(catalog)

HeroClass.WARRIOR = HeroClass("warrior", "Воин", 120, WarriorKitFactory)
HeroClass.RANGER = HeroClass("ranger", "Следопыт", 100, RangerKitFactory)
HeroClass.MAGE = HeroClass("mage", "Маг", 85, MageKitFactory)

HeroClass.ALL = [HeroClass.WARRIOR, HeroClass.RANGER, HeroClass.MAGE]

def get_hero_class_by_code(code: str) -> HeroClass:
    for hc in HeroClass.ALL:
        if hc.code == code:
            return hc
    raise UnknownCodeException("Класс героя", code)


class Hero(Combatant):
    MAX_NAME_LENGTH = 20
    STARTING_GOLD = 50
    HEALTH_PER_LEVEL = 15
    DAMAGE_PER_LEVEL = 3
    EXPERIENCE_PER_LEVEL = 100

    def __init__(self, builder):
        self.name = builder.name
        self.hero_class = builder.hero_class
        self.level = builder.level
        self.experience = 0
        self.gold = builder.gold
        self.weapon = builder.weapon
        self.armor = builder.armor
        self.inventory = []
        self.health = self.get_max_health()

    def get_code(self) -> str: return self.hero_class.code
    def get_name(self) -> str: return self.name
    def get_health(self) -> int: return self.health
    def get_max_health(self) -> int: return self.hero_class.base_health + (self.level - 1) * Hero.HEALTH_PER_LEVEL
    def get_hero_class(self) -> HeroClass: return self.hero_class
    def get_level(self) -> int: return self.level
    def get_experience(self) -> int: return self.experience
    def get_experience_to_next_level(self) -> int: return self.level * Hero.EXPERIENCE_PER_LEVEL
    def get_gold(self) -> int: return self.gold
    def get_weapon(self) -> Weapon: return self.weapon
    def get_armor(self) -> Armor: return self.armor
    def get_inventory(self) -> list: return list(self.inventory)

    def is_alive(self) -> bool:
        return self.health > 0

    def restore_health(self):
        self.health = self.get_max_health()

    def gain_experience(self, amount: int) -> int:
        self.experience += amount
        levels_gained = 0
        while self.experience >= self.get_experience_to_next_level():
            self.experience -= self.get_experience_to_next_level()
            self.level += 1
            levels_gained += 1
        return levels_gained

    def add_gold(self, amount: int):
        self.gold += amount

    def spend_gold(self, amount: int):
        if amount > self.gold:
            raise ValueError(f"Не хватает золота: нужно {amount}, есть {self.gold}")
        self.gold -= amount

    def add_item(self, item: Item):
        self.inventory.append(item)

    def remove_item(self, item: Item):
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            raise ValueError(f"В инвентаре нет предмета {item.get_name()}")

    def equip(self, item: Item):
        if isinstance(item, Weapon):
            self.remove_item(item)
            if self.weapon:
                self.inventory.append(self.weapon)
            self.weapon = item
        elif isinstance(item, Armor):
            self.remove_item(item)
            if self.armor:
                self.inventory.append(self.armor)
            self.armor = item
        else:
            raise ValueError(f"Предмет нельзя экипировать: {item.get_name()}")

    def roll_damage(self) -> Hit:
        hit = self.weapon.roll_damage()
        return Hit(hit.damage + (self.level - 1) * Hero.DAMAGE_PER_LEVEL, hit.critical)

    def receive_hit(self, damage: int) -> int:
        reduced_damage = round(damage * (1 - self.armor.get_defense()))
        dealt = max(1, reduced_damage)
        self.health = max(0, self.health - dealt)
        return dealt

    class Builder:
        def __init__(self):
            self.name = None
            self.hero_class = None
            self.weapon = None
            self.armor = None
            self.level = 1
            self.gold = Hero.STARTING_GOLD

        def set_name(self, name: str) -> 'Hero.Builder':
            self.name = name
            return self

        def set_hero_class(self, hero_class: HeroClass) -> 'Hero.Builder':
            self.hero_class = hero_class
            return self

        def set_weapon(self, weapon: Weapon) -> 'Hero.Builder':
            self.weapon = weapon
            return self

        def set_armor(self, armor: Armor) -> 'Hero.Builder':
            self.armor = armor
            return self

        def set_starter_kit(self, starter_kit: StarterKitFactory) -> 'Hero.Builder':
            self.weapon = starter_kit.create_weapon()
            self.armor = starter_kit.create_armor()
            return self

        def set_level(self, level: int) -> 'Hero.Builder':
            self.level = level
            return self

        def set_gold(self, gold: int) -> 'Hero.Builder':
            self.gold = gold
            return self

        def build(self) -> 'Hero':
            if not self.name or not self.name.strip():
                raise ValueError("У героя должно быть имя")
            if len(self.name) > Hero.MAX_NAME_LENGTH:
                raise ValueError(f"Имя героя не может быть длиннее {Hero.MAX_NAME_LENGTH} символов")
            if not self.hero_class:
                raise ValueError("Не выбран класс героя")
            if not self.weapon or not self.armor:
                raise ValueError("Герою нужны оружие и броня")
            if self.level < 1:
                raise ValueError("Уровень героя не может быть меньше 1")
            if self.gold < 0:
                raise ValueError("Золота не может быть меньше нуля")
            return Hero(self)