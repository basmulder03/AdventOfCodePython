def solve_part_1(input_data):
    """Count matching pairs from generators."""
    lines = input_data.strip().split('\n')
    a = int(lines[0].split()[-1])
    b = int(lines[1].split()[-1])

    matches = 0

    for _ in range(40_000_000):
        a = (a * 16807) % 2147483647
        b = (b * 48271) % 2147483647

        # Compare lower 16 bits
        if a & 0xFFFF == b & 0xFFFF:
            matches += 1

    return matches


def solve_part_2(input_data):
    """Count matching pairs with picky generators."""
    lines = input_data.strip().split('\n')
    a = int(lines[0].split()[-1])
    b = int(lines[1].split()[-1])

    matches = 0

    for _ in range(5_000_000):
        # Generator A - only multiples of 4
        a = (a * 16807) % 2147483647
        while a % 4 != 0:
            a = (a * 16807) % 2147483647

        # Generator B - only multiples of 8
        b = (b * 48271) % 2147483647
        while b % 8 != 0:
            b = (b * 48271) % 2147483647

        # Compare lower 16 bits
        if a & 0xFFFF == b & 0xFFFF:
            matches += 1

    return matches

