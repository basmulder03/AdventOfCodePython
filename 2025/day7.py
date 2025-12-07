from typing import Any
from collections import deque


def solve_part_1(input_data: str) -> Any:
    lines = input_data.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    splits = 0
    queue = deque([(start_row, start_col)])
    visited = set()

    while queue:
        row, col = queue.popleft()

        row += 1

        if row >= rows or col < 0 or col >= cols:
            continue

        if (row, col) in visited:
            continue

        visited.add((row, col))

        if grid[row][col] == '^':
            splits += 1
            queue.append((row, col - 1))
            queue.append((row, col + 1))
        else:
            queue.append((row, col))

    return splits


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    memo = {}

    def count_timelines(row, col):
        """Count how many timelines exist from this position."""
        if row >= rows or col < 0 or col >= cols:
            return 1

        if (row, col) in memo:
            return memo[(row, col)]

        result = 0

        if grid[row][col] == '^':
            result = count_timelines(row + 1, col - 1) + count_timelines(row + 1, col + 1)
        else:
            result = count_timelines(row + 1, col)

        memo[(row, col)] = result
        return result

    return count_timelines(start_row, start_col)
