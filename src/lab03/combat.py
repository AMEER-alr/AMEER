from dataclasses import dataclass
from enum import Enum

class Side(Enum):
    HERO = "HERO"
    ENEMY = "ENEMY"

class EventType(Enum):
    HIT = "HIT"
    CRITICAL_HIT = "CRITICAL_HIT"
    DEATH = "DEATH"

class Outcome(Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"

@dataclass
class Hit:
    damage: int
    critical: bool

@dataclass
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int

@dataclass
class Participant:
    code: str
    name: str
    max_health: int

    @staticmethod
    def of(combatant):
        return Participant(combatant.get_code(), combatant.get_name(), combatant.get_max_health())

@dataclass
class BattleReport:
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: list

class Combatant:
    def get_code(self) -> str: pass
    def get_name(self) -> str: pass
    def get_health(self) -> int: pass
    def get_max_health(self) -> int: pass
    def is_alive(self) -> bool: pass
    def roll_damage(self) -> Hit: pass
    def receive_hit(self, damage: int) -> int: pass

class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant):
        self.hero = hero
        self.enemy = enemy
        self.events = []
        self.round = 0

    def run(self) -> BattleReport:
        from .core import Dice
        dice = Dice()
        self.round = 0
        while self.hero.is_alive() and self.enemy.is_alive():
            self.round += 1
            self._strike(self.hero, Side.HERO, self.enemy, Side.ENEMY)
            if self.enemy.is_alive():
                self._strike(self.enemy, Side.ENEMY, self.hero, Side.HERO)
                
        outcome = Outcome.VICTORY if self.hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self.hero),
            Participant.of(self.enemy),
            outcome,
            list(self.events)
        )

    def _strike(self, attacker: Combatant, source_side: Side, defender: Combatant, target_side: Side):
        hit = attacker.roll_damage()
        dealt = defender.receive_hit(hit.damage)
        event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self._emit(BattleEvent(self.round, event_type, source_side, target_side, dealt, defender.get_health()))
        
        if not defender.is_alive():
            self._emit(BattleEvent(self.round, EventType.DEATH, source_side, target_side, 0, 0))

    def _emit(self, event: BattleEvent):
        self.events.append(event)