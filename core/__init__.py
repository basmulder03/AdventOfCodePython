"""
Core functionality for Advent of Code solutions.

This package contains the fundamental components needed to run AOC solutions:
- Input handling and downloading
- Solution loading and execution
- Tracking and database operations
- Submission handling
- Year-specific configuration
"""

from .input_handler import InputHandler, is_input_available
from .solution_loader import SolutionLoader
from .tracker import AOCTracker
from .submitter import AOCSubmitter
from .year_config import get_max_day, is_last_day, get_expected_parts, get_required_stars_for_last_day_part2

__all__ = [
    'InputHandler',
    'is_input_available',
    'SolutionLoader',
    'AOCTracker',
    'AOCSubmitter',
    'get_max_day',
    'is_last_day',
    'get_expected_parts',
    'get_required_stars_for_last_day_part2'
]
