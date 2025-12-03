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

    # Handle benchmark help
    if args.benchmark_help:
        handlers.handle_benchmark_help()
        return

    # Initialize tracking and submission
    tracker = None if args.no_tracking else AOCTracker()
    submitter = AOCSubmitter() if args.submit else None

    # Handle sync operation
    if args.sync:
        if not tracker:
            print("Sync requires tracking to be enabled (remove --no-tracking)")
            return

        # Need submitter for fetching data from AOC website
        if not submitter:
            submitter = AOCSubmitter()

        if not submitter.is_configured():
            print("Session cookie is required for syncing. Please add your session cookie to session_cookie.txt")
            return

        handlers.handle_sync(submitter, tracker, args.sync)
        return

    # Handle stats generation
    if args.stats or args.update_readme:
        if not tracker:
            print("Statistics require tracking to be enabled (remove --no-tracking)")
            return

        if args.stats:
            handlers.handle_stats(tracker, args.year_filter)

        if args.update_readme:
            handlers.handle_update_readme(tracker)

        return

    # Handle benchmarking
    if args.benchmark or args.benchmark_all or args.benchmark_year:
        # Initialize tracker for benchmarking if publishing is requested
        benchmark_tracker = tracker if args.benchmark_publish else None
        runner = BenchmarkRunner(tracker=benchmark_tracker, publish_to_db=args.benchmark_publish)
        results = None

        if args.benchmark_publish and not tracker:
            print("⚠️  Database publishing requires tracking to be enabled (remove --no-tracking)")
            print("   Continuing without database publishing...")
            runner = BenchmarkRunner()

        if args.benchmark_all:
            # Benchmark all available solutions
            results = runner.benchmark_all(runs=args.benchmark_runs, timeout=args.benchmark_timeout)

        elif args.benchmark_year:
            # Benchmark specific year
            results = runner.benchmark_year(args.benchmark_year, runs=args.benchmark_runs, timeout=args.benchmark_timeout)

        elif args.benchmark:
            # Benchmark specific problem/day
            if args.year is None or args.day is None:
                print("❌ Benchmark requires specifying year and day")
                print("Examples:")
                print("  python main.py 2025 1 --benchmark              # Benchmark both parts of day 1")
                print("  python main.py 2025 1 --benchmark --part 1     # Benchmark only part 1")
                print("  python main.py --benchmark-year 2025           # Benchmark all of 2025")
                print("  python main.py --benchmark-all                 # Benchmark everything")
                return

            if args.part:
                # Benchmark single part
                stats = runner.benchmark_problem(args.year, args.day, args.part,
                                               runs=args.benchmark_runs,
                                               warmup_runs=args.benchmark_warmup,
                                               timeout=args.benchmark_timeout)
                runner.print_benchmark_stats(f"{args.year} Day {args.day} Part {args.part}", stats)

                # Convert single problem result to nested dict format for saving
                results = {args.year: {args.day: {args.part: stats}}}
            else:
                # Benchmark full day (both parts)
                results = {args.year: runner.benchmark_day(args.year, args.day, runs=args.benchmark_runs, timeout=args.benchmark_timeout)}

        # Save results if requested
        if args.benchmark_save and results:
            filename = None if args.benchmark_save == 'auto' else args.benchmark_save
            runner.save_benchmark_results(results, filename)

        return

    # Show history if requested
    if args.history:
        if tracker:
            handlers.handle_history(tracker, args.year, args.day, args.part)
        else:
            print("History requires tracking to be enabled (remove --no-tracking)")
        return

    # Validate required arguments for solution running
    if args.year is None or args.day is None:
        parser.print_help()
        return

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

    # Run the determined parts
    for part_num in parts_to_run:
        success, elapsed, result = handlers.run_part(module, part_num, input_data, args.year, args.day,
                                          tracker, submitter, args.submit, is_sample)
        if success:
            total_time += elapsed

    # Print footer with total time
    handlers.display.print_footer(total_time)


if __name__ == "__main__":
    main()
