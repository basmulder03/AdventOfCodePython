from typing import Any
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class GameState:
    player_hp: int
    player_mana: int
    boss_hp: int
    boss_damage: int
    shield_timer: int = 0
    poison_timer: int = 0
    recharge_timer: int = 0
    mana_spent: int = 0
    hard_mode: bool = False


class Spell:
    def __init__(self, name: str, cost: int, damage: int = 0, heal: int = 0,
                 effect_type: str = None, effect_duration: int = 0):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.heal = heal
        self.effect_type = effect_type
        self.effect_duration = effect_duration


# Define all spells
SPELLS = [
    Spell("Magic Missile", 53, damage=4),
    Spell("Drain", 73, damage=2, heal=2),
    Spell("Shield", 113, effect_type="shield", effect_duration=6),
    Spell("Poison", 173, effect_type="poison", effect_duration=6),
    Spell("Recharge", 229, effect_type="recharge", effect_duration=5),
]


# Removed unused helper functions - logic is now inline in the recursive function


@lru_cache(maxsize=None)
def min_mana_recursive(player_hp: int, player_mana: int, boss_hp: int,
                      shield_timer: int, poison_timer: int, recharge_timer: int,
                      boss_damage: int, hard_mode: bool, player_turn: bool) -> int:
    """Recursive function to find minimum mana with memoization."""

    # Hard mode: player loses 1 HP at start of player turn
    if hard_mode and player_turn:
        player_hp -= 1
        if player_hp <= 0:
            return 999999

    # Apply effects at start of turn
    armor = 7 if shield_timer > 0 else 0

    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1

    if recharge_timer > 0:
        player_mana += 101
        recharge_timer -= 1

    if shield_timer > 0:
        shield_timer -= 1

    # Check if boss is dead after effects
    if boss_hp <= 0:
        return 0

    if player_turn:
        # Player's turn - try each spell
        min_cost = 999999

        for spell in SPELLS:
            # Check if we can cast this spell
            if player_mana < spell.cost:
                continue

            # Check if effect is already active
            if (spell.effect_type == "shield" and shield_timer > 0) or \
               (spell.effect_type == "poison" and poison_timer > 0) or \
               (spell.effect_type == "recharge" and recharge_timer > 0):
                continue

            # Apply spell effects
            new_player_hp = player_hp + spell.heal
            new_player_mana = player_mana - spell.cost
            new_boss_hp = boss_hp - spell.damage
            new_shield_timer = shield_timer
            new_poison_timer = poison_timer
            new_recharge_timer = recharge_timer

            # Start effect timers
            if spell.effect_type == "shield":
                new_shield_timer = spell.effect_duration
            elif spell.effect_type == "poison":
                new_poison_timer = spell.effect_duration
            elif spell.effect_type == "recharge":
                new_recharge_timer = spell.effect_duration

            # Check if boss dies immediately from spell
            if new_boss_hp <= 0:
                min_cost = min(min_cost, spell.cost)
            else:
                # Continue to boss turn
                cost = min_mana_recursive(
                    new_player_hp, new_player_mana, new_boss_hp,
                    new_shield_timer, new_poison_timer, new_recharge_timer,
                    boss_damage, hard_mode, False
                )
                if cost != 999999:
                    min_cost = min(min_cost, spell.cost + cost)

        return min_cost

    else:
        # Boss's turn
        damage = max(1, boss_damage - armor)
        new_player_hp = player_hp - damage

        if new_player_hp <= 0:
            return 999999

        # Continue to player turn
        return min_mana_recursive(
            new_player_hp, player_mana, boss_hp,
            shield_timer, poison_timer, recharge_timer,
            boss_damage, hard_mode, True
        )


def find_min_mana_to_win(boss_hp: int, boss_damage: int, hard_mode: bool = False) -> int:
    """Find minimum mana needed to win using optimized recursive search."""
    result = min_mana_recursive(
        50, 500, boss_hp, 0, 0, 0, boss_damage, hard_mode, True
    )
    return result if result != 999999 else -1


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')
    boss_hp = int(lines[0].split(': ')[1])
    boss_damage = int(lines[1].split(': ')[1])

    return find_min_mana_to_win(boss_hp, boss_damage, hard_mode=False)


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')
    boss_hp = int(lines[0].split(': ')[1])
    boss_damage = int(lines[1].split(': ')[1])

    return find_min_mana_to_win(boss_hp, boss_damage, hard_mode=True)
