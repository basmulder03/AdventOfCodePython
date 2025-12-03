from typing import Any
import re


def solve_part_1(input_data: str) -> Any:
    # Parse the input to get row and column
    match = re.search(r'row (\d+), column (\d+)', input_data)
    if not match:
        raise ValueError("Could not parse row and column from input")

    row = int(match.group(1))
    col = int(match.group(2))

    # Calculate which code number we need
    # The codes are filled diagonally
    # Diagonal d contains positions where row + col = d + 1
    d = row + col - 1

    # Number of codes in diagonals 1 through d-1
    codes_before_diagonal = d * (d - 1) // 2

    # Position within diagonal d
    # In diagonal d, positions go: (d,1), (d-1,2), (d-2,3), ..., (1,d)
    # So for position (row, col), it's the col-th position in the diagonal
    position_in_diagonal = col

    # Total code number (1-indexed)
    code_number = codes_before_diagonal + position_in_diagonal

    # Generate the code
    # First code is 20151125
    # Each subsequent code: (previous * 252533) % 33554393
    code = 20151125

    for i in range(1, code_number):
        code = (code * 252533) % 33554393

    return code


def solve_part_2(input_data: str) -> Any:
    """Day 25 traditionally has no part 2."""
    return "Merry Christmas!"
