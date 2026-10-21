from abc import ABC, abstractmethod
from .core import Dice, UnknownCodeException

class Enchantment:
    def __init__(self, code, name, bonus_damage, bonus_defense, bonus_price):
        self.code = code
        self.name = name
        self.bonus_damage = bonus_damage
        self.bonus_defense = bonus_defense
        self.bonus_price = bonus_price

Enchantment.SHARP = Enchantment("sharp", "Острое", 3, 0, 20)
Enchantment.FIERY = Enchantment("fiery", "Огненное", 6, 0, 50)
Enchantment.STURDY = Enchantment("sturdy", "Прочное", 0, 0.05, 20)
Enchantment.WARDING = Enchantment("warding", "Охранное", 0, 0.10, 50)

Enchantment.FOR_WEAPONS = [Enchantment.SHARP, Enchantment.FIERY]
Enchantment.FOR_ARMOR = [Enchantment.STURDY, Enchantment.WARDING]


class Item(ABC):
    def __init__(self, code, name, base_price):
        self.code = code
        self.name = name
        self.base_price = base_price
        self.enchantments = []

    def copy(self) -> 'Item':
        pass

    def get_possible_enchantments(self) -> list:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    def enchant(self, enchantment: Enchantment):
        if enchantment not in self.get_possible_enchantments():
            raise ValueError(f"Зачарование '{enchantment.name}' не подходит для предмета '{self.name}'")
        self.enchantments.append(enchantment)

    def get_code(self) -> str:
        return self.code

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> int:
        price = self.base_price
        for enc in self.enchantments:
            price += enc.bonus_price
        return price

    def get_enchantments(self) -> list:
        return list(self.enchantments)


class Weapon(Item):
    def __init__(self, code, name, base_price, damage):
        super().__init__(code, name, base_price)
        self.damage = damage

    def copy(self) -> 'Weapon':
        pass

    def get_damage(self) -> int:
        total = self.damage
        for enc in self.enchantments:
            total += enc.bonus_damage
        return total

    def get_possible_enchantments(self) -> list:
        return Enchantment.FOR_WEAPONS


class Sword(Weapon):
    def __init__(self, code, name, base_price, damage):
        super().__init__(code, name, base_price, damage)

    def copy(self) -> 'Sword':
        new_item = Sword(self.code, self.name, self.base_price, self.damage)
        new_item.enchantments = list(self.enchantments)
        return new_item

    def roll_damage(self):
        from .combat import Hit
        return Hit(self.get_damage(), False)

    def get_description(self) -> str:
        return f"урон {self.get_damage()}"


class Bow(Weapon):
    def __init__(self, code, name, base_price, damage, critical_chance):
        super().__init__(code, name, base_price, damage)
        self.critical_chance = critical_chance

    def copy(self) -> 'Bow':
        new_item = Bow(self.code, self.name, self.base_price, self.damage, self.critical_chance)
        new_item.enchantments = list(self.enchantments)
        return new_item

    def roll_damage(self):
        from .combat import Hit
        if Dice().chance(self.critical_chance):
            return Hit(self.get_damage() * 2, True)
        return Hit(self.get_damage(), False)

    def get_description(self) -> str:
        return f"урон {self.get_damage()}, шанс крита {round(self.critical_chance * 100)}%"


class Staff(Weapon):
    def __init__(self, code, name, base_price, damage, scatter):
        super().__init__(code, name, base_price, damage)
        self.scatter = scatter

    def copy(self) -> 'Staff':
        new_item = Staff(self.code, self.name, self.base_price, self.damage, self.scatter)
        new_item.enchantments = list(self.enchantments)
        return new_item

    def roll_damage(self):
        from .combat import Hit
        min_d = round(self.get_damage() * (1 - self.scatter))
        max_d = round(self.get_damage() * (1 + self.scatter))
        return Hit(Dice().roll(min_d, max_d), False)

    def get_description(self) -> str:
        min_d = round(self.get_damage() * (1 - self.scatter))
        max_d = round(self.get_damage() * (1 + self.scatter))
        return f"урон {min_d}-{max_d}"


