"""
Argument parser setup for the CLI.
"""
import argparse


class ArgumentParser:
    """Handles command-line argument parsing."""

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up and return the command line argument parser."""
        parser = argparse.ArgumentParser(description="Run Advent of Code solutions")
        parser.add_argument("year", type=int, nargs='?', help="the year of the AOC challenge")
        parser.add_argument("day", type=int, nargs='?', help="the day of the AOC challenge")
        parser.add_argument("--sample", "-s", action="store_true",
                           help="use sample input instead of actual input")
        parser.add_argument("--sample-input", type=str,
                           help="provide sample input directly as a string (implies --sample)")
        parser.add_argument("--part", "-p", type=int, choices=[1, 2],
                           help="run only specific part (1 or 2)")
        parser.add_argument("--submit", action="store_true",
                           help="submit the answer to AOC (requires --part, only for actual input)")
        parser.add_argument("--no-tracking", action="store_true",
                           help="disable run tracking and performance comparison")
        parser.add_argument("--history", action="store_true",
                           help="show recent run history for this problem")
        parser.add_argument("--stats", action="store_true",
                           help="generate statistics tables from tracked data")
        parser.add_argument("--update-readme", action="store_true",
                           help="update README.md with latest statistics")
        parser.add_argument("--year-filter", type=int,
                           help="filter stats by specific year (used with --stats)")
        parser.add_argument("--sync", type=int,
                           help="sync already completed problems from AOC website for specified year")

        # Benchmark arguments
        parser.add_argument("--benchmark", action="store_true",
                           help="run benchmarking on specified problem/day/year")
        parser.add_argument("--benchmark-runs", type=int, default=10,
                           help="number of benchmark runs (default: 10)")
        parser.add_argument("--benchmark-warmup", type=int, default=3,
                           help="number of warmup runs (default: 3)")
        parser.add_argument("--benchmark-all", action="store_true",
                           help="benchmark all available solutions")
        parser.add_argument("--benchmark-year", type=int,
                           help="benchmark all solutions for specific year")
        parser.add_argument("--benchmark-save", type=str, nargs='?', const='auto',
                           help="save benchmark results to file (optional filename)")
        parser.add_argument("--benchmark-timeout", type=float, default=30.0,
                           help="timeout for individual benchmark runs in seconds (default: 30)")
        parser.add_argument("--benchmark-publish", action="store_true",
                           help="publish benchmark results to tracking database")
        parser.add_argument("--benchmark-help", action="store_true",
                           help="show detailed benchmarking help and examples")

        return parser
