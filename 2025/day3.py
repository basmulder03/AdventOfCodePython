def solve_part_1(input_data):
    total = 0
    for raw_line in input_data.strip().splitlines():
        line = raw_line.strip()
        if len(line) < 2:
            continue

        max_joltage = 0
        best_suffix = line[-1]
        for digit in reversed(line[:-1]):
            max_joltage = max(max_joltage, int(digit + best_suffix))
            if digit > best_suffix:
                best_suffix = digit

        total += max_joltage
    return total


def solve_part_2(input_data):
    total = 0
    for raw_line in input_data.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue

        batteries_to_select = 12
        if len(line) <= batteries_to_select:
            total += int(line)
            continue

        to_remove = len(line) - batteries_to_select
        stack = []
        for digit in line:
            while to_remove and stack and stack[-1] < digit:
                stack.pop()
                to_remove -= 1
            stack.append(digit)

        if to_remove:
            stack = stack[:-to_remove]

        selected = stack[:batteries_to_select]
        total += int(''.join(selected))

    return total