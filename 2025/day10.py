from typing import Any
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    total_presses = 0

    for line in input_data.strip().split('\n'):
        lights_match = re.search(r'\[([.#]+)\]', line)
        target = lights_match.group(1)
        num_lights = len(target)

        target_state = [1 if c == '#' else 0 for c in target]

        buttons = []
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        for button_str in button_matches:
            indices = [int(x) for x in button_str.split(',')]
            button_vec = [0] * num_lights
            for idx in indices:
                button_vec[idx] = 1
            buttons.append(button_vec)

        min_presses = solve_gf2_system(buttons, target_state, num_lights)
        total_presses += min_presses

    return total_presses


def solve_gf2_system(buttons, target, num_lights):
    num_buttons = len(buttons)

    matrix = []
    for light_idx in range(num_lights):
        row = [buttons[button_idx][light_idx] for button_idx in range(num_buttons)]
        row.append(target[light_idx])
        matrix.append(row)

    pivot_col = 0
    pivot_row = 0
    pivot_cols = []

    while pivot_row < num_lights and pivot_col < num_buttons:
        found_pivot = False
        for row in range(pivot_row, num_lights):
            if matrix[row][pivot_col] == 1:
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break

        if not found_pivot:
            pivot_col += 1
            continue

        pivot_cols.append(pivot_col)

        for row in range(num_lights):
            if row != pivot_row and matrix[row][pivot_col] == 1:
                for col in range(num_buttons + 1):
                    matrix[row][col] ^= matrix[pivot_row][col]

        pivot_row += 1
        pivot_col += 1

    for row in range(pivot_row, num_lights):
        if matrix[row][num_buttons] == 1:
            return float('inf')

    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]

    if not free_vars:
        solution = [0] * num_buttons
        for row in range(len(pivot_cols)):
            pivot_col_idx = pivot_cols[row]
            solution[pivot_col_idx] = matrix[row][num_buttons]
        return sum(solution)

    min_presses = float('inf')

    for free_vals in range(1 << len(free_vars)):
        solution = [0] * num_buttons

        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = (free_vals >> i) & 1

        for row in range(len(pivot_cols)):
            pivot_col_idx = pivot_cols[row]
            val = matrix[row][num_buttons]
            for col in range(num_buttons):
                if col != pivot_col_idx:
                    val ^= (matrix[row][col] * solution[col])
            solution[pivot_col_idx] = val

        presses = sum(solution)
        min_presses = min(min_presses, presses)

    return min_presses


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    total_presses = 0

    for line in input_data.strip().split('\n'):
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        buttons = []
        for button_str in button_matches:
            indices = [int(x) for x in button_str.split(',')]
            buttons.append(indices)

        joltage_match = re.search(r'\{([0-9,]+)\}', line)
        target_joltages = [int(x) for x in joltage_match.group(1).split(',')]
        num_counters = len(target_joltages)

        min_presses = solve_joltage_system(buttons, target_joltages, num_counters)
        total_presses += min_presses

    return total_presses


def solve_joltage_system(buttons, target, num_counters):

    num_buttons = len(buttons)

    A = np.zeros((num_counters, num_buttons), dtype=float)
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            A[counter_idx][button_idx] = 1.0

    b = np.array(target, dtype=float)

    c = np.ones(num_buttons)

    constraints = LinearConstraint(A, lb=b, ub=b)

    bounds = Bounds(lb=0, ub=np.inf)

    integrality = np.ones(num_buttons)

    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(np.sum(result.x))

    from scipy.optimize import linprog
    result = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='highs')

    if result.success:
        x_int = np.round(result.x).astype(int)
        computed = A @ x_int
        if np.allclose(computed, b):
            return int(np.sum(x_int))

    return 0

