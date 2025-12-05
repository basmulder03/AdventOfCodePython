def solve_part_1(input_data):
    """Sporifica virus - count infections after 10,000 bursts."""
    lines = input_data.strip().split('\n')
    grid = {}

    # Parse initial grid
    start_r = len(lines) // 2
    start_c = len(lines[0]) // 2

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                grid[(r - start_r, c - start_c)] = '#'

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction = 0  # Start facing up
    r, c = 0, 0
    infections = 0

    for _ in range(10000):
        if (r, c) in grid and grid[(r, c)] == '#':
            # Turn right, clean node
            direction = (direction + 1) % 4
            del grid[(r, c)]
        else:
            # Turn left, infect node
            direction = (direction - 1) % 4
            grid[(r, c)] = '#'
            infections += 1

        # Move forward
        dr, dc = directions[direction]
        r, c = r + dr, c + dc

    return infections


def solve_part_2(input_data):
    """Evolved virus - count infections after 10,000,000 bursts."""
    lines = input_data.strip().split('\n')
    grid = {}

    # Parse initial grid
    start_r = len(lines) // 2
    start_c = len(lines[0]) // 2

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                grid[(r - start_r, c - start_c)] = 'infected'

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction = 0  # Start facing up
    r, c = 0, 0
    infections = 0

    for _ in range(10000000):
        state = grid.get((r, c), 'clean')

        if state == 'clean':
            # Turn left, weaken
            direction = (direction - 1) % 4
            grid[(r, c)] = 'weakened'
        elif state == 'weakened':
            # Don't turn, infect
            grid[(r, c)] = 'infected'
            infections += 1
        elif state == 'infected':
            # Turn right, flag
            direction = (direction + 1) % 4
            grid[(r, c)] = 'flagged'
        elif state == 'flagged':
            # Turn around, clean
            direction = (direction + 2) % 4
            del grid[(r, c)]

        # Move forward
        dr, dc = directions[direction]
        r, c = r + dr, c + dc

    return infections

