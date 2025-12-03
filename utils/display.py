"""
Display formatting utilities for console output.
"""
from typing import Optional, Any

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


class DisplayFormatter:
    """Handles console output formatting and styling."""

    def __init__(self):
        self.color_support = COLOR_SUPPORT

    def format_title(self, year: int, day: int, is_sample: bool, part: Optional[int]) -> str:
        """Format the title with appropriate styling."""
        if self.color_support:
            title = f"🎄 Advent of Code {year} - Day {day} 🎄"
            if is_sample:
                title += f" {Fore.YELLOW}(Sample Input){Style.RESET_ALL}"
            if part is not None:
                title += f" {Fore.CYAN}- Part {part}{Style.RESET_ALL}"
        else:
            title = f"🎄 Advent of Code {year} - Day {day} 🎄"
            if is_sample:
                title += " (Sample Input)"
            if part is not None:
                title += f" - Part {part}"
        return title

    def print_part_result(self, part_num: int, result: Any, elapsed_time: float,
                         tracker=None, year: int = None, day: int = None, code_content: str = "") -> None:
        """Print the result of running a part."""
        if self.color_support:
            part_header = f"{Fore.CYAN}{Style.BRIGHT}Part {part_num}:{Style.RESET_ALL}"
            result_text = f"{Fore.GREEN}{Style.BRIGHT}{result}{Style.RESET_ALL}"
            time_text = f"{Fore.YELLOW}{elapsed_time * 1000:.2f}ms{Style.RESET_ALL}"
        else:
            part_header = f"Part {part_num}:"
            result_text = str(result)
            time_text = f"{elapsed_time * 1000:.2f}ms"

        print(f"{part_header} {result_text} ({time_text})")

        # Show performance comparison if tracking is enabled
        if tracker and year and day:
            comparison = tracker.get_performance_comparison(year, day, part_num, elapsed_time * 1000, code_content)
            if comparison:
                if self.color_support:
                    if comparison['is_best']:
                        perf_text = f"{Fore.GREEN}🏆 New best time!{Style.RESET_ALL}"
                    elif comparison['percentile'] <= 25:
                        perf_text = f"{Fore.GREEN}⭐ Top 25% performance{Style.RESET_ALL}"
                    elif comparison['percentile'] <= 50:
                        perf_text = f"{Fore.BLUE}👍 Above average performance{Style.RESET_ALL}"
                    else:
                        perf_text = f"{Fore.YELLOW}📊 Below average performance{Style.RESET_ALL}"
                else:
                    if comparison['is_best']:
                        perf_text = "🏆 New best time!"
                    elif comparison['percentile'] <= 25:
                        perf_text = "⭐ Top 25% performance"
                    elif comparison['percentile'] <= 50:
                        perf_text = "👍 Above average performance"
                    else:
                        perf_text = "📊 Below average performance"

                avg_time_text = f"{comparison['avg_time']:.2f}ms"
                best_time_text = f"{comparison['best_time']:.2f}ms"

                print(f"    {perf_text}")
                print(f"    Average: {avg_time_text}, Best: {best_time_text} (from {comparison['run_count']} runs)")

    def print_part_error(self, part_num: int, error: Exception) -> None:
        """Print an error that occurred while running a part."""
        if self.color_support:
            error_header = f"{Fore.RED}{Style.BRIGHT}Part {part_num} Error:{Style.RESET_ALL}"
            error_text = f"{Fore.RED}{str(error)}{Style.RESET_ALL}"
        else:
            error_header = f"Part {part_num} Error:"
            error_text = str(error)

        print(f"{error_header} {error_text}")

    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        separator = "=" * max(len(title), 60)
        print(separator)
        print(title.center(len(separator)))
        print(separator)

    def print_footer(self, total_time: float) -> None:
        """Print a formatted footer with total execution time."""
        if self.color_support:
            time_text = f"{Fore.MAGENTA}{Style.BRIGHT}Total time: {total_time * 1000:.2f}ms{Style.RESET_ALL}"
        else:
            time_text = f"Total time: {total_time * 1000:.2f}ms"

        print("=" * 60)
        print(time_text.center(60))
        print("=" * 60)

    def format_table_for_terminal(self, headers: list, rows: list) -> str:
        """Format table data for terminal display."""
        if not rows:
            return "No data available."

        # Calculate column widths
        col_widths = [len(str(header)) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Format header
        header_line = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
        separator = "-+-".join("-" * width for width in col_widths)

        # Format rows
        formatted_rows = []
        for row in rows:
            formatted_row = " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
            formatted_rows.append(formatted_row)

        # Combine all parts
        table_lines = [header_line, separator] + formatted_rows
        return "\n".join(table_lines)
