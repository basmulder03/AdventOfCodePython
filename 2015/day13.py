from itertools import permutations
import re

def parse_happiness_data(input_data):
    happiness = {}
    people = set()

    for line in input_data.strip().split('\n'):
        # Parse lines like: "Alice would gain 54 happiness units by sitting next to Bob."
        match = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.', line)
        if match:
            person1, gain_lose, amount, person2 = match.groups()
            amount = int(amount)
            if gain_lose == 'lose':
                amount = -amount

            happiness[(person1, person2)] = amount
            people.add(person1)
            people.add(person2)

    return happiness, list(people)

def calculate_total_happiness(arrangement, happiness):
    total = 0
    n = len(arrangement)

    for i in range(n):
        person = arrangement[i]
        left_neighbor = arrangement[(i - 1) % n]
        right_neighbor = arrangement[(i + 1) % n]

        # Add happiness from sitting next to left and right neighbors
        total += happiness.get((person, left_neighbor), 0)
        total += happiness.get((person, right_neighbor), 0)

    return total

def find_optimal_seating(people, happiness):
    max_happiness = float('-inf')
    best_arrangement = None

    # Since the table is circular, we can fix one person's position to avoid counting
    # rotations as different arrangements
    fixed_person = people[0]
    other_people = people[1:]

    # Try all permutations of the other people
    for perm in permutations(other_people):
        arrangement = [fixed_person] + list(perm)
        total_happiness = calculate_total_happiness(arrangement, happiness)

        if total_happiness > max_happiness:
            max_happiness = total_happiness
            best_arrangement = arrangement

    return max_happiness, best_arrangement

def solve_part_1(input_data):
    happiness, people = parse_happiness_data(input_data)
    max_happiness, _ = find_optimal_seating(people, happiness)
    return max_happiness

def solve_part_2(input_data):
    happiness, people = parse_happiness_data(input_data)

    # Add myself to the list with 0 happiness relationships
    me = "Me"
    people.append(me)

    # Add happiness relationships between me and everyone else (all 0)
    for person in people[:-1]:  # Exclude myself from the loop
        happiness[(me, person)] = 0
        happiness[(person, me)] = 0

    max_happiness, _ = find_optimal_seating(people, happiness)
    return max_happiness
