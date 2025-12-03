def solve_part_1(input_data):
    lines = input_data.strip().split('\n')

    grid = []
    for line in lines:
        grid.append(list(line))

    rows, cols = len(grid), len(grid[0])

    for step in range(100):
        new_grid = [['.'] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                neighbors_on = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '#':
                            neighbors_on += 1

                if grid[r][c] == '#':
                    if neighbors_on == 2 or neighbors_on == 3:
                        new_grid[r][c] = '#'
                    else:
                        new_grid[r][c] = '.'
                else:
                    if neighbors_on == 3:
                        new_grid[r][c] = '#'
                    else:
                        new_grid[r][c] = '.'

        grid = new_grid

    count = 0
    for row in grid:
        for cell in row:
            if cell == '#':
                count += 1

    return count

def solve_part_2(input_data):
    lines = input_data.strip().split('\n')

    grid = []
    for line in lines:
        grid.append(list(line))

    rows, cols = len(grid), len(grid[0])

    grid[0][0] = '#'
    grid[0][cols-1] = '#'
    grid[rows-1][0] = '#'
    grid[rows-1][cols-1] = '#'

    for step in range(100):
        new_grid = [['.'] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                neighbors_on = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '#':
                            neighbors_on += 1

                if grid[r][c] == '#':
                    if neighbors_on == 2 or neighbors_on == 3:
                        new_grid[r][c] = '#'
                    else:
                        new_grid[r][c] = '.'
                else:
                    if neighbors_on == 3:
                        new_grid[r][c] = '#'
                    else:
                        new_grid[r][c] = '.'

        grid = new_grid

        grid[0][0] = '#'
        grid[0][cols-1] = '#'
        grid[rows-1][0] = '#'
        grid[rows-1][cols-1] = '#'

    count = 0
    for row in grid:
        for cell in row:
            if cell == '#':
                count += 1

    return count
