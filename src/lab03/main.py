from .item import DefaultCatalog
from .world import Forest, Crypt, DragonLair, LocationRegistry
from .camp import Merchant
from .hero import Hero, HeroClass
from .view import ConsoleView

def read_choice(count: int) -> int:
    try:
        choice = int(input().strip())
        if 1 <= choice <= count:
            return choice - 1
    except ValueError:
        pass
    return -1

def go_on_expedition(hero, locations, view):
    all_locs = locations.get_all()
    print("Куда отправимся?")
    for i, loc in enumerate(all_locs):
        print(f"{i + 1} - {loc.get_display_name()} (рекомендуемый уровень {loc.get_recommended_level()})")
    index = read_choice(len(all_locs))
    if index < 0:
        return

    location = all_locs[index]
    report = location.explore(hero)
    print()
    view.print_report(report, location.get_display_name())

    if report.battle.outcome.value == "VICTORY" and location.get_code() == "dragon-lair":
        print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero.get_name()}.")

def manage_equipment(hero, view):
    inventory = hero.get_inventory()
    if not inventory:
        print("Инвентарь пуст")
        return

    print("Что экипировать? (0 - назад)")
    print_items(inventory, view)
    index = read_choice(len(inventory))
    if index < 0:
        return

    item = inventory[index]
    hero.equip(item)
    print("Экипировано: " + view.describe(item))

def visit_merchant(hero, merchant, view):
    print(f"Торговец: \"Чего желаешь?\" (золото: {hero.get_gold()})")
    print("1 - купить, 2 - продать, 0 - назад")
    choice = input().strip()
    if choice == "1":
        buy(hero, merchant, view)
    elif choice == "2":
        sell(hero, merchant, view)

def buy(hero, merchant, view):
    showcase = merchant.get_showcase()
    for i, item in enumerate(showcase):
        print(f"{i + 1} - {view.describe(item)}: {item.get_price()} золота")
    index = read_choice(len(showcase))
    if index < 0:
        return

    try:
        item = merchant.buy(hero, showcase[index].get_code())
        print("Куплено: " + view.describe(item))
    except ValueError as e:
        print(e)

def sell(hero, merchant, view):
    inventory = hero.get_inventory()
    if not inventory:
        print("Продавать нечего (экипированные предметы продать нельзя)")
        return

    for i, item in enumerate(inventory):
        print(f"{i + 1} - {view.describe(item)}: {merchant.get_sell_price(item)} золота")
    index = read_choice(len(inventory))
    if index < 0:
        return

    item = inventory[index]
    price = merchant.sell(hero, item)
    print(f"Продано: {item.get_name()} за {price} золота")

def print_items(items, view):
    for i, item in enumerate(items):
        print(f"{i + 1} - {view.describe(item)}")

def create_hero(catalog, view) -> Hero:
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        for i, hc in enumerate(HeroClass.ALL):
            kit = hc.get_starter_kit(catalog)
            print(f"{i + 1} - {hc.display_name} (здоровье {hc.base_health}): {view.describe(kit.create_weapon())}, {view.describe(kit.create_armor())}")
        class_index = read_choice(len(HeroClass.ALL))
        if class_index < 0:
            continue

        hero_class = HeroClass.ALL[class_index]
        print("Введите имя:")
        name = input().strip()
        try:
            return Hero.Builder() \
                .set_name(name) \
                .set_hero_class(hero_class) \
                .set_starter_kit(hero_class.get_starter_kit(catalog)) \
                .build()
        except ValueError as e:
            print("Не получилось создать героя: " + str(e))

def main():
    catalog = DefaultCatalog.create()
    locations = LocationRegistry([
        Forest(catalog),
        Crypt(catalog),
        DragonLair(catalog)
    ])
    merchant = Merchant(catalog, [
        DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW, DefaultCatalog.EMBER_STAFF,
        DefaultCatalog.CHAINMAIL, DefaultCatalog.PLATE_ARMOR
    ])

    view = ConsoleView()
    hero = create_hero(catalog, view)
    print(f"{hero.get_name()} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        view.print_hero(hero)
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 0 - выйти из игры")
        choice = input().strip()

        if choice == "1":
            go_on_expedition(hero, locations, view)
        elif choice == "2":
            manage_equipment(hero, view)
        elif choice == "3":
            visit_merchant(hero, merchant, view)
        elif choice == "0":
            return
        else:
            print("Такого варианта нет")

if __name__ == "__main__":
    main()