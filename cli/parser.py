"""
Argument parser setup for the CLI.
"""
import argparse
import sys


class ArgumentParser:
    """Handles command-line argument parsing."""

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up and return the command line argument parser."""
        # Check if first argument is a known subcommand
        subcommands = ['sync', 'benchmark', 'stats', 'markdown', 'animation']
        has_subcommand = len(sys.argv) > 1 and sys.argv[1] in subcommands

        if has_subcommand:
            # Use subcommand-based parser
            return self._setup_subcommand_parser()
        else:
            # Use default run parser with positional year/day
            return self._setup_run_parser()

    def _setup_run_parser(self) -> argparse.ArgumentParser:
        """Setup parser for default run mode."""
        parser = argparse.ArgumentParser(
            description="Run Advent of Code solutions",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run solutions
  python main.py 2025 1                           # Run both parts
  python main.py 2025 1 --part 1                 # Run part 1 only
  python main.py 2025 1 -s                       # Run with sample input
  
  # Run with validation
  python main.py 2025 1 --expected-p1 123 --expected-p2 456
  python main.py 2025 1 --part 1 --expected 123
  
  # Other commands (use subcommands):
  python main.py sync 2025                       # Sync year 2025 from AOC website
  python main.py benchmark 2025 1                # Benchmark day 1
  python main.py stats                           # Show statistics
  python main.py markdown --all                  # Update all markdown
            """
        )

        # Positional arguments for default run behavior
        parser.add_argument("year", type=int, nargs='?', help="the year of the AOC challenge")
        parser.add_argument("day", type=int, nargs='?', help="the day of the AOC challenge")

        # Common options for running solutions
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
        parser.add_argument("--timeout", type=float, default=5.0,
                           help="timeout for solution execution in seconds (default: 5.0)")
        parser.add_argument("--no-timeout", action="store_true",
                           help="disable timeout for solution execution")
        parser.add_argument("--expected", type=str,
                           help="expected output value to validate against")
        parser.add_argument("--expected-p1", type=str,
                           help="expected output value for part 1")
        parser.add_argument("--expected-p2", type=str,
                           help="expected output value for part 2")
        parser.add_argument("--animation", action="store_true",
                           help="run animation if available for this solution")
        parser.add_argument("--export-gif", type=str, metavar="FILENAME",
                           help="export animation as GIF to specified filename (requires --animation)")

        return parser

    def _setup_subcommand_parser(self) -> argparse.ArgumentParser:
        """Setup parser with subcommands."""
        parser = argparse.ArgumentParser(
            description="Run Advent of Code solutions",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Create subparsers for commands
        subparsers = parser.add_subparsers(dest='command', help='Command to execute')

        # SYNC subcommand
        sync_parser = subparsers.add_parser('sync', help='Sync completed problems from AOC website')
        sync_parser.add_argument('year', type=int, help='Year to sync')
        sync_parser.add_argument("--no-tracking", action="store_true",
                                help="disable run tracking and performance comparison")

        # BENCHMARK subcommand
        benchmark_parser = subparsers.add_parser('benchmark',
                                                 help='Run benchmarks on solutions',
                                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                                 epilog="""
Examples:
  python main.py benchmark 2025 1              # Benchmark both parts of day 1
  python main.py benchmark 2025 1 --part 1     # Benchmark only part 1
  python main.py benchmark --year 2025         # Benchmark all of 2025
  python main.py benchmark --all               # Benchmark everything
  python main.py benchmark 2025 1 --save       # Save results to file
  python main.py benchmark 2025 1 --publish    # Publish to database
  
  # With validation
  python main.py benchmark 2025 1 --expected-p1 123 --expected-p2 456
  python main.py benchmark 2025 1 --part 1 --expected 123
                                                 """)
        benchmark_parser.add_argument('year', type=int, nargs='?', help='Year to benchmark')
        benchmark_parser.add_argument('day', type=int, nargs='?', help='Day to benchmark')
        benchmark_parser.add_argument("--part", "-p", type=int, choices=[1, 2],
                                     help="benchmark only specific part (1 or 2)")
        benchmark_parser.add_argument("--all", action="store_true",
                                     help="benchmark all available solutions")
        benchmark_parser.add_argument("--year", dest="year_flag", type=int,
                                     help="benchmark all solutions for specific year")
        benchmark_parser.add_argument("--runs", type=int, default=10,
                                     help="number of benchmark runs (default: 10)")
        benchmark_parser.add_argument("--warmup", type=int, default=3,
                                     help="number of warmup runs (default: 3)")
        benchmark_parser.add_argument("--timeout", type=float, default=30.0,
                                     help="timeout for individual benchmark runs in seconds (default: 30)")
        benchmark_parser.add_argument("--save", type=str, nargs='?', const='auto',
                                     help="save benchmark results to file (optional filename)")
        benchmark_parser.add_argument("--publish", action="store_true",
                                     help="publish benchmark results to tracking database (auto-updates markdown)")
        benchmark_parser.add_argument("--help-full", action="store_true",
                                     help="show detailed benchmarking help and examples")
        benchmark_parser.add_argument("--no-tracking", action="store_true",
                                     help="disable run tracking and performance comparison")
        benchmark_parser.add_argument("--expected", type=str,
                                     help="expected output value to validate against")
        benchmark_parser.add_argument("--expected-p1", type=str,
                                     help="expected output value for part 1")
        benchmark_parser.add_argument("--expected-p2", type=str,
                                     help="expected output value for part 2")

        # STATS subcommand
        stats_parser = subparsers.add_parser('stats', help='Show statistics from tracked data')
        stats_parser.add_argument("--year", type=int,
                                 help="filter stats by specific year")
        stats_parser.add_argument("--update-readme", action="store_true",
                                 help="update README.md with latest statistics (deprecated)")
        stats_parser.add_argument("--no-tracking", action="store_true",
                                 help="disable run tracking and performance comparison")

        # MARKDOWN subcommand
        markdown_parser = subparsers.add_parser('markdown', help='Update markdown documentation')
        markdown_parser.add_argument("--all", action="store_true",
                                    help="update all markdown files (main README + all year files)")
        markdown_parser.add_argument("--year", type=int,
                                    help="update markdown for specific year only")
        markdown_parser.add_argument("--day", type=int,
                                    help="update markdown for specific day (requires year and day)")
        markdown_parser.add_argument('year_pos', type=int, nargs='?', help='Year for markdown update')
        markdown_parser.add_argument('day_pos', type=int, nargs='?', help='Day for markdown update')
        markdown_parser.add_argument("--no-tracking", action="store_true",
                                    help="disable run tracking and performance comparison")

        # ANIMATION subcommand
        animation_parser = subparsers.add_parser('animation', help='Run animations for solutions')
        animation_parser.add_argument('year', type=int, help='Year of the problem')
        animation_parser.add_argument('day', type=int, help='Day of the problem')
        animation_parser.add_argument("--sample", "-s", action="store_true",
                                     help="use sample input instead of actual input")
        animation_parser.add_argument("--sample-input", type=str,
                                     help="provide sample input directly as a string (implies --sample)")
        animation_parser.add_argument("--export-gif", type=str, metavar="FILENAME",
                                     help="export animation as GIF to specified filename")
        animation_parser.add_argument("--speed", type=float, default=1.0,
                                     help="animation speed multiplier (default: 1.0)")
        animation_parser.add_argument("--no-tracking", action="store_true",
                                     help="disable run tracking and performance comparison")

        return parser
