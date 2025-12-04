def solve_part_1(input_data):
    target = int(input_data.strip())

    # Better upper bound - the answer is typically around target // 36 to target // 40
    max_house = target // 10

    presents = [0] * (max_house + 1)

    # Sieve approach: each elf delivers to houses that are multiples
    for elf in range(1, max_house + 1):
        for house in range(elf, max_house + 1, elf):
            presents[house] += elf * 10

    # Find first house with enough presents
    for house in range(1, max_house + 1):
        if presents[house] >= target:
            return house

    return None


def solve_part_2(input_data):
    target = int(input_data.strip())

    max_house = target // 10

    presents = [0] * (max_house + 1)

    # Each elf visits only 50 houses
    for elf in range(1, max_house + 1):
        for house in range(elf, min(elf * 50 + 1, max_house + 1), elf):
            presents[house] += elf * 11

    # Find first house with enough presents
    for house in range(1, max_house + 1):
        if presents[house] >= target:
            return house

    return None
