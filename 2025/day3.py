def solve_part_1(input_data):
    total = 0
    for line in input_data.strip().split('\n'):
        max_joltage = 0
        for i in range(len(line)):
            for j in range(i + 1, len(line)):
                joltage = int(line[i] + line[j])
                max_joltage = max(max_joltage, joltage)
        total += max_joltage
    return total

def solve_part_2(input_data):
    total = 0
    for line in input_data.strip().split('\n'):
        n = len(line)
        batteries_to_select = 12
        batteries_to_skip = n - batteries_to_select

        selected = []
        skip_count = 0

        for i in range(n):
            remaining = n - i
            needed = batteries_to_select - len(selected)

            can_skip = (remaining - 1) >= needed

            if can_skip and skip_count < batteries_to_skip:
                window_end = i + (batteries_to_skip - skip_count) + 1
                best_in_window = max(line[i:window_end])

                if line[i] < best_in_window:
                    skip_count += 1
                    continue

            selected.append(line[i])
            if len(selected) == batteries_to_select:
                break

        max_joltage = int(''.join(selected))
        total += max_joltage

    return total