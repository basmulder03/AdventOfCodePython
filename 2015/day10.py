def look_and_say(s):
    result = []
    i = 0
    while i < len(s):
        current_digit = s[i]
        count = 1

        # Count consecutive occurrences of the same digit
        while i + count < len(s) and s[i + count] == current_digit:
            count += 1

        # Add count followed by the digit
        result.append(str(count))
        result.append(current_digit)
        i += count

    return ''.join(result)


def apply_look_and_say(initial_sequence, iterations):
    sequence = initial_sequence.strip()
    for _ in range(iterations):
        sequence = look_and_say(sequence)
    return sequence


def solve_part_1(input_data):
    initial_sequence = input_data.strip()
    result_sequence = apply_look_and_say(initial_sequence, 40)
    return len(result_sequence)


def solve_part_2(input_data):
    initial_sequence = input_data.strip()
    result_sequence = apply_look_and_say(initial_sequence, 50)
    return len(result_sequence)
