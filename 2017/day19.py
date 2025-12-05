def solve_part_1(input_data):
    """Series of tubes - follow the path."""
    lines = input_data.split('\n')  # Don't strip to preserve spaces
    grid = [list(line) for line in lines]

    # Find starting position (top row, vertical bar)
    start_col = None
    for c, char in enumerate(grid[0]):
        if char == '|':
            start_col = c
            break

    # Directions: down, right, up, left
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction = 0  # Start going down

    r, c = 0, start_col
    letters = []

    while True:
        # Check current position for letters
        if grid[r][c].isalpha():
            letters.append(grid[r][c])

        dr, dc = directions[direction]

        # Try to continue in current direction
        nr, nc = r + dr, c + dc

        if (0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and
            grid[nr][nc] not in [' ', '']):
            r, c = nr, nc
        else:
            # Need to turn - find new direction
            found_new_dir = False
            for new_dir in range(4):
                if new_dir == direction or new_dir == (direction + 2) % 4:
                    continue  # Don't go back or continue same direction

                dr, dc = directions[new_dir]
                nr, nc = r + dr, c + dc

                if (0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and
                    grid[nr][nc] not in [' ', '']):
                    direction = new_dir
                    r, c = nr, nc
                    found_new_dir = True
                    break

            if not found_new_dir:
                break

    return ''.join(letters)


def solve_part_2(input_data):
    """Series of tubes - count steps."""
    lines = input_data.split('\n')  # Don't strip to preserve spaces
    grid = [list(line) for line in lines]

    # Find starting position
    start_col = None
    for c, char in enumerate(grid[0]):
        if char == '|':
            start_col = c
            break

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction = 0

    r, c = 0, start_col
    steps = 1  # Start with 1 since we're already on the starting position

    while True:
        dr, dc = directions[direction]

        # Try to continue in current direction
        nr, nc = r + dr, c + dc

        if (0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and
            grid[nr][nc] not in [' ', '']):
            r, c = nr, nc
            steps += 1
        else:
            # Need to turn - find new direction
            found_new_dir = False
            for new_dir in range(4):
                if new_dir == direction or new_dir == (direction + 2) % 4:
                    continue

                dr, dc = directions[new_dir]
                nr, nc = r + dr, c + dc

                if (0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and
                    grid[nr][nc] not in [' ', '']):
                    direction = new_dir
                    r, c = nr, nc
                    steps += 1
                    found_new_dir = True
                    break

            if not found_new_dir:
                break

    return steps

