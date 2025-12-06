from typing import Any


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')

    max_len = max(len(line) for line in lines)

    grand_total = 0
    col = 0

    while col < max_len:
        col_chars = []
        for line in lines:
            if col < len(line):
                col_chars.append(line[col])
            else:
                col_chars.append(' ')

        if all(c == ' ' for c in col_chars):
            col += 1
            continue

        nums = []
        op = None
        start_col = col

        while col < max_len:
            col_chars = []
            for line in lines:
                if col < len(line):
                    col_chars.append(line[col])
                else:
                    col_chars.append(' ')

            if all(c == ' ' for c in col_chars):
                break
            col += 1

        for line_idx, line in enumerate(lines):
            text = line[start_col:col].strip()
            if line_idx < len(lines) - 1:
                if text:
                    nums.append(int(text))
            else:
                op = text

        if nums and op:
            result = nums[0]
            for i in range(1, len(nums)):
                if op == '+':
                    result += nums[i]
                else:
                    result *= nums[i]
            grand_total += result

    return grand_total


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')
    max_len = max(len(line) for line in lines)

    for i in range(len(lines)):
        lines[i] = lines[i].ljust(max_len)

    grand_total = 0
    col = max_len - 1

    while col >= 0:
        col_chars = [lines[row][col] for row in range(len(lines))]

        if all(c == ' ' for c in col_chars):
            col -= 1
            continue

        end_col = col

        while col >= 0:
            col_chars = [lines[row][col] for row in range(len(lines))]
            if all(c == ' ' for c in col_chars):
                break
            col -= 1

        start_col = col + 1

        nums = []
        op = None

        for c in range(end_col, start_col - 1, -1):
            digit_str = ""
            for row_idx in range(len(lines) - 1):
                ch = lines[row_idx][c]
                if ch != ' ':
                    digit_str += ch

            if digit_str:
                nums.append(int(digit_str))

        for c in range(start_col, end_col + 1):
            ch = lines[-1][c]
            if ch in ['+', '*']:
                op = ch
                break

        if nums and op:
            result = nums[0]
            for i in range(1, len(nums)):
                if op == '+':
                    result += nums[i]
                else:
                    result *= nums[i]
            grand_total += result

    return grand_total
