class ConsoleView:
    def describe(self, item) -> str:
        if item is None:
            return "ничего"
        description = item.get_name()
        enchants = item.get_enchantments()
        if enchants:
            names = ", ".join([enc.name for enc in enchants])
            description += f" [{names}]"
        return f"{description} ({item.get_description()})"

    def print_hero(self, hero):
        print(f"{hero.get_name()}, {hero.get_hero_class().display_name} {hero.get_level()} ур. | "
              f"здоровье {hero.get_max_health()} | опыт {hero.get_experience()}/{hero.get_experience_to_next_level()} | "
              f"золото {hero.get_gold()}")
        print("  Оружие: " + self.describe(hero.get_weapon()))
        print("  Броня:  " + self.describe(hero.get_armor()))

    def print_report(self, report, location_name: str):
        battle = report.battle
        print(f"=== {location_name} (сид {report.seed}) ===")
        print(f"{battle.hero.name} встречает врага: {battle.enemy.name} ({battle.enemy.max_health} здоровья)")

        for event in battle.events:
            self._print_event(event, battle)

        self._print_rewards(battle, report.rewards)

    def _print_event(self, event, battle):
        source = battle.hero if event.source.value == "HERO" else battle.enemy
        target = battle.hero if event.target.value == "HERO" else battle.enemy

        if event.type.value == "HIT":
            print(f"[раунд {event.round}] {source.name} -> {target.name}: {event.amount} урона, осталось {event.target_health_after}/{target.max_health}")
        elif event.type.value == "CRITICAL_HIT":
            print(f"[раунд {event.round}] {source.name} -> {target.name}: КРИТ! {event.amount} урона, осталось {event.target_health_after}/{target.max_health}")
        elif event.type.value == "DEATH":
            print(f"{target.name} повержен!")

    def _print_rewards(self, battle, rewards):
        if battle.outcome.value == "DEFEAT":
            print(f"Поражение... {battle.hero.name} едва уносит ноги и теряет {-rewards.gold} золота")
            return

        print(f"Победа! +{rewards.experience} опыта, +{rewards.gold} золота")
        if rewards.loot:
            print(f"Добыча: {self.describe(rewards.loot)}")
        if rewards.levels_gained > 0:
            print("Новый уровень!")