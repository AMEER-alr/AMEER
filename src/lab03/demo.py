from .core import Dice
from .hero import Hero, HeroClass
from .item import DefaultCatalog, Enchantment
from .world import Forest, Crypt

def run_demo():
    catalog = DefaultCatalog.create()

    print("===== Одиночка =====")
    first = Dice()
    second = Dice()
    print(f"Dice.getInstance() возвращает один и тот же объект: {first is second}")

    print("\n===== Прототип =====")
    plain_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword.enchant(Enchantment.FIERY)
    
    from .view import ConsoleView
    view = ConsoleView()
    print(f"Первая копия:        {view.describe(plain_sword)}")
    print(f"Вторая копия:        {view.describe(fiery_sword)}")
    print(f"Новая копия шаблона: {view.describe(catalog.create(DefaultCatalog.IRON_SWORD))}")
    print(f"Копии - разные объекты: {plain_sword is not fiery_sword}")

    print("\n===== Абстрактная фабрика =====")
    for hc in HeroClass.ALL:
        kit = hc.get_starter_kit(catalog)
        print(f"{hc.display_name}: {view.describe(kit.create_weapon())}, {view.describe(kit.create_armor())}")

    print("\n===== Строитель =====")
    hero = Hero.Builder() \
        .set_name("Артур") \
        .set_hero_class(HeroClass.WARRIOR) \
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog)) \
        .set_level(3) \
        .build()
    view.print_hero(hero)

    try:
        Hero.Builder() \
            .set_hero_class(HeroClass.MAGE) \
            .set_starter_kit(HeroClass.MAGE.get_starter_kit(catalog)) \
            .build()
    except ValueError as e:
        print(f"Герой без имени не создается: {e}")

    try:
        Hero.Builder() \
            .set_name("Мерлин") \
            .build()
    except ValueError as e:
        print(f"Герой без класса не создается: {e}")

    print("\n===== Фабричный метод =====")
    forest = Forest(catalog)
    crypt = Crypt(catalog)
    view.print_report(forest.explore(hero, 7), forest.get_display_name())
    print()
    view.print_report(crypt.explore(hero, 7), crypt.get_display_name())

if __name__ == "__main__":
   run_demo()