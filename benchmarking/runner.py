"""
Benchmarking functionality for Advent of Code solutions.

This module provides comprehensive benchmarking capabilities at different levels:
- Individual problems (single day/part)
- Full day (both parts)
- Full year (all days in a year)
- Full set (all available solutions)
"""

import importlib.util
import statistics
import time
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
import json

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False
    # Initialize dummy colorama for when it's not available
    init = lambda **kwargs: None

    # Fallback classes for when colorama is not available
    class _DummyStyle:
        BRIGHT = ""
        RESET_ALL = ""

    class _DummyFore:
        CYAN = ""
        YELLOW = ""
        GREEN = ""
        BLUE = ""
        RED = ""
        MAGENTA = ""
        WHITE = ""

    Fore = _DummyFore()
    Style = _DummyStyle()

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.input_handler import get_input
from core.tracker import AOCTracker
from .results import BenchmarkResult, BenchmarkStats


def create_progress_bar(current: int, total: int, width: int = 40, prefix: str = "") -> str:
    """Create a progress bar string."""
    if total == 0:
        return f"{prefix}[{'=' * width}] 0/0 (100%)"

    percentage = current / total
    filled = int(width * percentage)
    bar = '=' * filled + '-' * (width - filled)
    percent_str = f"{percentage * 100:.1f}%"

    return f"{prefix}[{bar}] {current}/{total} ({percent_str})"


def clear_current_line():
    """Clear the current console line."""
    if sys.stdout.isatty():  # Only clear if we're in a real terminal
        sys.stdout.write('\r\033[K')  # Move to beginning and clear line
        sys.stdout.flush()


def print_progress_update(message: str, overwrite: bool = True):
    """Print a progress update, optionally overwriting the current line."""
    if overwrite:
        clear_current_line()
        sys.stdout.write(f"\r{message}")
        sys.stdout.flush()
    else:
        print(message)


