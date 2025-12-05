def solve_part_1(input_data):
    """Redistribute memory blocks until cycle detected."""
    banks = list(map(int, input_data.strip().split()))
    seen = set()
    cycles = 0

    while tuple(banks) not in seen:
        seen.add(tuple(banks))

        # Find bank with most blocks
        max_blocks = max(banks)
        max_idx = banks.index(max_blocks)

        # Redistribute
        banks[max_idx] = 0
        pos = max_idx
        for _ in range(max_blocks):
            pos = (pos + 1) % len(banks)
            banks[pos] += 1

        cycles += 1

    return cycles


def solve_part_2(input_data):
    """Find size of the loop in memory redistribution."""
    banks = list(map(int, input_data.strip().split()))
    seen = {}
    cycles = 0

    while tuple(banks) not in seen:
        seen[tuple(banks)] = cycles

        # Find bank with most blocks
        max_blocks = max(banks)
        max_idx = banks.index(max_blocks)

        # Redistribute
        banks[max_idx] = 0
        pos = max_idx
        for _ in range(max_blocks):
            pos = (pos + 1) % len(banks)
            banks[pos] += 1

        cycles += 1

    return cycles - seen[tuple(banks)]

