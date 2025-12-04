"""
Time formatting utilities.
"""


def format_time(ms: float) -> str:
    """Format milliseconds into human-readable time string."""
    if ms < 0.05:  # Less than 0.05ms (50μs) show as microseconds
        return f"{ms * 1000:.1f}μs"
    elif ms < 1000:
        return f"{ms:.1f}ms"
    elif ms < 60000:
        return f"{ms / 1000:.2f}s"
    else:
        minutes = int(ms // 60000)
        seconds = (ms % 60000) / 1000
        return f"{minutes}m {seconds:.1f}s"
