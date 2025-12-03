def solve_part_1(input_data):
    containers = [int(line.strip()) for line in input_data.strip().split('\n')]
    target = 25 if len(containers) == 5 else 150

    def find_combinations(containers, target, start_index=0):
        if target == 0:
            return [[]]
        if target < 0 or start_index >= len(containers):
            return []

        combinations = []

        remaining_target = target - containers[start_index]
        for combo in find_combinations(containers, remaining_target, start_index + 1):
            combinations.append([containers[start_index]] + combo)

        for combo in find_combinations(containers, target, start_index + 1):
            combinations.append(combo)

        return combinations

    valid_combinations = find_combinations(containers, target)
    return len(valid_combinations)

def solve_part_2(input_data):
    containers = [int(line.strip()) for line in input_data.strip().split('\n')]
    target = 25 if len(containers) == 5 else 150

    def find_combinations(containers, target, start_index=0):
        if target == 0:
            return [[]]
        if target < 0 or start_index >= len(containers):
            return []

        combinations = []

        remaining_target = target - containers[start_index]
        for combo in find_combinations(containers, remaining_target, start_index + 1):
            combinations.append([containers[start_index]] + combo)

        for combo in find_combinations(containers, target, start_index + 1):
            combinations.append(combo)

        return combinations

    valid_combinations = find_combinations(containers, target)

    if not valid_combinations:
        return 0

    min_containers = min(len(combo) for combo in valid_combinations)
    min_combinations = [combo for combo in valid_combinations if len(combo) == min_containers]

    return len(min_combinations)
