def solve_part_1(input_data):
    """Calculate score of stream processing."""
    stream = input_data.strip()
    score = 0
    depth = 0
    in_garbage = False
    i = 0

    while i < len(stream):
        char = stream[i]

        if in_garbage:
            if char == '!':
                i += 1  # Skip next character
            elif char == '>':
                in_garbage = False
        else:
            if char == '<':
                in_garbage = True
            elif char == '{':
                depth += 1
            elif char == '}':
                score += depth
                depth -= 1

        i += 1

    return score


def solve_part_2(input_data):
    """Count non-canceled garbage characters."""
    stream = input_data.strip()
    garbage_count = 0
    in_garbage = False
    i = 0

    while i < len(stream):
        char = stream[i]

        if in_garbage:
            if char == '!':
                i += 1  # Skip next character
            elif char == '>':
                in_garbage = False
            else:
                garbage_count += 1
        else:
            if char == '<':
                in_garbage = True

        i += 1

    return garbage_count
