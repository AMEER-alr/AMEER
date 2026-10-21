from abc import ABC, abstractmethod
from .item import DefaultCatalog, ItemCatalog, Armor, Weapon

class StarterKitFactory(ABC):
    @abstractmethod
    def create_weapon(self) -> Weapon: pass

    @abstractmethod
    def create_armor(self) -> Armor: pass

class WarriorKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Weapon:
        return self.catalog.create_weapon(DefaultCatalog.TRAINING_SWORD)

    def create_armor(self) -> Armor:
        return self.catalog.create_armor(DefaultCatalog.CHAINMAIL)

class RangerKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Weapon:
        return self.catalog.create_weapon(DefaultCatalog.HUNTING_BOW)

    def create_armor(self) -> Armor:
        return self.catalog.create_armor(DefaultCatalog.LEATHER_ARMOR)

class MageKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Weapon:
        return self.catalog.create_weapon(DefaultCatalog.APPRENTICE_STAFF)

    def create_armor(self) -> Armor:
        return self.catalog.create_armor(DefaultCatalog.LINEN_ROBE)