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
from typing import Any, Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from datetime import datetime
import json

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False
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


class BenchmarkRunner:
    """Main benchmarking class."""

    def __init__(self, tracker: AOCTracker = None, publish_to_db: bool = False):
        self.results: List[BenchmarkResult] = []
        self.tracker = tracker
        self.publish_to_db = publish_to_db

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
                    error_message=f"Execution too slow: {execution_time:.1f}s > {timeout}s"
                )

            return BenchmarkResult(
                year=year,
                day=day,
                part=part,
                success=True,
                result=result,
                execution_time=execution_time
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
                error_message=str(e)
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

        # Warmup runs
        for i in range(warmup_runs):
            result = self.run_single_benchmark(year, day, part, input_data, module, timeout)
            if result.success:
                print(f"  Warmup {i+1}/{warmup_runs}: {result.execution_time*1000:.3f}ms")
            else:
                print(f"  Warmup {i+1}/{warmup_runs}: ❌ {result.error_message}")

        # Actual benchmark runs
        for i in range(runs):
            result = self.run_single_benchmark(year, day, part, input_data, module, timeout)
            all_results.append(result)

            # Publish to database if configured
            if self.publish_to_db:
                self.publish_result_to_db(result, input_data, code_content)

            if result.success:
                print(f"  Run {i+1}/{runs}: {result.execution_time*1000:.3f}ms")
            else:
                print(f"  Run {i+1}/{runs}: ❌ {result.error_message}")

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

        return BenchmarkStats(
            runs=runs,
            success_count=success_count,
            success_rate=success_rate,
            min_time=min_time,
            max_time=max_time,
            mean_time=mean_time,
            median_time=median_time,
            std_dev=std_dev,
            times=successful_times
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

            for part in available_parts:
                try:
                    stats = self.benchmark_problem(year, day, part, runs, timeout=timeout)
                    results[part] = stats
                    self.print_benchmark_stats(f"Part {part}", stats)
                except Exception as e:
                    print(f"❌ Failed to benchmark Part {part}: {e}")
                    results[part] = BenchmarkStats(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, [])

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

        for day_file in day_files:
            # Extract day number from filename
            day_num = int(day_file.stem.replace('day', ''))

            try:
                day_results = self.benchmark_day(year, day_num, runs, timeout)
                results[day_num] = day_results
            except Exception as e:
                print(f"❌ Failed to benchmark Day {day_num}: {e}")

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

        for year_dir in year_dirs:
            year = int(year_dir.name)
            try:
                year_results = self.benchmark_year(year, runs, timeout)
                all_results[year] = year_results
            except Exception as e:
                print(f"❌ Failed to benchmark Year {year}: {e}")

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
        print(f"  Min Time:     {stats.min_time*1000:.3f}ms")
        print(f"  Max Time:     {stats.max_time*1000:.3f}ms")
        print(f"  Mean Time:    {stats.mean_time*1000:.3f}ms")
        print(f"  Median Time:  {stats.median_time*1000:.3f}ms")
        print(f"  Std Dev:      {stats.std_dev*1000:.3f}ms")

        if COLOR_SUPPORT:
            if stats.std_dev/stats.mean_time < 0.05:  # Less than 5% variation
                print(f"  {Fore.GREEN}✅ Consistent performance{Style.RESET_ALL}")
            elif stats.std_dev/stats.mean_time < 0.15:  # Less than 15% variation
                print(f"  {Fore.YELLOW}⚠️  Moderate variation{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}⚠️  High variation{Style.RESET_ALL}")

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
        print(f"Fastest Solution: {fastest_time*1000:.3f}ms")
        print(f"Slowest Solution: {slowest_time*1000:.3f}ms")
        print(f"Average Time: {avg_time*1000:.3f}ms")
        print(f"Total Runtime: {total_time*1000:.3f}ms")

        # Show fastest solutions
        if all_times:
            print(f"\n{Fore.GREEN if COLOR_SUPPORT else ''}🚀 Top 5 Fastest Solutions:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
            problem_times = []
            for day, day_results in results.items():
                for part, stats in day_results.items():
                    if stats.success_count > 0:
                        problem_times.append((day, part, stats.min_time))

            problem_times.sort(key=lambda x: x[2])
            for i, (day, part, time) in enumerate(problem_times[:5]):
                print(f"  {i+1}. Day {day:2d} Part {part}: {time*1000:.3f}ms")

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
            print(f"Fastest Solution: {min(all_times)*1000:.3f}ms")
            print(f"Slowest Solution: {max(all_times)*1000:.3f}ms")
            print(f"Average Time: {statistics.mean(all_times)*1000:.3f}ms")
            print(f"Total Runtime: {sum(all_times)*1000:.3f}ms")

            # Year comparisons
            if len(year_summaries) > 1:
                print(f"\n{Fore.BLUE if COLOR_SUPPORT else ''}📊 Year Comparisons:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
                year_summaries.sort(key=lambda x: x['avg_time'])
                for i, year_data in enumerate(year_summaries):
                    status = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
                    print(f"  {status} {year_data['year']}: {year_data['avg_time']*1000:.3f}ms avg "
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
    ms = seconds * 1000
    if ms < 1:
        return f"{ms:.3f}ms"
    elif ms < 100:
        return f"{ms:.2f}ms"
    elif ms < 1000:
        return f"{ms:.1f}ms"
    else:
        return f"{seconds:.2f}s"


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