class BenchmarkRunner:
    """Main benchmarking class."""

    def __init__(self, tracker: AOCTracker = None, publish_to_db: bool = False, expected_values: Dict[int, str] = None):
        self.results: List[BenchmarkResult] = []
        self.tracker = tracker
        self.publish_to_db = publish_to_db
        self.expected_values = expected_values or {}

    def validate_result(self, result: Any, part: int) -> bool:
        """Validate result against expected value if configured."""
        if part not in self.expected_values:
            return True  # No validation requested

        expected = self.expected_values[part].strip()
        actual = str(result).strip()
        return actual == expected

    def load_solution_module(self, year: int, day: int) -> Any:
        """Load the solution module for the given year and day."""
        module_name = f"{year}.day{day}"
        module_path = Path.cwd() / f"{year}" / f"day{day}.py"

        if not module_path.exists():
            raise FileNotFoundError(f"Solution file not found: {module_path}")

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module spec for {module_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            raise ImportError(f"Failed to load module {module_path}: {e}")

    def get_input_data(self, year: int, day: int) -> str:
        """Get input data for the given year and day."""
        try:
            return get_input(year, day, sample=False)
        except Exception as e:
            raise RuntimeError(f"Failed to get input for {year} day {day}: {e}")

    def publish_result_to_db(self, result: BenchmarkResult, input_data: str, code_content: str) -> None:
        """Publish a benchmark result to the tracking database."""
        if not self.tracker or not self.publish_to_db:
            return

        try:
            self.tracker.record_run(
                year=result.year,
                day=result.day,
                part=result.part,
                execution_time=result.execution_time,
                result=result.result,
                input_data=input_data,
                code_content=code_content,
                success=result.success,
                error_message=result.error_message,
                is_sample=False  # Benchmarks are always on real data
            )
        except Exception as e:
            print(f"⚠️  Failed to publish benchmark result to database: {e}")

    def run_single_benchmark(self, year: int, day: int, part: int,
                           input_data: str, module: Any, timeout: float = 30.0) -> BenchmarkResult:
        """Run a single benchmark for a specific part with timeout."""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Benchmark timed out after {timeout} seconds")

        try:
            # Set up timeout (only on Unix systems)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(int(timeout))

            start_time = time.perf_counter()

            if part == 1:
                result = module.solve_part_1(input_data)
            elif part == 2:
                result = module.solve_part_2(input_data)
            else:
                raise ValueError(f"Invalid part number: {part}")

            end_time = time.perf_counter()
            execution_time = end_time - start_time

            # Cancel timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)

            # Skip if too slow
            if execution_time > timeout:
                return BenchmarkResult(
                    year=year,
                    day=day,
                    part=part,
                    success=False,
                    result=None,
                    execution_time=execution_time,
                    error_message=f"Execution too slow: {execution_time:.1f}s > {timeout}s",
                    validation_passed=None
                )

            # Validate result if expected value is configured
            validation_passed = None
            if part in self.expected_values:
                validation_passed = self.validate_result(result, part)

            return BenchmarkResult(
                year=year,
                day=day,
                part=part,
                success=True,
                result=result,
                execution_time=execution_time,
                validation_passed=validation_passed
            )

        except Exception as e:
            # Cancel timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return BenchmarkResult(
                year=year,
                day=day,
                part=part,
                success=False,
                result=None,
                execution_time=0.0,
                error_message=str(e),
                validation_passed=None
            )

    def benchmark_problem(self, year: int, day: int, part: int,
                         runs: int = 10, warmup_runs: int = 3, timeout: float = 30.0) -> BenchmarkStats:
        """Benchmark a specific problem multiple times."""
        print(f"Benchmarking {year} Day {day} Part {part} ({runs} runs, {warmup_runs} warmup)...")

        try:
            module = self.load_solution_module(year, day)
            input_data = self.get_input_data(year, day)

            # Get code content for database publishing
            code_content = ""
            if self.publish_to_db:
                module_path = Path.cwd() / f"{year}" / f"day{day}.py"
                if module_path.exists():
                    code_content = module_path.read_text()
        except Exception as e:
            print(f"❌ Failed to setup benchmark: {e}")
            return BenchmarkStats(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, [])

        all_results = []

        # Warmup runs with progress
        for i in range(warmup_runs):
            progress = create_progress_bar(i, warmup_runs, prefix="  Warmup: ")
            print_progress_update(progress)

            result = self.run_single_benchmark(year, day, part, input_data, module, timeout)
            if result.success:
                validation_indicator = ""
                if result.validation_passed is not None:
                    validation_indicator = " ✅" if result.validation_passed else " ❌"
                print(f"  Warmup {i+1}/{warmup_runs}: {result.execution_time*1000:.3f}ms{validation_indicator}")
            else:
                print(f"  Warmup {i+1}/{warmup_runs}: ❌ {result.error_message}")

            if not result.success:
                print_progress_update(f"  Warmup {i+1}/{warmup_runs}: ❌ {result.error_message}", overwrite=False)

        # Clear warmup progress line
        clear_current_line()
        print(f"  Warmup complete ({warmup_runs} runs)")

        # Actual benchmark runs with progress
        for i in range(runs):
            progress = create_progress_bar(i, runs, prefix="  Benchmark: ")
            print_progress_update(progress)

            result = self.run_single_benchmark(year, day, part, input_data, module, timeout)
            all_results.append(result)

            # Publish to database if configured
            if self.publish_to_db:
                self.publish_result_to_db(result, input_data, code_content)

            if result.success:
                validation_indicator = ""
                if result.validation_passed is not None:
                    validation_indicator = " ✅" if result.validation_passed else " ❌"
                print(f"  Run {i+1}/{runs}: {result.execution_time*1000:.3f}ms{validation_indicator}")
            else:
                print_progress_update(f"  Run {i+1}/{runs}: ❌ {result.error_message}", overwrite=False)

        # Clear final progress line
        clear_current_line()

        # Calculate statistics
        successful_times = [r.execution_time for r in all_results if r.success]
        success_count = len(successful_times)
        success_rate = success_count / runs if runs > 0 else 0.0

        if successful_times:
            min_time = min(successful_times)
            max_time = max(successful_times)
            mean_time = statistics.mean(successful_times)
            median_time = statistics.median(successful_times)
            std_dev = statistics.stdev(successful_times) if len(successful_times) > 1 else 0.0
        else:
            min_time = max_time = mean_time = median_time = std_dev = 0.0

        # Calculate validation statistics
        validation_enabled = part in self.expected_values
        validation_passed_count = sum(1 for r in all_results if r.validation_passed is True)
        expected_value = self.expected_values.get(part)

        # Show completion with final stats
        if successful_times:
            print(f"  Completed: {success_count}/{runs} successful runs, avg: {format_time(mean_time)}")
        else:
            print(f"  Completed: {success_count}/{runs} successful runs")
        return BenchmarkStats(
            runs=runs,
            success_count=success_count,
            success_rate=success_rate,
            min_time=min_time,
            max_time=max_time,
            mean_time=mean_time,
            median_time=median_time,
            std_dev=std_dev,
            times=successful_times,
            validation_enabled=validation_enabled,
            validation_passed_count=validation_passed_count,
            expected_value=expected_value
        )

    def benchmark_day(self, year: int, day: int, runs: int = 5, timeout: float = 30.0) -> Dict[int, BenchmarkStats]:
        """Benchmark available parts of a specific day."""
        results = {}

        print(f"\n{'='*60}")
        if COLOR_SUPPORT:
            print(f"{Fore.CYAN}{Style.BRIGHT}🎄 Benchmarking {year} Day {day}{Style.RESET_ALL}")
        else:
            print(f"🎄 Benchmarking {year} Day {day}")
        print(f"{'='*60}")

        # Check which parts are available before benchmarking
        try:
            from core.solution_loader import SolutionLoader
            loader = SolutionLoader()
            module = loader.load_solution_module(year, day)

            available_parts = loader.get_available_parts(module)

            if not available_parts:
                print(f"❌ No solve_part functions found for {year} Day {day}")
                return results

            total_parts = len(available_parts)

            for i, part in enumerate(available_parts):
                # Show progress for multiple parts
                if total_parts > 1:
                    progress = create_progress_bar(i, total_parts, prefix=f"Day {day} Progress: ")
                    print_progress_update(progress)

                try:
                    stats = self.benchmark_problem(year, day, part, runs, timeout=timeout)
                    results[part] = stats

                    # Clear progress line and show results
                    if total_parts > 1:
                        clear_current_line()

                    self.print_benchmark_stats(f"Part {part}", stats)

                except Exception as e:
                    if total_parts > 1:
                        clear_current_line()
                    print(f"❌ Failed to benchmark Part {part}: {e}")
                    results[part] = BenchmarkStats(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, [])

            # Clear final progress line
            if total_parts > 1:
                clear_current_line()
                print(f"✅ Day {day} completed ({total_parts} parts)")

        except Exception as e:
            print(f"❌ Failed to load module for {year} Day {day}: {e}")

        return results

    def benchmark_year(self, year: int, runs: int = 3, timeout: float = 30.0) -> Dict[int, Dict[int, BenchmarkStats]]:
        """Benchmark all available solutions for a given year."""
        year_path = Path.cwd() / str(year)
        if not year_path.exists():
            print(f"❌ Year {year} directory not found")
            return {}

        # Find all day files and sort by day number
        day_files = [f for f in year_path.glob("day*.py")]
        if not day_files:
            print(f"❌ No solution files found in {year_path}")
            return {}

        # Sort by day number (extract numeric part)
        day_files = sorted(day_files, key=lambda f: int(f.stem.replace('day', '')))

        results = {}

        print(f"\n{'='*60}")
        if COLOR_SUPPORT:
            print(f"{Fore.CYAN}{Style.BRIGHT}🎄 Benchmarking Year {year} ({len(day_files)} days){Style.RESET_ALL}")
        else:
            print(f"🎄 Benchmarking Year {year} ({len(day_files)} days)")
        print(f"{'='*60}")

        total_days = len(day_files)

        for i, day_file in enumerate(day_files):
            # Extract day number from filename
            day_num = int(day_file.stem.replace('day', ''))

            # Show overall year progress
            progress = create_progress_bar(i, total_days, prefix=f"Year {year} Progress: ")
            print_progress_update(progress)

            try:
                day_results = self.benchmark_day(year, day_num, runs, timeout)
                results[day_num] = day_results
            except Exception as e:
                clear_current_line()
                print(f"❌ Failed to benchmark Day {day_num}: {e}")

        # Clear final progress line
        clear_current_line()
        print(f"✅ Year {year} benchmarking completed ({total_days} days)")

        self.print_year_summary(year, results)
        return results

    def benchmark_all(self, runs: int = 3, timeout: float = 30.0) -> Dict[int, Dict[int, Dict[int, BenchmarkStats]]]:
        """Benchmark all available solutions across all years."""
        # Find all year directories and sort by year number
        year_dirs = [d for d in Path.cwd().iterdir()
                    if d.is_dir() and d.name.isdigit()]
        year_dirs = sorted(year_dirs, key=lambda d: int(d.name))

        if not year_dirs:
            print("❌ No year directories found")
            return {}

        all_results = {}

        print(f"\n{'='*60}")
        if COLOR_SUPPORT:
            print(f"{Fore.CYAN}{Style.BRIGHT}🎄 Benchmarking All Solutions ({len(year_dirs)} years){Style.RESET_ALL}")
        else:
            print(f"🎄 Benchmarking All Solutions ({len(year_dirs)} years)")
        print(f"{'='*60}")

        total_years = len(year_dirs)

        for i, year_dir in enumerate(year_dirs):
            year = int(year_dir.name)

            # Show overall progress across all years
            progress = create_progress_bar(i, total_years, prefix="Overall Progress: ")
            print_progress_update(progress)

            try:
                year_results = self.benchmark_year(year, runs, timeout)
                all_results[year] = year_results
            except Exception as e:
                clear_current_line()
                print(f"❌ Failed to benchmark Year {year}: {e}")

        # Clear final progress line
        clear_current_line()
        print(f"✅ All benchmarking completed ({total_years} years)")

        self.print_overall_summary(all_results)
        return all_results

    def print_benchmark_stats(self, title: str, stats: BenchmarkStats) -> None:
        """Print formatted benchmark statistics."""
        if COLOR_SUPPORT:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}📊 {title} Statistics:{Style.RESET_ALL}")
        else:
            print(f"\n📊 {title} Statistics:")

        if stats.success_count == 0:
            print("  ❌ All runs failed")
            return

        print(f"  Success Rate: {stats.success_rate*100:.1f}% ({stats.success_count}/{stats.runs})")

        # Display validation results if enabled
        if stats.validation_enabled:
            validation_rate = stats.validation_passed_count / stats.success_count * 100 if stats.success_count > 0 else 0
            if stats.validation_passed_count == stats.success_count:
                print(f"  Validation:   ✅ {stats.validation_passed_count}/{stats.success_count} passed (expected: {stats.expected_value})")
            else:
                print(f"  Validation:   ❌ {stats.validation_passed_count}/{stats.success_count} passed ({validation_rate:.1f}%)")
                print(f"                Expected: {stats.expected_value}")

        print(f"  Fastest:      {format_time(stats.min_time)}")
        print(f"  Slowest:      {format_time(stats.max_time)}")
        print(f"  Mean Time:    {format_time(stats.mean_time)}")
        print(f"  Median Time:  {format_time(stats.median_time)}")
        print(f"  Std Dev:      {format_time(stats.std_dev)}")

        # Show performance consistency
        if stats.mean_time > 0:
            variation = stats.std_dev / stats.mean_time
            if COLOR_SUPPORT:
                if variation < 0.05:  # Less than 5% variation
                    print(f"  {Fore.GREEN}✅ Consistent performance ({variation*100:.1f}% variation){Style.RESET_ALL}")
                elif variation < 0.15:  # Less than 15% variation
                    print(f"  {Fore.YELLOW}⚠️  Moderate variation ({variation*100:.1f}%){Style.RESET_ALL}")
                else:
                    print(f"  {Fore.RED}⚠️  High variation ({variation*100:.1f}%){Style.RESET_ALL}")
            else:
                print(f"  Performance variation: {variation*100:.1f}%")

    def print_year_summary(self, year: int, results: Dict[int, Dict[int, BenchmarkStats]]) -> None:
        """Print summary for a year's benchmarks."""
        if not results:
            return

        print(f"\n{'='*60}")
        if COLOR_SUPPORT:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}📈 Year {year} Summary{Style.RESET_ALL}")
        else:
            print(f"📈 Year {year} Summary")
        print(f"{'='*60}")

        total_problems = 0
        successful_problems = 0
        all_times = []

        # Collect data
        for day, day_results in results.items():
            for part, stats in day_results.items():
                total_problems += 1
                if stats.success_count > 0:
                    successful_problems += 1
                    all_times.extend(stats.times)

        if all_times:
            fastest_time = min(all_times)
            slowest_time = max(all_times)
            avg_time = statistics.mean(all_times)
            total_time = sum(all_times)
        else:
            fastest_time = slowest_time = avg_time = total_time = 0.0

        print(f"Total Problems: {total_problems}")
        print(f"Successful: {successful_problems} ({successful_problems/total_problems*100:.1f}%)")
        print(f"Fastest Solution: {format_time(fastest_time)}")
        print(f"Slowest Solution: {format_time(slowest_time)}")
        print(f"Average Time: {format_time(avg_time)}")
        print(f"Total Runtime: {format_time(total_time)}")

        # Show fastest and slowest solutions
        if all_times:
            problem_times = []
            for day, day_results in results.items():
                for part, stats in day_results.items():
                    if stats.success_count > 0:
                        problem_times.append((day, part, stats.min_time))

            problem_times.sort(key=lambda x: x[2])

            # Show fastest solutions
            print(f"\n{Fore.GREEN if COLOR_SUPPORT else ''}🚀 Top 5 Fastest Solutions:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
            for i, (day, part, time) in enumerate(problem_times[:5]):
                print(f"  {i+1}. Day {day:2d} Part {part}: {format_time(time)}")

            # Show slowest solutions
            if len(problem_times) > 1:
                print(f"\n{Fore.RED if COLOR_SUPPORT else ''}🐌 Top 5 Slowest Solutions:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
                slowest_times = problem_times[-5:]
                slowest_times.reverse()  # Show slowest first
                for i, (day, part, time) in enumerate(slowest_times):
                    print(f"  {i+1}. Day {day:2d} Part {part}: {format_time(time)}")

    def print_overall_summary(self, all_results: Dict[int, Dict[int, Dict[int, BenchmarkStats]]]) -> None:
        """Print overall summary across all years."""
        if not all_results:
            return

        print(f"\n{'='*60}")
        if COLOR_SUPPORT:
            print(f"{Fore.CYAN}{Style.BRIGHT}🌟 Overall Summary{Style.RESET_ALL}")
        else:
            print(f"🌟 Overall Summary")
        print(f"{'='*60}")

        total_problems = 0
        successful_problems = 0
        all_times = []
        year_summaries = []

        # Collect data from all years
        for year, year_results in all_results.items():
            year_problems = 0
            year_successful = 0
            year_times = []

            for day, day_results in year_results.items():
                for part, stats in day_results.items():
                    total_problems += 1
                    year_problems += 1
                    if stats.success_count > 0:
                        successful_problems += 1
                        year_successful += 1
                        all_times.extend(stats.times)
                        year_times.extend(stats.times)

            if year_times:
                year_summaries.append({
                    'year': year,
                    'problems': year_problems,
                    'successful': year_successful,
                    'avg_time': statistics.mean(year_times),
                    'total_time': sum(year_times)
                })

        print(f"Total Problems Benchmarked: {total_problems}")
        print(f"Successfully Solved: {successful_problems} ({successful_problems/total_problems*100:.1f}%)")

        if all_times:
            print(f"Fastest Solution: {format_time(min(all_times))}")
            print(f"Slowest Solution: {format_time(max(all_times))}")
            print(f"Average Time: {format_time(statistics.mean(all_times))}")
            print(f"Total Runtime: {format_time(sum(all_times))}")

            # Overall fastest and slowest across all years
            all_problem_times = []
            for year, year_results in all_results.items():
                for day, day_results in year_results.items():
                    for part, stats in day_results.items():
                        if stats.success_count > 0:
                            all_problem_times.append((year, day, part, stats.min_time))

            if all_problem_times:
                all_problem_times.sort(key=lambda x: x[3])

                # Show fastest solutions across all years
                print(f"\n{Fore.GREEN if COLOR_SUPPORT else ''}🚀 Top 5 Fastest Solutions Overall:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
                for i, (year, day, part, time) in enumerate(all_problem_times[:5]):
                    print(f"  {i+1}. {year} Day {day:2d} Part {part}: {format_time(time)}")

                # Show slowest solutions across all years
                if len(all_problem_times) > 1:
                    print(f"\n{Fore.RED if COLOR_SUPPORT else ''}🐌 Top 5 Slowest Solutions Overall:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
                    slowest_overall = all_problem_times[-5:]
                    slowest_overall.reverse()  # Show slowest first
                    for i, (year, day, part, time) in enumerate(slowest_overall):
                        print(f"  {i+1}. {year} Day {day:2d} Part {part}: {format_time(time)}")

            # Year comparisons
            if len(year_summaries) > 1:
                print(f"\n{Fore.BLUE if COLOR_SUPPORT else ''}📊 Year Comparisons:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
                year_summaries.sort(key=lambda x: x['avg_time'])
                for i, year_data in enumerate(year_summaries):
                    status = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
                    print(f"  {status} {year_data['year']}: {format_time(year_data['avg_time'])} avg "
                          f"({year_data['successful']}/{year_data['problems']} solved)")

    def save_benchmark_results(self, results: Dict, filename: str = None) -> None:
        """Save benchmark results to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"

        def convert_stats_to_dict(stats: BenchmarkStats) -> dict:
            """Convert BenchmarkStats to dictionary."""
            return {
                'runs': stats.runs,
                'success_count': stats.success_count,
                'success_rate': stats.success_rate,
                'min_time': stats.min_time,
                'max_time': stats.max_time,
                'mean_time': stats.mean_time,
                'median_time': stats.median_time,
                'std_dev': stats.std_dev,
                'times': stats.times
            }

        # Convert BenchmarkStats to dictionaries for JSON serialization
        serializable_results = {}
        for year, year_data in results.items():
            serializable_results[year] = {}
            for day, day_data in year_data.items():
                serializable_results[year][day] = {}

                # Handle both dict of parts and direct BenchmarkStats
                if isinstance(day_data, dict):
                    for part, stats in day_data.items():
                        serializable_results[year][day][part] = convert_stats_to_dict(stats)
                else:
                    # This is a BenchmarkStats object directly
                    serializable_results[year][day] = convert_stats_to_dict(day_data)

        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': serializable_results
            }, f, indent=2)

        print(f"📄 Benchmark results saved to {filename}")


def format_time(seconds: float) -> str:
    """Format time in human-readable way."""
    if seconds < 0.001:  # Less than 1ms, show microseconds
        us = seconds * 1_000_000
        if us < 10:
            return f"{us:.1f}μs"
        elif us < 100:
            return f"{us:.0f}μs"
        else:
            return f"{us:.0f}μs"
    elif seconds < 1.0:  # Less than 1s, show milliseconds
        ms = seconds * 1000
        if ms < 10:
            return f"{ms:.2f}ms"
        elif ms < 100:
            return f"{ms:.1f}ms"
        else:
            return f"{ms:.0f}ms"
    else:  # 1s or more, show seconds
        if seconds < 10:
            return f"{seconds:.3f}s"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            mins = int(seconds // 60)
            secs = seconds % 60
            return f"{mins}m {secs:.1f}s"


if __name__ == "__main__":
    # Example usage
    runner = BenchmarkRunner()

    # Benchmark a single problem
    # stats = runner.benchmark_problem(2025, 1, 1, runs=10)
    # runner.print_benchmark_stats("Single Problem", stats)

    # Benchmark a full day
    # day_results = runner.benchmark_day(2025, 1, runs=5)

    # Benchmark a full year
    # year_results = runner.benchmark_year(2025, runs=3)

    # Benchmark everything
    # all_results = runner.benchmark_all(runs=3)

    print("Use the BenchmarkRunner class to run benchmarks!")
    print("Examples:")
    print("  runner = BenchmarkRunner()")
    print("  runner.benchmark_problem(2025, 1, 1, runs=10)")
    print("  runner.benchmark_day(2025, 1)")
    print("  runner.benchmark_year(2025)")
    print("  runner.benchmark_all()")
