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
from .markdown_generator import MarkdownGenerator
from .hardware_info import get_hardware_info, format_hardware_info, format_hardware_info_compact

__all__ = ['DisplayFormatter', 'StatsGenerator', 'format_time', 'MarkdownGenerator',
           'get_hardware_info', 'format_hardware_info', 'format_hardware_info_compact']
