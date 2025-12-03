"""
Benchmarking functionality for Advent of Code solutions.

This package provides comprehensive benchmarking capabilities at different levels:
- Individual problems (single day/part)
- Full day (both parts)
- Full year (all days in a year)
- Full set (all available solutions)
"""

from .runner import BenchmarkRunner
from .results import BenchmarkResult, BenchmarkStats

__all__ = ['BenchmarkRunner', 'BenchmarkResult', 'BenchmarkStats']