class Armor(Item):
    MAX_DEFENSE = 0.75

    def __init__(self, code, name, base_price, defense):
        super().__init__(code, name, base_price)
        self.defense = defense

    def copy(self) -> 'Armor':
        new_item = Armor(self.code, self.name, self.base_price, self.defense)
        new_item.enchantments = list(self.enchantments)
        return new_item

    def get_defense(self) -> float:
        total = self.defense
        for enc in self.enchantments:
            total += enc.bonus_defense
        return min(total, self.MAX_DEFENSE)

    def get_possible_enchantments(self) -> list:
        return Enchantment.FOR_ARMOR

    def get_description(self) -> str:
        return f"защита {round(self.get_defense() * 100)}%"


class ItemCatalog:
    def __init__(self):
        self.prototypes = {}

    def register(self, prototype: Item):
        self.prototypes[prototype.get_code()] = prototype

    def create(self, code: str) -> Item:
        prototype = self.prototypes.get(code)
        if prototype is None:
            raise UnknownCodeException("Предмет", code)
        return prototype.copy()

    def create_weapon(self, code: str) -> Weapon:
        item = self.create(code)
        if not isinstance(item, Weapon):
            raise ValueError(f"Предмет '{code}' не является оружием")
        return item

    def create_armor(self, code: str) -> Armor:
        item = self.create(code)
        if not isinstance(item, Armor):
            raise ValueError(f"Предмет '{code}' не является броней")
        return item


class DefaultCatalog:
    TRAINING_SWORD = "training-sword"
    HUNTING_BOW = "hunting-bow"
    APPRENTICE_STAFF = "apprentice-staff"
    CHAINMAIL = "chainmail"
    LEATHER_ARMOR = "leather-armor"
    LINEN_ROBE = "linen-robe"

    IRON_SWORD = "iron-sword"
    ELVEN_BOW = "elven-bow"
    EMBER_STAFF = "ember-staff"
    PLATE_ARMOR = "plate-armor"

    GOBLIN_CLEAVER = "goblin-cleaver"
    BONE_BOW = "bone-bow"
    NECROMANCER_STAFF = "necromancer-staff"
    KNIGHT_BLADE = "knight-blade"
    CRYPT_MAIL = "crypt-mail"
    DAWN_BLADE = "dawn-blade"
    DRAGONSCALE_ARMOR = "dragonscale-armor"

    @staticmethod
    def create() -> ItemCatalog:
        catalog = ItemCatalog()

        catalog.register(Sword(DefaultCatalog.TRAINING_SWORD, "Тренировочный меч", 20, 12))
        catalog.register(Bow(DefaultCatalog.HUNTING_BOW, "Охотничий лук", 20, 10, 0.3))
        catalog.register(Staff(DefaultCatalog.APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.3))
        catalog.register(Armor(DefaultCatalog.CHAINMAIL, "Кольчуга", 40, 0.3))
        catalog.register(Armor(DefaultCatalog.LEATHER_ARMOR, "Кожаная броня", 30, 0.2))
        catalog.register(Armor(DefaultCatalog.LINEN_ROBE, "Льняная роба", 15, 0.1))

        catalog.register(Sword(DefaultCatalog.IRON_SWORD, "Железный меч", 80, 17))
        catalog.register(Bow(DefaultCatalog.ELVEN_BOW, "Эльфийский лук", 90, 14, 0.4))
        catalog.register(Staff(DefaultCatalog.EMBER_STAFF, "Тлеющий посох", 90, 20, 0.3))
        catalog.register(Armor(DefaultCatalog.PLATE_ARMOR, "Латы", 120, 0.4))

        catalog.register(Sword(DefaultCatalog.GOBLIN_CLEAVER, "Гоблинский тесак", 40, 15))
        catalog.register(Bow(DefaultCatalog.BONE_BOW, "Костяной лук", 140, 17, 0.4))
        catalog.register(Staff(DefaultCatalog.NECROMANCER_STAFF, "Посох некроманта", 150, 25, 0.35))
        catalog.register(Sword(DefaultCatalog.KNIGHT_BLADE, "Клинок рыцаря", 150, 23))
        catalog.register(Armor(DefaultCatalog.CRYPT_MAIL, "Кольчуга стража склепа", 160, 0.45))
        catalog.register(Sword(DefaultCatalog.DAWN_BLADE, "Клинок рассвета", 500, 35))
        catalog.register(Armor(DefaultCatalog.DRAGONSCALE_ARMOR, "Драконья чешуя", 500, 0.55))

        return catalog