from .core import UnknownCodeException
from .hero import Hero
from .item import ItemCatalog, Item

class Merchant:
    SELL_PRICE_PERCENT = 50

    def __init__(self, catalog: ItemCatalog, assortment: list):
        self.catalog = catalog
        self.assortment = list(assortment)

    def get_showcase(self) -> list:
        return [self.catalog.create(code) for code in self.assortment]

    def buy(self, hero: Hero, code: str) -> Item:
        if code not in self.assortment:
            raise UnknownCodeException("Товар", code)

        item = self.catalog.create(code)
        hero.spend_gold(item.get_price())
        hero.add_item(item)
        return item

    def sell(self, hero: Hero, item: Item) -> int:
        price = self.get_sell_price(item)
        hero.remove_item(item)
        hero.add_gold(price)
        return price

    def get_sell_price(self, item: Item) -> int:
        return item.get_price() * self.SELL_PRICE_PERCENT // 100