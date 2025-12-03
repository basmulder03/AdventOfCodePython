def solve_part_1(input_data):
    digits = input_data.strip()
    total = 0
    for i in range(len(digits)):
        next_i = (i + 1) % len(digits)
        if digits[i] == digits[next_i]:
            total += int(digits[i])
    return total


def solve_part_2(input_data):
    digits = input_data.strip()
    total = 0
    step = len(digits) // 2
    for i in range(len(digits)):
        next_i = (i + step) % len(digits)
        if digits[i] == digits[next_i]:
            total += int(digits[i])
    return total

