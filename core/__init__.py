"""
Core functionality for Advent of Code solutions.

This package contains the fundamental components needed to run AOC solutions:
- Input handling and downloading
- Solution loading and execution
- Tracking and database operations
- Submission handling
"""

from .input_handler import InputHandler, is_input_available
from .solution_loader import SolutionLoader
from .tracker import AOCTracker
from .submitter import AOCSubmitter

__all__ = [
    'InputHandler',
    'is_input_available',
    'SolutionLoader',
    'AOCTracker',
    'AOCSubmitter'
]
