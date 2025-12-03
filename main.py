import argparse
import importlib.util
from pathlib import Path
from time import perf_counter
from typing import Any, Optional, Tuple
from datetime import datetime
from input import get_input
from tracking import AOCTracker
from submitter import AOCSubmitter

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

    def init(**kwargs):
        pass  # Do nothing if colorama is not available

    Fore = _DummyFore()
    Style = _DummyStyle()


def load_solution_module(year: int, day: int) -> Any:
    """Load the solution module for the given year and day."""
    module_name = f"{year}.day{day}"
    module_path = Path.cwd() / f"{year}" / f"day{day}.py"

    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module spec for {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (FileNotFoundError, ImportError, AttributeError):
        create_solution_file(year, day)
        raise FileNotFoundError(f"Solution file created at {module_path}. Please implement the functions.")


def create_solution_file(year: int, day: int) -> None:
    """Create a template solution file for the given year and day."""
    year_dir = Path.cwd() / str(year)
    year_dir.mkdir(exist_ok=True)

    solution_file = year_dir / f"day{day}.py"
    if not solution_file.exists():
        template = (
            "from typing import Any\n\n\n"
            "def solve_part_1(input_data: str) -> Any:\n"
            "    \"\"\"Solve part 1 of the challenge.\"\"\"\n"
            "    pass\n\n\n"
            "def solve_part_2(input_data: str) -> Any:\n"
            "    \"\"\"Solve part 2 of the challenge.\"\"\"\n"
            "    pass\n"
        )
        solution_file.write_text(template)


def get_input_data(args: argparse.Namespace) -> str:
    """Get input data based on command line arguments."""
    if args.sample_input:
        # Decode escape sequences like \n, \t, etc.
        return args.sample_input.encode().decode('unicode_escape')

    return get_input(args.year, args.day, args.sample or args.sample_input)


def format_title(year: int, day: int, is_sample: bool, part: Optional[int]) -> str:
    """Format the title with appropriate styling."""
    if COLOR_SUPPORT:
        title = f"🎄 Advent of Code {year} - Day {day} 🎄"
        if is_sample:
            title += f" {Fore.YELLOW}[SAMPLE]{Style.RESET_ALL}"
        if part:
            title += f" {Fore.MAGENTA}[Part {part}]{Style.RESET_ALL}"
        return f"{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}"
    else:
        title = f"Advent of Code {year} - Day {day}"
        if is_sample:
            title += " [SAMPLE]"
        if part:
            title += f" [Part {part}]"
        return title


def print_part_result(part_num: int, result: Any, elapsed_time: float,
                     perf_data: dict = None) -> None:
    """Print the result for a specific part."""
    if COLOR_SUPPORT:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⭐ Part {part_num}:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Answer: {Style.BRIGHT}{result}{Style.RESET_ALL}")
        print(f"  {Fore.BLUE}Time: {elapsed_time * 1000:.3f} ms{Style.RESET_ALL}")
    else:
        print(f"Part {part_num}:")
        print(f"  Answer: {result}")
        print(f"  Time: {elapsed_time * 1000:.3f} ms")

    # Show performance comparison if available
    if perf_data:
        if COLOR_SUPPORT:
            if perf_data['improvement_vs_best'] > 0:
                print(f"  {Fore.GREEN}🚀 {perf_data['improvement_vs_best']:.1f}% faster than best ({perf_data['best_time']:.3f} ms){Style.RESET_ALL}")
            elif perf_data['improvement_vs_best'] < 0:
                print(f"  {Fore.RED}🐌 {abs(perf_data['improvement_vs_best']):.1f}% slower than best ({perf_data['best_time']:.3f} ms){Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}🥇 New personal best!{Style.RESET_ALL}")

            if perf_data['improvement_vs_prev'] is not None:
                if perf_data['improvement_vs_prev'] > 0:
                    print(f"  {Fore.CYAN}📈 {perf_data['improvement_vs_prev']:.1f}% faster than previous run{Style.RESET_ALL}")
                elif perf_data['improvement_vs_prev'] < 0:
                    print(f"  {Fore.MAGENTA}📉 {abs(perf_data['improvement_vs_prev']):.1f}% slower than previous run{Style.RESET_ALL}")
        else:
            if perf_data['improvement_vs_best'] > 0:
                print(f"  {perf_data['improvement_vs_best']:.1f}% faster than best ({perf_data['best_time']:.3f} ms)")
            elif perf_data['improvement_vs_best'] < 0:
                print(f"  {abs(perf_data['improvement_vs_best']):.1f}% slower than best ({perf_data['best_time']:.3f} ms)")
            else:
                print(f"  New personal best!")

        print(f"  Run #{perf_data['total_runs']}")

    print()


def print_part_error(part_num: int, error: Exception) -> None:
    """Print an error for a specific part."""
    if COLOR_SUPPORT:
        print(f"{Fore.RED}❌ Part {part_num} Error: {error}{Style.RESET_ALL}\n")
    else:
        print(f"Part {part_num} Error: {error}\n")


def run_part(module: Any, part_num: int, input_data: str, year: int, day: int,
             tracker: AOCTracker = None, submitter: AOCSubmitter = None,
             should_submit: bool = False, is_sample: bool = False) -> Tuple[bool, float, Any]:
    """Run a specific part of the solution and return success status, elapsed time, and result."""
    try:
        # Get code content for tracking
        code_content = ""
        if tracker:
            module_path = Path.cwd() / f"{year}" / f"day{day}.py"
            if module_path.exists():
                code_content = module_path.read_text()

        start_time = perf_counter()
        if part_num == 1:
            result = module.solve_part_1(input_data)
        else:
            result = module.solve_part_2(input_data)
        end_time = perf_counter()

        elapsed_time = end_time - start_time

        # Determine if this run should be considered successful for tracking
        is_successful = False
        if tracker and result is not None:
            # Check if we have a known correct answer
            correct_answer = tracker.get_correct_answer(year, day, part_num)
            if correct_answer is not None:
                # We know the correct answer, so only successful if it matches
                is_successful = str(result) == correct_answer
            else:
                # No known correct answer yet, so we'll consider any non-None result as potentially successful
                # This will be updated when we get submission feedback
                is_successful = True

        # Track the run
        if tracker:
            tracker.record_run(year, day, part_num, elapsed_time, result,
                             input_data, code_content, is_successful)

            # Get performance comparison (only for successful runs)
            perf_data = tracker.get_performance_comparison(year, day, part_num,
                                                         elapsed_time, code_content) if is_successful else None
        else:
            perf_data = None

        print_part_result(part_num, result, elapsed_time, perf_data)

        # Handle submission
        if should_submit and not is_sample and submitter and submitter.is_configured():
            handle_submission(submitter, tracker, year, day, part_num, result)

        return True, elapsed_time, result

    except Exception as e:
        # Track failed run
        if tracker:
            module_path = Path.cwd() / f"{year}" / f"day{day}.py"
            code_content = module_path.read_text() if module_path.exists() else ""
            tracker.record_run(year, day, part_num, 0, None, input_data,
                             code_content, False, str(e))

        print_part_error(part_num, e)
        return False, 0.0, None


def print_header(title: str) -> None:
    """Print the formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def print_footer(total_time: float) -> None:
    """Print the formatted footer with total time."""
    print("-" * 60)
    if COLOR_SUPPORT:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}⏱️  Total Time: {total_time * 1000:.3f} ms{Style.RESET_ALL}")
    else:
        print(f"Total Time: {total_time * 1000:.3f} ms")
    print("=" * 60 + "\n")


def handle_submission(submitter: AOCSubmitter, tracker: AOCTracker,
                     year: int, day: int, part: int, result: Any) -> None:
    """Handle answer submission to AOC."""
    answer = str(result)

    # Check if we already know this is correct
    correct_answer = tracker.get_correct_answer(year, day, part) if tracker else None
    if correct_answer == answer:
        if COLOR_SUPPORT:
            print(f"  {Fore.GREEN}✅ Already submitted and confirmed correct!{Style.RESET_ALL}")
        else:
            print(f"  Already submitted and confirmed correct!")
        return

    # Check if we can submit (timeout check)
    can_submit, wait_until = tracker.can_submit(year, day, part) if tracker else (True, None)
    if not can_submit:
        if COLOR_SUPPORT:
            print(f"  {Fore.RED}⏳ Cannot submit yet. Wait until: {wait_until.strftime('%H:%M:%S')}{Style.RESET_ALL}")
        else:
            print(f"  Cannot submit yet. Wait until: {wait_until.strftime('%H:%M:%S')}")
        return

    # Check if this exact answer was already submitted
    if tracker and tracker.has_been_submitted(year, day, part, answer):
        if COLOR_SUPPORT:
            print(f"  {Fore.YELLOW}⚠️  This answer was already submitted before{Style.RESET_ALL}")
        else:
            print(f"  This answer was already submitted before")
        return

    # Submit the answer
    if COLOR_SUPPORT:
        print(f"  {Fore.BLUE}🚀 Submitting answer: {answer}...{Style.RESET_ALL}")
    else:
        print(f"  Submitting answer: {answer}...")

    status, message, wait_minutes = submitter.submit_answer(year, day, part, answer)

    # Record submission
    if tracker:
        tracker.record_submission(year, day, part, answer, status, message, wait_minutes)

    # Display result
    if status == 'correct':
        if COLOR_SUPPORT:
            print(f"  {Fore.GREEN}{Style.BRIGHT}🎉 CORRECT! 🎉{Style.RESET_ALL}")
        else:
            print(f"  CORRECT!")
    elif status == 'incorrect':
        if COLOR_SUPPORT:
            print(f"  {Fore.RED}❌ Incorrect answer{Style.RESET_ALL}")
            if wait_minutes > 0:
                print(f"  {Fore.YELLOW}⏰ Wait {wait_minutes} minutes before next submission{Style.RESET_ALL}")
        else:
            print(f"  Incorrect answer")
            if wait_minutes > 0:
                print(f"  Wait {wait_minutes} minutes before next submission")
    elif status == 'timeout':
        if COLOR_SUPPORT:
            print(f"  {Fore.YELLOW}⏳ Too many recent submissions{Style.RESET_ALL}")
        else:
            print(f"  Too many recent submissions")
    else:
        if COLOR_SUPPORT:
            print(f"  {Fore.RED}❌ Submission error: {message}{Style.RESET_ALL}")
        else:
            print(f"  Submission error: {message}")


def show_history(tracker: AOCTracker, year: int, day: int, part: int = None) -> None:
    """Show recent run history for a problem."""
    parts_to_show = [part] if part else [1, 2]

    for p in parts_to_show:
        history = tracker.get_run_history(year, day, p)
        if not history:
            continue

        if COLOR_SUPPORT:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 Recent runs for Part {p}:{Style.RESET_ALL}")
        else:
            print(f"\nRecent runs for Part {p}:")

        for i, run in enumerate(history[:5]):  # Show last 5 runs
            timestamp = datetime.fromisoformat(run['timestamp']).strftime('%H:%M:%S')
            if run['success']:
                status = f"✅ {run['result']}"
                time_info = f"({run['execution_time_ms']:.1f}ms)"
            else:
                status = f"❌ {run['error_message'][:30]}..."
                time_info = ""

            if COLOR_SUPPORT:
                print(f"  {Fore.WHITE}{timestamp} {status} {Fore.BLUE}{time_info}{Style.RESET_ALL}")
            else:
                print(f"  {timestamp} {status} {time_info}")


def format_time(ms: float) -> str:
    """Format time in a human-readable way."""
    if ms < 1:
        return f"{ms:.3f}ms"
    elif ms < 1000:
        return f"{ms:.1f}ms"
    else:
        return f"{ms/1000:.2f}s"


def format_table_for_terminal(headers: list, rows: list) -> str:
    """Format table for nice terminal display."""
    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Create formatted table
    lines = []

    # Header
    header_line = "  ".join(f"{str(headers[i]):<{widths[i]}}" for i in range(len(headers)))
    lines.append(header_line)

    # Separator
    separator = "  ".join("-" * widths[i] for i in range(len(headers)))
    lines.append(separator)

    # Rows
    for row in rows:
        row_line = "  ".join(f"{str(row[i]):<{widths[i]}}" for i in range(len(row)))
        lines.append(row_line)

    return "\n".join(lines)


def generate_stats_table(tracker: AOCTracker, year: int = None, for_readme: bool = False) -> str:
    """Generate statistics table for display."""
    best_times = tracker.get_best_times_by_year(year)
    if not best_times:
        return "No performance data available."

    # Group by year
    years_data = {}
    for entry in best_times:
        y = entry['year']
        if y not in years_data:
            years_data[y] = {}
        day = entry['day']
        if day not in years_data[y]:
            years_data[y][day] = {}
        years_data[y][day][entry['part']] = entry

    output = []

    for year_key in sorted(years_data.keys(), reverse=True):
        year_data = years_data[year_key]
        year_summary = tracker.get_year_summary(year_key)

        output.append(f"\n## {year_key} Statistics")
        output.append(f"\n**Year Summary:**")
        output.append(f"- ⭐ Stars: {year_summary['stars']}")
        output.append(f"- 🧩 Problems Solved: {year_summary['total_solved']}")
        output.append(f"- 🏃 Total Runs: {year_summary['total_runs']} ({year_summary['success_rate']:.1f}% success)")
        output.append(f"- ⚡ Average Time: {format_time(year_summary['average_time_ms'])}")
        output.append(f"- 🚀 Fastest Time: {format_time(year_summary['fastest_time_ms'])}")

        output.append(f"\n**Best Times by Day:**")

        # Prepare table data
        table_rows = []
        for day in sorted(year_data.keys()):
            day_data = year_data[day]
            part1_time = format_time(day_data[1]['best_time_ms']) if 1 in day_data else "—"
            part2_time = format_time(day_data[2]['best_time_ms']) if 2 in day_data else "—"

            total_time = 0
            if 1 in day_data and 2 in day_data:
                total_time = day_data[1]['best_time_ms'] + day_data[2]['best_time_ms']
                total_str = format_time(total_time)
            elif 1 in day_data:
                total_str = part1_time
            elif 2 in day_data:
                total_str = part2_time
            else:
                total_str = "—"

            table_rows.append([day, part1_time, part2_time, total_str])

        if for_readme:
            # Markdown table format
            output.append("")
            output.append("| Day | Part 1 | Part 2 | Total |")
            output.append("|-----|--------|--------|-------|")
            for row in table_rows:
                day, part1, part2, total = row
                output.append(f"| {day:2d} | {part1:>7} | {part2:>7} | {total:>7} |")
        else:
            # Terminal-friendly table format
            output.append("")
            headers = ["Day", "Part 1", "Part 2", "Total"]
            formatted_table = format_table_for_terminal(headers, table_rows)
            output.append(formatted_table)

    return "\n".join(output)


def generate_overall_stats(tracker: AOCTracker) -> str:
    """Generate overall statistics across all years."""
    overall_summary = tracker.get_year_summary()
    available_years = tracker.get_available_years()

    if not available_years:
        return "No tracked data available."

    output = []
    output.append("## 🎄 Overall Statistics")
    output.append("")
    output.append(f"**Summary Across All Years ({min(available_years)}-{max(available_years)}):**")
    output.append(f"- ⭐ Total Stars: {overall_summary['stars']}")
    output.append(f"- 🧩 Total Problems Solved: {overall_summary['total_solved']}")
    output.append(f"- 🏃 Total Runs: {overall_summary['total_runs']} ({overall_summary['success_rate']:.1f}% success)")
    output.append(f"- ⚡ Average Time: {format_time(overall_summary['average_time_ms'])}")
    output.append(f"- 🚀 Fastest Time: {format_time(overall_summary['fastest_time_ms'])}")
    output.append(f"- 🐌 Slowest Time: {format_time(overall_summary['slowest_time_ms'])}")
    output.append("")

    return "\n".join(output)


def show_statistics(tracker: AOCTracker, year: int = None) -> None:
    """Display statistics in the terminal."""
    if COLOR_SUPPORT:
        print(f"{Fore.CYAN}{Style.BRIGHT}📊 Advent of Code Statistics{Style.RESET_ALL}")
    else:
        print("📊 Advent of Code Statistics")
    print("=" * 60)

    if year:
        stats_content = generate_stats_table(tracker, year, for_readme=False)
    else:
        # Show overall stats first
        overall_stats = generate_overall_stats(tracker)
        year_stats = generate_stats_table(tracker, for_readme=False)
        stats_content = overall_stats + "\n" + year_stats

    print(stats_content)
    print("=" * 60)


def sync_completed_problems(submitter: AOCSubmitter, tracker: AOCTracker, year: int) -> None:
    """Sync completed problems from AOC website for the specified year."""
    if COLOR_SUPPORT:
        print(f"{Fore.CYAN}{Style.BRIGHT}🔄 Syncing completed problems for {year}...{Style.RESET_ALL}")
    else:
        print(f"🔄 Syncing completed problems for {year}...")

    print(f"Fetching completion data from adventofcode.com...")

    # Get completed problems from AOC website
    completed_data = submitter.sync_completed_problems(year)

    if not completed_data:
        if COLOR_SUPPORT:
            print(f"{Fore.YELLOW}⚠️  No completed problems found for {year}{Style.RESET_ALL}")
        else:
            print(f"⚠️  No completed problems found for {year}")
        return

    # Show what was found
    total_parts = sum(len(day_data['completed_parts']) for day_data in completed_data.values())
    days_with_answers = sum(1 for day_data in completed_data.values() if day_data['answers'])

    if COLOR_SUPPORT:
        print(f"{Fore.GREEN}📊 Found {total_parts} completed parts across {len(completed_data)} days{Style.RESET_ALL}")
        if days_with_answers > 0:
            print(f"{Fore.BLUE}💡 Found actual answers for {days_with_answers} days{Style.RESET_ALL}")
    else:
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

        if COLOR_SUPPORT:
            print(f"  {Fore.WHITE}Day {day}: {parts_str}{Fore.CYAN}{answers_info}{Style.RESET_ALL}")
        else:
            print(f"  Day {day}: {parts_str}{answers_info}")

    # Sync to database
    new_answers_count = tracker.sync_completed_problems(year, completed_data)

    if COLOR_SUPPORT:
        print(f"\n{Fore.GREEN}✅ Sync completed!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📈 Added {new_answers_count} new correct answers to database{Style.RESET_ALL}")
    else:
        print(f"\n✅ Sync completed!")
        print(f"📈 Added {new_answers_count} new correct answers to database")

    if new_answers_count > 0:
        if COLOR_SUPPORT:
            print(f"{Fore.YELLOW}💡 You can now see these in statistics with --stats{Style.RESET_ALL}")
        else:
            print(f"💡 You can now see these in statistics with --stats")


def update_readme_with_stats(tracker: AOCTracker) -> None:
    """Update README.md with the latest statistics."""
    readme_path = Path.cwd() / "README.md"
    if not readme_path.exists():
        if COLOR_SUPPORT:
            print(f"{Fore.RED}❌ README.md not found{Style.RESET_ALL}")
        else:
            print("❌ README.md not found")
        return

    # Generate stats content
    overall_stats = generate_overall_stats(tracker)
    year_stats = generate_stats_table(tracker, for_readme=True)
    stats_content = overall_stats + "\n" + year_stats

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats_section = f"<!-- STATS_START -->\n{stats_content}\n\n*Last updated: {timestamp}*\n<!-- STATS_END -->"

    # Read current README
    current_content = readme_path.read_text(encoding='utf-8')

    # Replace stats section
    import re
    pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
    if re.search(pattern, current_content, re.DOTALL):
        new_content = re.sub(pattern, stats_section, current_content, flags=re.DOTALL)
    else:
        # If no stats section exists, append it
        new_content = current_content + "\n\n" + stats_section

    # Write updated README
    readme_path.write_text(new_content, encoding='utf-8')

    if COLOR_SUPPORT:
        print(f"{Fore.GREEN}✅ README.md updated with latest statistics{Style.RESET_ALL}")
    else:
        print("✅ README.md updated with latest statistics")


def setup_argument_parser() -> argparse.ArgumentParser:
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
                       help="submit the answer to AOC (only for actual input)")
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
    return parser


def main() -> None:
    """Main entry point for the Advent of Code solution runner."""
    parser = setup_argument_parser()
    args = parser.parse_args()

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

        sync_completed_problems(submitter, tracker, args.sync)
        return

    # Handle stats generation
    if args.stats or args.update_readme:
        if not tracker:
            print("Statistics require tracking to be enabled (remove --no-tracking)")
            return

        if args.stats:
            show_statistics(tracker, args.year_filter)

        if args.update_readme:
            update_readme_with_stats(tracker)

        return

    # Show history if requested
    if args.history:
        if tracker:
            show_history(tracker, args.year, args.day, args.part)
        else:
            print("History requires tracking to be enabled (remove --no-tracking)")
        return

    # Validate required arguments for solution running
    if args.year is None or args.day is None:
        parser.print_help()
        return

    try:
        module = load_solution_module(args.year, args.day)
    except FileNotFoundError as e:
        print(str(e))
        return

    # Get input data
    input_data = get_input_data(args)
    is_sample = args.sample or bool(args.sample_input)

    # Print header
    title = format_title(args.year, args.day, is_sample, args.part)
    print_header(title)

    total_time = 0.0

    # Run Part 1 if requested
    if args.part is None or args.part == 1:
        success, elapsed, result = run_part(module, 1, input_data, args.year, args.day,
                                          tracker, submitter, args.submit, is_sample)
        if success:
            total_time += elapsed

    # Run Part 2 if requested
    if args.part is None or args.part == 2:
        success, elapsed, result = run_part(module, 2, input_data, args.year, args.day,
                                          tracker, submitter, args.submit, is_sample)
        if success:
            total_time += elapsed

    # Print footer with total time
    print_footer(total_time)


if __name__ == "__main__":
    main()
