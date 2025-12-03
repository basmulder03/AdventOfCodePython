from typing import Any


def solve_part_1(input_data: str) -> Any:
    instructions = input_data.strip().split(', ')

    x, y = 0, 0
    direction = 0

    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    for instruction in instructions:
        turn = instruction[0]
        steps = int(instruction[1:])

        if turn == 'L':
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4

        x += dx[direction] * steps
        y += dy[direction] * steps

    return abs(x) + abs(y)


def solve_part_2(input_data: str) -> Any:
    instructions = input_data.strip().split(', ')

    x, y = 0, 0
    direction = 0

    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    visited = {(0, 0)}

    for instruction in instructions:
        turn = instruction[0]
        steps = int(instruction[1:])

        if turn == 'L':
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4

        for _ in range(steps):
            x += dx[direction]
            y += dy[direction]

            if (x, y) in visited:
                return abs(x) + abs(y)

            visited.add((x, y))

    return None
