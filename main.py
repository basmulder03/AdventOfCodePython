#!/usr/bin/env python3
"""
Advent of Code Solution Runner

A streamlined main entry point that coordinates the modular components
for running, benchmarking, and tracking AOC solutions.
"""

from cli import ArgumentParser, CommandHandlers
from core import AOCTracker, AOCSubmitter
from benchmarking import BenchmarkRunner


def main() -> None:
    """Main entry point for the Advent of Code solution runner."""
    # Set up argument parsing
    arg_parser = ArgumentParser()
    parser = arg_parser.setup_parser()
    args = parser.parse_args()

    # Initialize command handlers
    handlers = CommandHandlers()

    # Initialize tracking (can be disabled with --no-tracking)
    tracker = None if args.no_tracking else AOCTracker()

    # Get command (if any)
    command = getattr(args, 'command', None)

    # SYNC command
    if command == 'sync':
        if not tracker:
            print("Sync requires tracking to be enabled (remove --no-tracking)")
            return

        submitter = AOCSubmitter()
        if not submitter.is_configured():
            print("Session cookie is required for syncing. Please add your session cookie to session_cookie.txt")
            return

        handlers.handle_sync(submitter, tracker, args.year)
        return

    # BENCHMARK command
    if command == 'benchmark':
        # Handle full help
        if hasattr(args, 'help_full') and args.help_full:
            handlers.handle_benchmark_help()
            return

        # Initialize tracker for benchmarking if publishing is requested
        publish = hasattr(args, 'publish') and args.publish
        benchmark_tracker = tracker if publish else None

        # Get expected values if provided
        expected_values = {}
        if hasattr(args, 'expected') and args.expected:
            # Single expected value - use for the part being run if specified
            if hasattr(args, 'part') and args.part:
                expected_values[args.part] = args.expected
        if hasattr(args, 'expected_p1') and args.expected_p1:
            expected_values[1] = args.expected_p1
        if hasattr(args, 'expected_p2') and args.expected_p2:
            expected_values[2] = args.expected_p2

        runner = BenchmarkRunner(tracker=benchmark_tracker, publish_to_db=publish, expected_values=expected_values)
        results = None

        if publish and not tracker:
            print("⚠️  Database publishing requires tracking to be enabled (remove --no-tracking)")
            print("   Continuing without database publishing...")
            runner = BenchmarkRunner(expected_values=expected_values)

        # Determine scope
        if args.all:
            # Benchmark all available solutions
            results = runner.benchmark_all(runs=args.runs, timeout=args.timeout)

        elif args.year_flag:
            # Benchmark specific year (using --year flag)
            results = runner.benchmark_year(args.year_flag, runs=args.runs, timeout=args.timeout)

        elif args.year and args.day:
            # Benchmark specific day
            if args.part:
                # Benchmark single part
                stats = runner.benchmark_problem(args.year, args.day, args.part,
                                               runs=args.runs,
                                               warmup_runs=args.warmup,
                                               timeout=args.timeout)
                runner.print_benchmark_stats(f"{args.year} Day {args.day} Part {args.part}", stats)

                # Convert single problem result to nested dict format for saving
                results = {args.year: {args.day: {args.part: stats}}}
            else:
                # Benchmark full day (both parts)
                results = {args.year: runner.benchmark_day(args.year, args.day, runs=args.runs, timeout=args.timeout)}
        else:
            print("❌ Benchmark requires specifying scope")
            print("Examples:")
            print("  python main.py benchmark 2025 1              # Benchmark both parts of day 1")
            print("  python main.py benchmark 2025 1 --part 1     # Benchmark only part 1")
            print("  python main.py benchmark --year 2025         # Benchmark all of 2025")
            print("  python main.py benchmark --all               # Benchmark everything")
            return

        # Save results if requested
        if hasattr(args, 'save') and args.save and results:
            filename = None if args.save == 'auto' else args.save
            runner.save_benchmark_results(results, filename)

        # Auto-update markdown if results were published to database
        if publish and tracker:
            print("\n📝 Updating markdown documentation with new benchmark results...")
            if args.all:
                handlers.handle_update_markdown(tracker, update_all=True)
            elif args.year_flag:
                handlers.handle_update_markdown(tracker, year=args.year_flag)
            elif args.year:
                handlers.handle_update_markdown(tracker, year=args.year)

        return

    # STATS command
    if command == 'stats':
        if not tracker:
            print("Statistics require tracking to be enabled (remove --no-tracking)")
            return

        year_filter = getattr(args, 'year', None)
        handlers.handle_stats(tracker, year_filter)

        if hasattr(args, 'update_readme') and args.update_readme:
            # Deprecated: redirect to new markdown handler
            print("⚠️  --update-readme is deprecated, use 'python main.py markdown' instead")
            handlers.handle_update_markdown(tracker)

        return

    # MARKDOWN command
    if command == 'markdown':
        if not tracker:
            print("Markdown updates require tracking to be enabled (remove --no-tracking)")
            return

        # Determine year and day from either positional or flag arguments
        year = args.year_pos if hasattr(args, 'year_pos') and args.year_pos else getattr(args, 'year', None)
        day = args.day_pos if hasattr(args, 'day_pos') and args.day_pos else getattr(args, 'day', None)

        if args.all:
            handlers.handle_update_markdown(tracker, update_all=True)
        elif year and day:
            handlers.handle_update_markdown(tracker, year=year, day=day)
        elif year:
            handlers.handle_update_markdown(tracker, year=year)
        else:
            handlers.handle_update_markdown(tracker)

        return

    # If we get here, it's the default run command (no subcommand specified)

    # Show history if requested
    if args.history:
        if not args.year or not args.day:
            print("❌ History requires year and day arguments")
            print("Example: python main.py 2025 1 --history")
            return
        if tracker:
            handlers.handle_history(tracker, args.year, args.day, args.part)
        else:
            print("History requires tracking to be enabled (remove --no-tracking)")
        return

    # Validate required arguments for solution running
    if args.year is None or args.day is None:
        parser.print_help()
        return

    # Check if puzzle HTML needs to be downloaded
    from pathlib import Path

    # Check if we need to download puzzle parts
    puzzle_part1_file = Path.cwd() / ".puzzle_html" / str(args.year) / f"day{args.day}" / "part1.txt"
    puzzle_part2_file = Path.cwd() / ".puzzle_html" / str(args.year) / f"day{args.day}" / "part2.txt"

    # Auto-download if:
    # 1. Part 1 doesn't exist (fresh download)
    # 2. Part 1 exists but part 2 doesn't (need to refresh for part 2)
    needs_download = not puzzle_part1_file.exists() or (puzzle_part1_file.exists() and not puzzle_part2_file.exists())

    # Initialize submitter only if needed
    submitter = AOCSubmitter() if (args.submit or needs_download) else None

    # Download puzzle HTML if needed (silently)
    if needs_download and submitter and submitter.is_configured():
        submitter.download_puzzle_html(args.year, args.day)

    # Validate submission requirements
    if args.submit and args.part is None:
        print("❌ Submission requires specifying a single part with --part 1 or --part 2")
        print("Example: python main.py 2025 3 --part 1 --submit")
        return

    try:
        module = handlers.solution_loader.load_solution_module(args.year, args.day)
    except FileNotFoundError as e:
        print(str(e))
        return

    # Get input data
    input_data = handlers.get_input_data(args)
    is_sample = args.sample or bool(args.sample_input)

    # Print header
    title = handlers.display.format_title(args.year, args.day, is_sample, args.part)
    handlers.display.print_header(title)

    total_time = 0.0

    # Determine which parts to run based on availability
    available_parts = handlers.solution_loader.get_available_parts(module)

    if not available_parts:
        print(f"❌ No solve_part functions found in the solution file")
        return

    # Run requested parts
    parts_to_run = []
    if args.part is not None:
        # Specific part requested
        if args.part in available_parts:
            parts_to_run = [args.part]
        else:
            print(f"❌ Part {args.part} is not available. Available parts: {', '.join(map(str, available_parts))}")
            return
    else:
        # No specific part requested, run all available parts
        parts_to_run = available_parts

    # Determine timeout setting
    timeout = None if args.no_timeout else args.timeout

    # Get expected values if provided
    expected_values = {}
    if hasattr(args, 'expected') and args.expected:
        # Single expected value - use for the part being run
        if args.part:
            expected_values[args.part] = args.expected
    if hasattr(args, 'expected_p1') and args.expected_p1:
        expected_values[1] = args.expected_p1
    if hasattr(args, 'expected_p2') and args.expected_p2:
        expected_values[2] = args.expected_p2

    # Run the determined parts
    for part_num in parts_to_run:
        expected_value = expected_values.get(part_num)
        success, elapsed, result = handlers.run_part(module, part_num, input_data, args.year, args.day,
                                          tracker, submitter, args.submit, is_sample, timeout, expected_value)
        if success:
            total_time += elapsed

    # Print footer with total time
    handlers.display.print_footer(total_time)


if __name__ == "__main__":
    main()
