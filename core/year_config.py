"""
Year-specific configuration for Advent of Code.

This module handles special cases for different years, such as:
- Years with fewer than 25 days (e.g., 2025 only has 12 days)
- Last day logic (traditionally, the last day only has part 1)
"""
from typing import Dict


# Years with non-standard number of days
SPECIAL_YEARS: Dict[int, int] = {
    2025: 12,  # 2025 only has 12 days instead of the usual 25
}


def get_max_day(year: int) -> int:
    """
    Get the maximum day number for a given year.

    Args:
        year: The AOC year

    Returns:
        The maximum day number (typically 25, but can be different for special years)
    """
    return SPECIAL_YEARS.get(year, 25)


def is_last_day(year: int, day: int) -> bool:
    """
    Check if a given day is the last day of the year.

    The last day has both part 1 and part 2. Part 2 is special: it accepts
    any answer as correct, but only after you've completed all other puzzles
    (earned 49 stars). This is the "free star" that completes the year.

    Args:
        year: The AOC year
        day: The day number

    Returns:
        True if this is the last day of the year, False otherwise
    """
    return day == get_max_day(year)


def get_expected_parts(year: int, day: int) -> list[int]:
    """
    Get the expected parts for a given day (for solution template generation).

    Args:
        year: The AOC year
        day: The day number

    Returns:
        List of expected part numbers for template generation.
        Last day returns [1] since part 2 accepts any answer and doesn't
        need a solve function.

    Note: This is for template generation only. The last day's part 2 can
    still be submitted to AOC (any answer works after earning the required stars).
    """
    if is_last_day(year, day):
        # Last day only needs solve_part_1 in template
        # Part 2 accepts any answer, so no solving function needed
        return [1]
    else:
        # All other days have both parts
        return [1, 2]


def get_required_stars_for_last_day_part2(year: int) -> int:
    """
    Get the number of stars required before the last day's part 2 becomes available.

    The last day's part 2 accepts any answer, but only after completing all other
    puzzles in the year.

    Args:
        year: The AOC year

    Returns:
        Number of stars required (e.g., 49 for 25-day years, 23 for 2025's 12-day event)

    Examples:
        >>> get_required_stars_for_last_day_part2(2023)  # 25 days
        49
        >>> get_required_stars_for_last_day_part2(2025)  # 12 days
        23
    """
    max_day = get_max_day(year)
    # Calculate: all previous days (2 stars each) + last day part 1 (1 star)
    return (max_day - 1) * 2 + 1


