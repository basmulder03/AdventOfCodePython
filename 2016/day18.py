from typing import Any


def solve_part_1(input_data: str) -> Any:
    row = [c == '^' for c in input_data.strip()]
    safe_count = sum(not trap for trap in row)

    for _ in range(39):
        new_row = []
        for i in range(len(row)):
            left = row[i-1] if i > 0 else False
            right = row[i+1] if i < len(row)-1 else False
            # Trap if left XOR right (one is trap, other is safe)
            is_trap = left != right
            new_row.append(is_trap)
            if not is_trap:
                safe_count += 1
        row = new_row

    return safe_count


def solve_part_2(input_data: str) -> Any:
    row = [c == '^' for c in input_data.strip()]
    safe_count = sum(not trap for trap in row)

    for _ in range(399999):
        new_row = []
        for i in range(len(row)):
            left = row[i-1] if i > 0 else False
            right = row[i+1] if i < len(row)-1 else False
            # Trap if left XOR right (one is trap, other is safe)
            is_trap = left != right
            new_row.append(is_trap)
            if not is_trap:
                safe_count += 1
        row = new_row

    return safe_count

