def solve_part_1(input_data):
    """Spinlock - find value after 2017."""
    steps = int(input_data.strip())
    buffer = [0]
    pos = 0

    for i in range(1, 2018):
        pos = (pos + steps) % len(buffer) + 1
        buffer.insert(pos, i)

    # Find position of 2017 and return next value
    idx_2017 = buffer.index(2017)
    return buffer[(idx_2017 + 1) % len(buffer)]


def solve_part_2(input_data):
    """Spinlock - find value after 0 after 50 million insertions."""
    steps = int(input_data.strip())

    # We only need to track what's at position 1 (after 0)
    # 0 always stays at position 0
    pos = 0
    value_after_zero = None

    for i in range(1, 50_000_001):
        pos = (pos + steps) % i + 1
        # If we insert at position 1, it becomes the value after 0
        if pos == 1:
            value_after_zero = i

    return value_after_zero
