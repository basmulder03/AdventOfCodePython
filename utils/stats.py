"""
Statistics generation utilities.
"""
from typing import Optional
from .time_utils import format_time


class StatsGenerator:
    """Generates formatted statistics from tracker data."""

    def __init__(self, tracker):
        self.tracker = tracker

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

    def generate_stats_table(self, year: int = None, for_readme: bool = False) -> str:
        """Generate statistics table for display."""
        best_times = self.tracker.get_best_times_by_year(year)
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
            year_summary = self.tracker.get_year_summary(year_key)

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
                formatted_table = self.format_table_for_terminal(headers, table_rows)
                output.append(formatted_table)

        return "\n".join(output)

    def generate_overall_stats(self) -> str:
        """Generate overall statistics across all years."""
        overall_summary = self.tracker.get_year_summary()
        available_years = self.tracker.get_available_years()

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
