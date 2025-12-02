def is_invalid_id(num):
    s = str(num)
    length = len(s)

    # Must have even length to be repeated twice
    if length % 2 != 0:
        return False

    half = length // 2
    first_half = s[:half]
    second_half = s[half:]

    return first_half == second_half

def solve_part_1(input_data):
    ids = input_data.strip().split(",")
    invalid_ids = []

    for range_str in ids:
        start, end = map(int, range_str.split("-"))
        for num in range(start, end + 1):
            if is_invalid_id(num):
                invalid_ids.append(num)

    return sum(invalid_ids)


def is_invalid_id_part2(num):
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths (from 1 to length//2)
    # Pattern must repeat at least twice, so max pattern length is length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if the length is divisible by the pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if repeating this pattern gives us the full number
            if pattern * (length // pattern_len) == s:
                return True
    return False

def solve_part_2(input_data):
    ids = input_data.strip().split(",")
    invalid_ids = []

    for range_str in ids:
        start, end = map(int, range_str.split("-"))
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                invalid_ids.append(num)

    return sum(invalid_ids)