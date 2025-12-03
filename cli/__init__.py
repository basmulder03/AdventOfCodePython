"""
Command-line interface components for Advent of Code solution runner.

This package contains:
- Argument parsing
- Command handling
- Help generation
"""

from .parser import ArgumentParser
from .handlers import CommandHandlers

__all__ = ['ArgumentParser', 'CommandHandlers']
