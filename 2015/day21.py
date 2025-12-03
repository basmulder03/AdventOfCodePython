from typing import Any
from itertools import combinations


def parse_boss_stats(input_data: str) -> tuple[int, int, int]:
    lines = input_data.strip().split('\n')
    hit_points = int(lines[0].split(': ')[1])
    damage = int(lines[1].split(': ')[1])
    armor = int(lines[2].split(': ')[1])
    return hit_points, damage, armor


def simulate_combat(player_hp: int, player_damage: int, player_armor: int,
                   boss_hp: int, boss_damage: int, boss_armor: int) -> bool:
    player_current_hp = player_hp
    boss_current_hp = boss_hp

    while True:
        damage_dealt = max(1, player_damage - boss_armor)
        boss_current_hp -= damage_dealt

        if boss_current_hp <= 0:
            return True

        damage_dealt = max(1, boss_damage - player_armor)
        player_current_hp -= damage_dealt

        if player_current_hp <= 0:
            return False


def get_all_equipment_combinations():
    weapons = [
        ("Dagger", 8, 4, 0),
        ("Shortsword", 10, 5, 0),
        ("Warhammer", 25, 6, 0),
        ("Longsword", 40, 7, 0),
        ("Greataxe", 74, 8, 0)
    ]

    armor = [
        ("None", 0, 0, 0),
        ("Leather", 13, 0, 1),
        ("Chainmail", 31, 0, 2),
        ("Splintmail", 53, 0, 3),
        ("Bandedmail", 75, 0, 4),
        ("Platemail", 102, 0, 5)
    ]

    rings = [
        ("None1", 0, 0, 0),
        ("None2", 0, 0, 0),
        ("Damage +1", 25, 1, 0),
        ("Damage +2", 50, 2, 0),
        ("Damage +3", 100, 3, 0),
        ("Defense +1", 20, 0, 1),
        ("Defense +2", 40, 0, 2),
        ("Defense +3", 80, 0, 3)
    ]

    combinations_list = []

    for weapon in weapons:
        for armor_item in armor:
            total_cost = weapon[1] + armor_item[1]
            total_damage = weapon[2] + armor_item[2]
            total_armor = weapon[3] + armor_item[3]
            combinations_list.append((total_cost, total_damage, total_armor))

            for ring in rings[2:]:
                total_cost = weapon[1] + armor_item[1] + ring[1]
                total_damage = weapon[2] + armor_item[2] + ring[2]
                total_armor = weapon[3] + armor_item[3] + ring[3]
                combinations_list.append((total_cost, total_damage, total_armor))

            for ring1, ring2 in combinations(rings[2:], 2):  # Skip None placeholders
                total_cost = weapon[1] + armor_item[1] + ring1[1] + ring2[1]
                total_damage = weapon[2] + armor_item[2] + ring1[2] + ring2[2]
                total_armor = weapon[3] + armor_item[3] + ring1[3] + ring2[3]
                combinations_list.append((total_cost, total_damage, total_armor))

    return combinations_list


def solve_part_1(input_data: str) -> Any:
    boss_hp, boss_damage, boss_armor = parse_boss_stats(input_data)
    player_hp = 100

    min_cost = float('inf')

    for cost, damage, armor in get_all_equipment_combinations():
        if simulate_combat(player_hp, damage, armor, boss_hp, boss_damage, boss_armor):
            min_cost = min(min_cost, cost)

    return min_cost


def solve_part_2(input_data: str) -> Any:
    boss_hp, boss_damage, boss_armor = parse_boss_stats(input_data)
    player_hp = 100

    max_cost = 0

    for cost, damage, armor in get_all_equipment_combinations():
        if not simulate_combat(player_hp, damage, armor, boss_hp, boss_damage, boss_armor):
            max_cost = max(max_cost, cost)

    return max_cost
