def solve_part_1(input_data):
    lines = [line for line in input_data.split("\n") if line.strip()]
    if not lines:
        return 0
    m, n = len(lines), len(lines[0])
    ans = 0

    # Pre-compute all symbol positions for faster lookup
    symbols = set()
    for i in range(m):
        for j in range(n):
            c = lines[i][j]
            if not c.isdigit() and c != '.':
                symbols.add((i, j))

    def has_adjacent_symbol(row, start_col, end_col):
        """Check if number at row[start_col:end_col] has adjacent symbol"""
        for r in range(max(0, row-1), min(m, row+2)):
            for c in range(max(0, start_col-1), min(n, end_col+1)):
                if (r, c) in symbols:
                    return True
        return False

    for x, line in enumerate(lines):
        left = -1
        for idx, c in enumerate(line):
            if c.isdigit():
                if left == -1:
                    left = idx
            elif left != -1:  # End of number
                if has_adjacent_symbol(x, left, idx):
                    ans += int(line[left:idx])
                left = -1

        # Handle number at end of line
        if left != -1 and has_adjacent_symbol(x, left, len(line)):
            ans += int(line[left:])

    return ans
                                
def solve_part_2(input_data):
    from collections import defaultdict

    lines = [line for line in input_data.split("\n") if line.strip()]
    if not lines:
        return 0
    m, n = len(lines), len(lines[0])
    gear_adjacent = defaultdict(list)

    def find_adjacent_gears(row, start_col, end_col):
        """Find all gears adjacent to number at row[start_col:end_col]"""
        gears = set()
        for r in range(max(0, row-1), min(m, row+2)):
            for c in range(max(0, start_col-1), min(n, end_col+1)):
                if lines[r][c] == '*':
                    gears.add((r, c))
        return gears

    # Find all numbers and their adjacent gears
    for x, line in enumerate(lines):
        left = -1
        for idx, c in enumerate(line):
            if c.isdigit():
                if left == -1:
                    left = idx
            elif left != -1:  # End of number
                nr = int(line[left:idx])
                for gear_pos in find_adjacent_gears(x, left, idx):
                    gear_adjacent[gear_pos].append(nr)
                left = -1

        # Handle number at end of line
        if left != -1:
            nr = int(line[left:])
            for gear_pos in find_adjacent_gears(x, left, len(line)):
                gear_adjacent[gear_pos].append(nr)

    # Calculate answer
    return sum(nums[0] * nums[1] for nums in gear_adjacent.values() if len(nums) == 2)
