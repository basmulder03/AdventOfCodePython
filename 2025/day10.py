from typing import Any
import re
from itertools import combinations
import pulp


def parse_machine(line: str):
    pattern = r'\[([.#]+)\]\s+((?:\([0-9,]+\)\s*)+)\s*\{([0-9,]+)\}'
    match = re.match(pattern, line)

    if not match:
        raise ValueError(f"Invalid machine line: {line}")

    lights_str, buttons_str, jolts_str = match.groups()

    target_lights = [1 if c == '#' else 0 for c in lights_str]

    button_matches = re.findall(r'\(([0-9,]+)\)', buttons_str)
    buttons = []
    for button_match in button_matches:
        indices = [int(x) for x in button_match.split(',')]
        buttons.append(indices)

    jolts = [int(x) for x in jolts_str.split(',')]

    return target_lights, buttons, jolts


def solve_part_1_machine(target_lights, buttons):
    n_lights = len(target_lights)
    n_buttons = len(buttons)

    for num_presses in range(n_buttons + 1):
        for combo in combinations(range(n_buttons), num_presses):
            lights = [0] * n_lights
            for button_idx in combo:
                for light_idx in buttons[button_idx]:
                    lights[light_idx] = 1 - lights[light_idx]  # Toggle

            if lights == target_lights:
                return num_presses

    return float('inf')


def solve_integer_linear_program(jolts, buttons):
    n_counters = len(jolts)
    n_buttons = len(buttons)

    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(n_buttons)]

    prob += pulp.lpSum(x)

    for counter_idx in range(n_counters):
        constraint = 0
        for button_idx in range(n_buttons):
            if counter_idx in buttons[button_idx]:
                constraint += x[button_idx]
        prob += constraint == jolts[counter_idx]

    try:
        prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=10))
    except Exception:
        return None

    if prob.status == pulp.LpStatusOptimal:
        return int(sum(x[i].varValue for i in range(n_buttons)))
    else:
        return None



def solve_part_2_machine(jolts, buttons):
    result = solve_integer_linear_program(jolts, buttons)
    if result is not None:
        return result

    return greedy_heuristic(jolts, buttons)


def greedy_heuristic(jolts, buttons):
    n_counters = len(jolts)
    counters = [0] * n_counters
    total_presses = 0

    max_iterations = sum(jolts) * 2

    for _ in range(max_iterations):
        if counters == jolts:
            return total_presses

        max_deficit = 0
        target_counter = -1
        for i in range(n_counters):
            deficit = jolts[i] - counters[i]
            if deficit > max_deficit:
                max_deficit = deficit
                target_counter = i

        if max_deficit <= 0:
            break

        best_button = -1
        best_score = -1

        for button_idx, button in enumerate(buttons):
            if target_counter in button:
                score = 0
                for counter_idx in button:
                    if counters[counter_idx] < jolts[counter_idx]:
                        score += 1

                if score > best_score:
                    best_score = score
                    best_button = button_idx

        if best_button == -1:
            break

        for counter_idx in buttons[best_button]:
            counters[counter_idx] += 1
        total_presses += 1

    return total_presses if counters == jolts else float('inf')




def solve_part_1(input_data: str) -> Any:
    lines = input_data.strip().split('\n')
    total_presses = 0

    for line in lines:
        target_lights, buttons, _ = parse_machine(line)
        presses = solve_part_1_machine(target_lights, buttons)
        if presses == float('inf'):
            return "No solution found"
        total_presses += presses

    return total_presses


def solve_part_2(input_data: str) -> Any:
    lines = input_data.strip().split('\n')
    total_presses = 0

    for line in lines:
        _, buttons, jolts = parse_machine(line)
        presses = solve_part_2_machine(jolts, buttons)
        if presses == float('inf'):
            return "No solution found"
        total_presses += presses

    return total_presses
