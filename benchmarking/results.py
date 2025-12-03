"""
Data structures for benchmark results and statistics.
"""
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class BenchmarkResult:
    """Single benchmark run result."""
    year: int
    day: int
    part: int
    success: bool
    result: Any
    execution_time: float  # in seconds
    error_message: Optional[str] = None


@dataclass
class BenchmarkStats:
    """Statistics for multiple benchmark runs."""
    runs: int
    success_count: int
    success_rate: float
    min_time: float
    max_time: float
    mean_time: float
    median_time: float
    std_dev: float
    times: List[float]  # All successful run times
