from typing import Any


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')
    checksum = 0

    for line in lines:
        numbers = [int(x) for x in line.split()]
        checksum += max(numbers) - min(numbers)

    return checksum


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')
    checksum = 0

    for line in lines:
        numbers = [int(x) for x in line.split()]
        # Find the two numbers that divide evenly
        for i, num1 in enumerate(numbers):
            for num2 in numbers[i+1:]:
                if num1 % num2 == 0:
                    checksum += num1 // num2
                    break
                elif num2 % num1 == 0:
                    checksum += num2 // num1
                    break

    return checksum
