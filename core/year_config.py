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

    The last day traditionally only has part 1 - you get the second star
    for free after completing all other puzzles.

    Args:
        year: The AOC year
        day: The day number

    Returns:
        True if this is the last day of the year, False otherwise
    """
    return day == get_max_day(year)


def get_expected_parts(year: int, day: int) -> list[int]:
    """
    Get the expected parts for a given day.

    Args:
        year: The AOC year
        day: The day number

    Returns:
        List of expected part numbers (e.g., [1, 2] or just [1] for last day)
    """
    if is_last_day(year, day):
        # Last day traditionally only has part 1
        return [1]
    else:
        # All other days have parts 1 and 2
        return [1, 2]

