def solve_part_1(input_data):
    """Follow jump instructions to escape maze."""
    instructions = list(map(int, input_data.strip().split('\n')))
    pos = 0
    steps = 0

    while 0 <= pos < len(instructions):
        jump = instructions[pos]
        instructions[pos] += 1
        pos += jump
        steps += 1

    return steps


def solve_part_2(input_data):
    """Follow jump instructions with different increment rule."""
    instructions = list(map(int, input_data.strip().split('\n')))
    pos = 0
    steps = 0

    while 0 <= pos < len(instructions):
        jump = instructions[pos]
        if jump >= 3:
            instructions[pos] -= 1
        else:
            instructions[pos] += 1
        pos += jump
        steps += 1

    return steps
