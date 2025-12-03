import argparse
import importlib.util
from pathlib import Path
from time import perf_counter
from typing import Any, Optional, Tuple
from input import get_input

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


def print_part_result(part_num: int, result: Any, elapsed_time: float) -> None:
    """Print the result for a specific part."""
    if COLOR_SUPPORT:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⭐ Part {part_num}:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Answer: {Style.BRIGHT}{result}{Style.RESET_ALL}")
        print(f"  {Fore.BLUE}Time: {elapsed_time * 1000:.3f} ms{Style.RESET_ALL}")
    else:
        print(f"Part {part_num}:")
        print(f"  Answer: {result}")
        print(f"  Time: {elapsed_time * 1000:.3f} ms")
    print()


def print_part_error(part_num: int, error: Exception) -> None:
    """Print an error for a specific part."""
    if COLOR_SUPPORT:
        print(f"{Fore.RED}❌ Part {part_num} Error: {error}{Style.RESET_ALL}\n")
    else:
        print(f"Part {part_num} Error: {error}\n")


def run_part(module: Any, part_num: int, input_data: str) -> Tuple[bool, float]:
    """Run a specific part of the solution and return success status and elapsed time."""
    try:
        start_time = perf_counter()
        if part_num == 1:
            result = module.solve_part_1(input_data)
        else:
            result = module.solve_part_2(input_data)
        end_time = perf_counter()

        elapsed_time = end_time - start_time
        print_part_result(part_num, result, elapsed_time)
        return True, elapsed_time
    except Exception as e:
        print_part_error(part_num, e)
        return False, 0.0


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


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up and return the command line argument parser."""
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions")
    parser.add_argument("year", type=int, help="the year of the AOC challenge")
    parser.add_argument("day", type=int, help="the day of the AOC challenge")
    parser.add_argument("--sample", "-s", action="store_true",
                       help="use sample input instead of actual input")
    parser.add_argument("--sample-input", type=str,
                       help="provide sample input directly as a string (implies --sample)")
    parser.add_argument("--part", "-p", type=int, choices=[1, 2],
                       help="run only specific part (1 or 2)")
    return parser


def main() -> None:
    """Main entry point for the Advent of Code solution runner."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    try:
        module = load_solution_module(args.year, args.day)
    except FileNotFoundError as e:
        print(str(e))
        return

    # Get input data
    input_data = get_input_data(args)

    # Print header
    title = format_title(args.year, args.day, args.sample or bool(args.sample_input), args.part)
    print_header(title)

    total_time = 0.0

    # Run Part 1 if requested
    if args.part is None or args.part == 1:
        success, elapsed = run_part(module, 1, input_data)
        if success:
            total_time += elapsed

    # Run Part 2 if requested
    if args.part is None or args.part == 2:
        success, elapsed = run_part(module, 2, input_data)
        if success:
            total_time += elapsed

    # Print footer with total time
    print_footer(total_time)


if __name__ == "__main__":
    main()
