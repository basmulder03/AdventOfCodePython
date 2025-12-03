from typing import Any


def solve_part_1(input_data: str) -> Any:
    n = int(input_data.strip())
    p = 1
    while p * 2 <= n:
        p *= 2
    return 2 * (n - p) + 1


def solve_part_2(input_data: str) -> Any:
    n = int(input_data.strip())
    p = 1
    while p * 3 <= n:
        p *= 3
    if n - p < p:
        return n - p
    return 2 * (n - p) - p

