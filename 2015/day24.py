from typing import Any
from itertools import combinations
import math


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    weights = [int(line.strip()) for line in input_data.strip().split('\n')]
    total_weight = sum(weights)

    # Each group must have exactly 1/3 of the total weight
    if total_weight % 3 != 0:
        return None

    target_weight = total_weight // 3

    # Find all possible first groups (passenger compartment) with minimum number of packages
    min_packages = float('inf')
    best_quantum_entanglement = float('inf')

    # Try different numbers of packages in the first group, starting from the smallest
    for num_packages in range(1, len(weights) + 1):
        found_valid = False

        # Generate all combinations of this size
        for combo in combinations(weights, num_packages):
            if sum(combo) == target_weight:
                # Check if remaining packages can be split into two equal groups
                remaining = [w for w in weights if w not in combo]

                if can_split_into_two_equal_groups(remaining, target_weight):
                    found_valid = True
                    quantum_entanglement = math.prod(combo)

                    if num_packages < min_packages:
                        min_packages = num_packages
                        best_quantum_entanglement = quantum_entanglement
                    elif num_packages == min_packages:
                        best_quantum_entanglement = min(best_quantum_entanglement, quantum_entanglement)

        # If we found valid configurations with this number of packages, we don't need to check larger numbers
        if found_valid:
            break

    return best_quantum_entanglement


def can_split_into_two_equal_groups(weights, target_weight):
    """Check if weights can be split into two groups of equal weight (target_weight each)."""
    if sum(weights) != 2 * target_weight:
        return False

    # Use dynamic programming to check if we can form a subset with target_weight
    # If we can, then the remaining will also have target_weight
    dp = [False] * (target_weight + 1)
    dp[0] = True

    for weight in weights:
        # Traverse from right to left to avoid using the same weight multiple times
        for w in range(target_weight, weight - 1, -1):
            dp[w] = dp[w] or dp[w - weight]

    return dp[target_weight]


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    weights = [int(line.strip()) for line in input_data.strip().split('\n')]
    total_weight = sum(weights)

    # Each group must have exactly 1/4 of the total weight (4 groups in part 2)
    if total_weight % 4 != 0:
        return None

    target_weight = total_weight // 4

    # Find all possible first groups (passenger compartment) with minimum number of packages
    min_packages = float('inf')
    best_quantum_entanglement = float('inf')

    # Try different numbers of packages in the first group, starting from the smallest
    for num_packages in range(1, len(weights) + 1):
        found_valid = False

        # Generate all combinations of this size
        for combo in combinations(weights, num_packages):
            if sum(combo) == target_weight:
                # Check if remaining packages can be split into three equal groups
                remaining = [w for w in weights if w not in combo]

                if can_split_into_three_equal_groups(remaining, target_weight):
                    found_valid = True
                    quantum_entanglement = math.prod(combo)

                    if num_packages < min_packages:
                        min_packages = num_packages
                        best_quantum_entanglement = quantum_entanglement
                    elif num_packages == min_packages:
                        best_quantum_entanglement = min(best_quantum_entanglement, quantum_entanglement)

        # If we found valid configurations with this number of packages, we don't need to check larger numbers
        if found_valid:
            break

    return best_quantum_entanglement


def can_split_into_three_equal_groups(weights, target_weight):
    """Check if weights can be split into three groups of equal weight (target_weight each)."""
    if sum(weights) != 3 * target_weight:
        return False

    # Try all combinations for the first group
    for num_packages in range(1, len(weights)):
        for combo in combinations(weights, num_packages):
            if sum(combo) == target_weight:
                remaining = [w for w in weights if w not in combo]
                # Check if remaining can be split into two equal groups
                if can_split_into_two_equal_groups(remaining, target_weight):
                    return True
    return False
