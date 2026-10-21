from dataclasses import dataclass
from .combat import BattleReport, Outcome, Battle
from .core import Dice, UnknownCodeException
from .enemy import Enemy
from .item import Item, ItemCatalog, DefaultCatalog

@dataclass
class Rewards:
    experience: int
    gold: int
    loot: Item
    levels_gained: int

@dataclass
class ExpeditionReport:
    seed: int
    location_code: str
    battle: BattleReport
    rewards: Rewards

class Location:
    LOOT_CHANCE = 0.6
    ENCHANT_CHANCE = 0.3

    def __init__(self, code, display_name, recommended_level, catalog: ItemCatalog):
        self.code = code
        self.display_name = display_name
        self.recommended_level = recommended_level
        self.catalog = catalog

    def create_enemy(self) -> Enemy:
        pass

    def get_loot_table(self) -> list:
        pass

    def explore(self, hero, seed=None) -> ExpeditionReport:
        dice = Dice()
        if seed is None:
            seed = dice.next_seed()
        dice.reseed(seed)

        hero.restore_health()
        enemy = self.create_enemy()
        battle = Battle(hero, enemy)
        battle_report = battle.run()

        if battle_report.outcome == Outcome.VICTORY:
            rewards = self._reward(hero, enemy, dice)
        else:
            rewards = self._punish(hero)

        return ExpeditionReport(seed, self.code, battle_report, rewards)

    def _reward(self, hero, enemy, dice) -> Rewards:
        experience = enemy.get_experience_reward()
        gold = enemy.roll_gold_reward()
        loot = self._roll_loot(dice)

        levels_gained = hero.gain_experience(experience)
        hero.add_gold(gold)
        if loot:
            hero.add_item(loot)

        return Rewards(experience, gold, loot, levels_gained)

    def _roll_loot(self, dice) -> Item:
        if not dice.chance(self.LOOT_CHANCE):
            return None
        loot = self.catalog.create(dice.pick(self.get_loot_table()))
        if dice.chance(self.ENCHANT_CHANCE):
            loot.enchant(dice.pick(loot.get_possible_enchantments()))
        return loot

    def _punish(self, hero) -> Rewards:
        lost_gold = hero.get_gold() // 2
        hero.spend_gold(lost_gold)
        return Rewards(0, -lost_gold, None, 0)

    def get_code(self) -> str: return self.code
    def get_display_name(self) -> str: return self.display_name
    def get_recommended_level(self) -> int: return self.recommended_level


class Forest(Location):
    def __init__(self, catalog):
        super().__init__("forest", "Мистический лес", 1, catalog)

    def create_enemy(self):
        from .enemy import Goblin
        return Goblin()

    def get_loot_table(self):
        return [DefaultCatalog.GOBLIN_CLEAVER, DefaultCatalog.HUNTING_BOW, DefaultCatalog.LEATHER_ARMOR]


class Crypt(Location):
    def __init__(self, catalog):
        super().__init__("crypt", "Заброшенный склеп", 3, catalog)

    def create_enemy(self):
        from .enemy import Skeleton
        return Skeleton()

    def get_loot_table(self):
        return [DefaultCatalog.KNIGHT_BLADE, DefaultCatalog.BONE_BOW, DefaultCatalog.NECROMANCER_STAFF, DefaultCatalog.CRYPT_MAIL]


class DragonLair(Location):
    def __init__(self, catalog):
        super().__init__("dragon-lair", "Логово дракона", 5, catalog)

    def create_enemy(self):
        from .enemy import Dragon
        return Dragon()

    def get_loot_table(self):
        return [DefaultCatalog.DAWN_BLADE, DefaultCatalog.DRAGONSCALE_ARMOR]


class LocationRegistry:
    def __init__(self, locations: list):
        self.locations = {loc.get_code(): loc for loc in locations}

    def get(self, code: str) -> Location:
        loc = self.locations.get(code)
        if loc is None:
            raise UnknownCodeException("Локация", code)
        return loc

    def get_all(self) -> list:
        return list(self.locations.values())