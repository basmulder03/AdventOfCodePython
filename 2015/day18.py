def solve_part_1(input_data):
    lines = input_data.strip().split('\n')

    # Use a set to track lit lights
    lights = set()
    rows = len(lines)
    cols = len(lines[0])

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                lights.add((r, c))

    for _ in range(100):
        new_lights = set()

        # Check all cells that might change
        cells_to_check = set()
        for r, c in lights:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cells_to_check.add((nr, nc))

        for r, c in cells_to_check:
            neighbors_on = sum(
                1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                if not (dr == 0 and dc == 0) and (r + dr, c + dc) in lights
            )

            if (r, c) in lights:
                if neighbors_on == 2 or neighbors_on == 3:
                    new_lights.add((r, c))
            else:
                if neighbors_on == 3:
                    new_lights.add((r, c))

        lights = new_lights

    return len(lights)


def solve_part_2(input_data):
    lines = input_data.strip().split('\n')

    # Use a set to track lit lights
    lights = set()
    rows = len(lines)
    cols = len(lines[0])

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                lights.add((r, c))

    # Corners are always on
    corners = {(0, 0), (0, cols-1), (rows-1, 0), (rows-1, cols-1)}
    lights.update(corners)

    for _ in range(100):
        new_lights = set()

        # Check all cells that might change
        cells_to_check = set()
        for r, c in lights:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cells_to_check.add((nr, nc))

        for r, c in cells_to_check:
            # Corners are always on
            if (r, c) in corners:
                new_lights.add((r, c))
                continue

            neighbors_on = sum(
                1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                if not (dr == 0 and dc == 0) and (r + dr, c + dc) in lights
            )

            if (r, c) in lights:
                if neighbors_on == 2 or neighbors_on == 3:
                    new_lights.add((r, c))
            else:
                if neighbors_on == 3:
                    new_lights.add((r, c))

        lights = new_lights

    return len(lights)

