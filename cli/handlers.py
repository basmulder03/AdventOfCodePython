"""
Command handlers for various CLI operations.
"""
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, Any
import re

from core import AOCTracker, AOCSubmitter, SolutionLoader, InputHandler
from utils import DisplayFormatter, StatsGenerator, MarkdownGenerator
from benchmarking import BenchmarkRunner


class CommandHandlers:
    """Handles execution of various CLI commands."""

    def __init__(self):
        self.display = DisplayFormatter()
        self.solution_loader = SolutionLoader()
        self.input_handler = InputHandler()

    def handle_benchmark_help(self) -> None:
        """Show comprehensive benchmarking help."""
        help_text = """
🎄 Advent of Code Benchmarking Help

QUICK START:
  python main.py 2025 1 --benchmark                    # Benchmark both parts of day 1
  python benchmarking/quick.py fast 2025 1             # Quick benchmark with presets
  python benchmarking/quick.py --examples              # Show detailed examples

BASIC BENCHMARKING:
  --benchmark                                           # Enable benchmarking
  --benchmark-runs N           (default: 10)           # Number of measurement runs
  --benchmark-warmup N         (default: 3)            # Number of warmup runs  
  --benchmark-timeout N        (default: 30)           # Timeout per run (seconds)

SCOPE OPTIONS:
  python main.py YEAR DAY --benchmark                   # Single day (both parts)
  python main.py YEAR DAY --benchmark --part N          # Single part only
  python main.py --benchmark-year YEAR                 # All days in year
  python main.py --benchmark-all                       # All available solutions

SAVING RESULTS:
  --benchmark-save                                      # Auto-generate filename
  --benchmark-save filename.json                       # Custom filename
  --benchmark-publish                                   # Publish results to tracking database

QUICK PRESETS (benchmarking/quick.py):
  fast         3 runs, 2 warmup, 5s timeout           # Quick checks
  normal       10 runs, 3 warmup, 30s timeout         # Standard measurement
  thorough     25 runs, 5 warmup, 60s timeout         # Detailed analysis

EXAMPLES:
  # Quick development check
  python benchmarking/quick.py fast 2025 1

  # Detailed optimization analysis  
  python benchmarking/quick.py thorough 2025 1 --save

  # Find slow solutions across all years
  python main.py --benchmark-all --benchmark-runs 1 --benchmark-timeout 5

  # Regression testing
  python benchmarking/quick.py fast-year 2025 --save baseline.json

  # Compare implementations
  python main.py 2025 1 --benchmark --benchmark-save before.json
  # ... make changes ...
  python main.py 2025 1 --benchmark --benchmark-save after.json

  # Store benchmark results in database for tracking
  python main.py 2025 1 --benchmark --benchmark-publish

For detailed documentation: See docs/benchmarking.md
For more examples: python benchmarking/quick.py --examples
        """
        print(help_text)

    def handle_sync(self, submitter: AOCSubmitter, tracker: AOCTracker, year: int) -> None:
        """Sync completed problems from AOC website for the specified year."""
        print(f"🔄 Syncing completed problems for {year}...")
        print(f"Fetching completion data from adventofcode.com...")

        # Get completed problems from AOC website
        completed_data = submitter.sync_completed_problems(year)

        if not completed_data:
            print(f"⚠️  No completed problems found for {year}")
            return

        # Show what was found
        total_parts = sum(len(day_data['completed_parts']) for day_data in completed_data.values())
        days_with_answers = sum(1 for day_data in completed_data.values() if day_data['answers'])

        print(f"📊 Found {total_parts} completed parts across {len(completed_data)} days")
        if days_with_answers > 0:
            print(f"💡 Found actual answers for {days_with_answers} days")

        # Show detailed breakdown
        for day in sorted(completed_data.keys()):
            day_data = completed_data[day]
            parts_str = ", ".join(f"Part {p}" for p in sorted(day_data['completed_parts']))
            answers_info = ""
            if day_data['answers']:
                answers_info = f" (answers: {', '.join(f'P{k}: {v}' for k, v in day_data['answers'].items())})"

            print(f"  Day {day}: {parts_str}{answers_info}")

        # Sync to database
        new_answers_count = tracker.sync_completed_problems(year, completed_data)

        print(f"\n✅ Sync completed!")
        print(f"📈 Added {new_answers_count} new correct answers to database")

        if new_answers_count > 0:
            print(f"💡 You can now see these in statistics with --stats")

    def handle_stats(self, tracker: AOCTracker, year_filter: Optional[int] = None) -> None:
        """Generate and display statistics."""
        stats_gen = StatsGenerator(tracker)

        print("=" * 60)
        print("📊 ADVENT OF CODE STATISTICS")
        print("=" * 60)

        overall_stats = stats_gen.generate_overall_stats()
        year_stats = stats_gen.generate_stats_table(year_filter)

        stats_content = overall_stats + "\n" + year_stats
        print(stats_content)
        print("=" * 60)

    def handle_update_readme(self, tracker: AOCTracker) -> None:
        """Update README.md with the latest statistics."""
        readme_path = Path.cwd() / "README.md"
        if not readme_path.exists():
            print("❌ README.md not found")
            return

        stats_gen = StatsGenerator(tracker)

        # Generate stats content
        overall_stats = stats_gen.generate_overall_stats()
        year_stats = stats_gen.generate_stats_table(for_readme=True)
        stats_content = overall_stats + "\n" + year_stats

        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats_section = f"<!-- STATS_START -->\n{stats_content}\n\n*Last updated: {timestamp}*\n<!-- STATS_END -->"

        # Read current README
        current_content = readme_path.read_text(encoding='utf-8')

        # Replace stats section
        pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
        if re.search(pattern, current_content, re.DOTALL):
            new_content = re.sub(pattern, stats_section, current_content, flags=re.DOTALL)
        else:
            # If no stats section exists, append it
            new_content = current_content + "\n\n" + stats_section

        # Write updated README
        readme_path.write_text(new_content, encoding='utf-8')
        print("✅ README.md updated with latest statistics")

    def handle_update_markdown(self, tracker: AOCTracker, year: Optional[int] = None,
                              day: Optional[int] = None, update_all: bool = False) -> None:
        """Update markdown files based on specified scope."""
        md_gen = MarkdownGenerator(tracker)

        if update_all:
            # Update main README and all year files
            md_gen.update_all_readmes()
        elif year and day:
            # Update specific day
            md_gen.update_day_readme(year, day)
        elif year:
            # Update specific year
            md_gen.update_year_readme(year)
            md_gen.update_main_readme()
        else:
            # Default: update main README only
            md_gen.update_main_readme()

    def handle_history(self, tracker: AOCTracker, year: int, day: int, part: Optional[int] = None) -> None:
        """Show recent run history for this problem."""
        print(f"📈 Recent run history for {year} Day {day}")
        if part:
            print(f" Part {part}")
        print("=" * 50)

        history = tracker.get_recent_runs(year, day, part, limit=10)
        if not history:
            print("No run history found for this problem.")
            return

        for run in history:
            timestamp = run['timestamp']
            execution_time = run['execution_time_ms']
            success = "✅" if run['success'] else "❌"
            result_preview = str(run['result'])[:50] + ("..." if len(str(run['result'])) > 50 else "")

            print(f"{timestamp} | Part {run['part']} | {success} | {execution_time:.2f}ms | {result_preview}")

    def get_input_data(self, args: argparse.Namespace) -> str:
        """Get input data based on command line arguments."""
        if args.sample_input:
            # Decode escape sequences like \n, \t, etc.
            return args.sample_input.encode().decode('unicode_escape')

        return self.input_handler.get_input(args.year, args.day, args.sample or args.sample_input)

    def run_part(self, module: Any, part_num: int, input_data: str, year: int, day: int,
                tracker: Optional[AOCTracker], submitter: Optional[AOCSubmitter],
                should_submit: bool, is_sample: bool, timeout: Optional[float] = None) -> Tuple[bool, float, Any]:
        """Run a single part of the solution with optional timeout."""
        from time import perf_counter
        import inspect
        import threading

        # Get the code content for tracking
        code_content = ""
        try:
            code_content = inspect.getsource(module)
        except (OSError, TypeError):
            # Fallback: try to read the file directly
            try:
                module_path = Path.cwd() / f"{year}" / f"day{day}.py"
                if module_path.exists():
                    code_content = module_path.read_text()
            except Exception:
                pass

        try:
            func_name = f"solve_part_{part_num}"
            if not hasattr(module, func_name):
                self.display.print_part_error(part_num, Exception(f"Function {func_name} not found in module"))
                return False, 0.0, None

            func = getattr(module, func_name)

            # Execute function with optional timeout
            result = None
            elapsed_time = 0.0
            exception = None

            if timeout is not None and timeout > 0:
                # Use threading for cross-platform timeout support
                result_container = [None]
                exception_container = [None]

                def run_func():
                    try:
                        result_container[0] = func(input_data)
                    except Exception as e:
                        exception_container[0] = e

                start_time = perf_counter()
                thread = threading.Thread(target=run_func, daemon=True)
                thread.start()
                thread.join(timeout)
                end_time = perf_counter()
                elapsed_time = end_time - start_time

                if thread.is_alive():
                    # Timeout occurred
                    raise TimeoutError(f"Solution execution timed out after {timeout} seconds")

                if exception_container[0]:
                    raise exception_container[0]

                result = result_container[0]
            else:
                # No timeout - run directly
                start_time = perf_counter()
                result = func(input_data)
                end_time = perf_counter()
                elapsed_time = end_time - start_time

            self.display.print_part_result(part_num, result, elapsed_time, tracker, year, day, code_content)

            # Track the run if tracking is enabled
            if tracker and not is_sample:
                tracker.record_run(
                    year=year,
                    day=day,
                    part=part_num,
                    execution_time=elapsed_time,
                    result=str(result),
                    input_data=input_data,
                    code_content=code_content,
                    success=True,
                    is_sample=is_sample
                )

            # Handle submission if requested
            if should_submit and submitter and not is_sample and part_num:
                self.handle_submission(submitter, tracker, year, day, part_num, result)

            return True, elapsed_time, result

        except Exception as e:
            self.display.print_part_error(part_num, e)

            # Track failed run if tracking is enabled
            if tracker and not is_sample:
                tracker.record_run(
                    year=year,
                    day=day,
                    part=part_num,
                    execution_time=0,
                    result=None,
                    input_data=input_data,
                    code_content=code_content,
                    success=False,
                    error_message=str(e),
                    is_sample=is_sample
                )

            return False, 0.0, None

    def handle_submission(self, submitter: AOCSubmitter, tracker: Optional[AOCTracker],
                         year: int, day: int, part: int, answer: Any) -> None:
        """Handle answer submission to AOC."""
        print(f"\n🚀 Submitting answer for {year} Day {day} Part {part}...")

        success, message, wait_time = submitter.submit_answer(year, day, part, str(answer))

        if success:
            print(f"✅ {message}")

            # Record successful submission in tracker
            if tracker:
                tracker.record_submission(year, day, part, str(answer), 'correct', message)

        elif wait_time:
            print(f"⏰ {message}")
            print(f"   Please wait {wait_time} seconds before submitting again.")

            # Record rate-limited submission
            if tracker:
                tracker.record_submission(year, day, part, str(answer), 'rate_limited', message, wait_time)
        else:
            print(f"❌ {message}")

            # Record failed submission
            if tracker:
                tracker.record_submission(year, day, part, str(answer), 'incorrect', message)
