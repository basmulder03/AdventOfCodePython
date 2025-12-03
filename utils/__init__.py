"""
Utility functions for Advent of Code solution runner.

This package contains helper functions for:
- Text formatting and display
- Statistics generation
- Output styling
- Time formatting
"""

from .display import DisplayFormatter
from .stats import StatsGenerator
from .time_utils import format_time

__all__ = ['DisplayFormatter', 'StatsGenerator', 'format_time']
