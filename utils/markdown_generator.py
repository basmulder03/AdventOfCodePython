"""
Markdown generation utilities for benchmark results and statistics.
"""
from pathlib import Path
from datetime import datetime
from .time_utils import format_time


class MarkdownGenerator:
    """Generates markdown documentation from benchmark and tracking data."""

    def __init__(self, tracker):
        self.tracker = tracker

    def generate_overview_table(self) -> str:
        """Generate a single overview table with all years and their totals."""
        available_years = self.tracker.get_available_years()
        if not available_years:
            return "No tracked data available."

        output = []
        output.append("## 🎄 Solutions Overview")
        output.append("")
        output.append("| Year | Stars ⭐ | Problems 🧩 | Runs 🏃 | Success Rate | Avg Time ⚡ | Fastest 🚀 | Slowest 🐌 |")
        output.append("|------|----------|-------------|---------|--------------|-------------|------------|------------|")

        # Collect data for each year
        for year in sorted(available_years, reverse=True):
            year_summary = self.tracker.get_year_summary(year)

            output.append(
                f"| [{year}](./docs/{year}-results.md) | "
                f"{year_summary['stars']} | "
                f"{year_summary['total_solved']} | "
                f"{year_summary['total_runs']} | "
                f"{year_summary['success_rate']:.1f}% | "
                f"{format_time(year_summary['average_time_ms'])} | "
                f"{format_time(year_summary['fastest_time_ms'])} | "
                f"{format_time(year_summary['slowest_time_ms'])} |"
            )

        output.append("")

        # Add overall totals
        overall_summary = self.tracker.get_year_summary()
        output.append("### Overall Totals")
        output.append(f"- ⭐ **Total Stars**: {overall_summary['stars']}")
        output.append(f"- 🧩 **Total Problems Solved**: {overall_summary['total_solved']}")
        output.append(f"- 🏃 **Total Runs**: {overall_summary['total_runs']} ({overall_summary['success_rate']:.1f}% success)")
        output.append(f"- ⚡ **Average Time**: {format_time(overall_summary['average_time_ms'])}")
        output.append(f"- 🚀 **Fastest Time**: {format_time(overall_summary['fastest_time_ms'])}")
        output.append(f"- 🐌 **Slowest Time**: {format_time(overall_summary['slowest_time_ms'])}")

        return "\n".join(output)

    def generate_year_detailed_stats(self, year: int) -> str:
        """Generate detailed statistics for a specific year."""
        year_summary = self.tracker.get_year_summary(year)
        best_times = self.tracker.get_best_times_by_year(year)

        if not best_times:
            return f"No performance data available for {year}."

        # Group by day
        days_data = {}
        for entry in best_times:
            day = entry['day']
            if day not in days_data:
                days_data[day] = {}
            days_data[day][entry['part']] = entry

        output = []
        output.append(f"# 🎄 Advent of Code {year} Results")
        output.append("")
        output.append(f"[← Back to Overview](../README.md)")
        output.append("")

        # Year Summary
        output.append("## Year Summary")
        output.append("")
        output.append(f"- ⭐ **Stars**: {year_summary['stars']}")
        output.append(f"- 🧩 **Problems Solved**: {year_summary['total_solved']}")
        output.append(f"- 🏃 **Total Runs**: {year_summary['total_runs']} ({year_summary['success_rate']:.1f}% success)")
        output.append(f"- ⚡ **Average Time**: {format_time(year_summary['average_time_ms'])}")
        output.append(f"- 🚀 **Fastest Time**: {format_time(year_summary['fastest_time_ms'])}")
        output.append(f"- 🐌 **Slowest Time**: {format_time(year_summary['slowest_time_ms'])}")
        output.append("")

        # Detailed table
        output.append("## Performance by Day")
        output.append("")
        output.append("| Day | Part 1 | Part 2 | Total | Status |")
        output.append("|-----|--------|--------|-------|--------|")

        for day in sorted(days_data.keys()):
            day_data = days_data[day]

            # Part 1
            if 1 in day_data:
                part1_time = format_time(day_data[1]['best_time_ms'])
                part1_result = str(day_data[1]['result'])[:20]
            else:
                part1_time = "—"
                part1_result = ""

            # Part 2
            if 2 in day_data:
                part2_time = format_time(day_data[2]['best_time_ms'])
                part2_result = str(day_data[2]['result'])[:20]
            else:
                part2_time = "—"
                part2_result = ""

            # Total
            if 1 in day_data and 2 in day_data:
                total_time = day_data[1]['best_time_ms'] + day_data[2]['best_time_ms']
                total_str = format_time(total_time)
                status = "⭐⭐"
            elif 1 in day_data or 2 in day_data:
                total_str = part1_time if 1 in day_data else part2_time
                status = "⭐"
            else:
                total_str = "—"
                status = "—"

            output.append(f"| {day:2d} | {part1_time:>7} | {part2_time:>7} | {total_str:>7} | {status} |")

        output.append("")

        # Performance distribution
        output.append("## Performance Distribution")
        output.append("")
        all_times = [entry['best_time_ms'] for entry in best_times]
        if all_times:
            fast_count = sum(1 for t in all_times if t < 10)  # < 10ms
            medium_count = sum(1 for t in all_times if 10 <= t < 1000)  # 10ms - 1s
            slow_count = sum(1 for t in all_times if t >= 1000)  # >= 1s

            output.append(f"- 🚀 **Fast** (< 10ms): {fast_count} problems")
            output.append(f"- ⚡ **Medium** (10ms - 1s): {medium_count} problems")
            output.append(f"- 🐌 **Slow** (≥ 1s): {slow_count} problems")

        output.append("")
        output.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(output)

    def generate_day_detailed_stats(self, year: int, day: int) -> str:
        """Generate detailed statistics for a specific day."""
        # Get all runs for this day
        history = self.tracker.get_recent_runs(year, day, part=None, limit=100)

        if not history:
            return f"No run history found for {year} Day {day}."

        output = []
        output.append(f"# 🎄 Advent of Code {year} - Day {day}")
        output.append("")
        output.append(f"[← Back to {year} Results](../docs/{year}-results.md)")
        output.append("")

        # Get best times for each part
        best_times = {}
        part_results = {}
        for run in history:
            part = run['part']
            if run['success']:
                if part not in best_times or run['execution_time_ms'] < best_times[part]:
                    best_times[part] = run['execution_time_ms']
                    part_results[part] = run['result']

        # Summary
        output.append("## Summary")
        output.append("")
        for part in sorted(best_times.keys()):
            output.append(f"### Part {part}")
            output.append(f"- ⚡ **Best Time**: {format_time(best_times[part])}")
            output.append(f"- ✅ **Result**: `{part_results[part]}`")
            output.append("")

        # Run History
        output.append("## Run History")
        output.append("")
        output.append("| Timestamp | Part | Status | Time | Result |")
        output.append("|-----------|------|--------|------|--------|")

        for run in history[:50]:  # Show last 50 runs
            timestamp = run['timestamp']
            part = run['part']
            status = "✅" if run['success'] else "❌"
            time_str = format_time(run['execution_time_ms']) if run['success'] else "—"
            result = str(run['result'])[:30] if run['success'] else run.get('error_message', 'Error')[:30]

            output.append(f"| {timestamp} | {part} | {status} | {time_str} | {result} |")

        output.append("")
        output.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(output)

    def update_main_readme(self) -> bool:
        """Update the main README.md with overview table."""
        readme_path = Path.cwd() / "README.md"
        if not readme_path.exists():
            print("❌ README.md not found")
            return False

        # Generate overview content
        overview = self.generate_overview_table()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats_section = f"<!-- STATS_START -->\n{overview}\n\n*Last updated: {timestamp}*\n<!-- STATS_END -->"

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
        print(f"✅ Updated README.md with overview table")
        return True

    def update_year_readme(self, year: int) -> bool:
        """Create or update year-specific results file."""
        docs_path = Path.cwd() / "docs"
        docs_path.mkdir(exist_ok=True)

        year_readme_path = docs_path / f"{year}-results.md"

        # Generate detailed year stats
        content = self.generate_year_detailed_stats(year)

        # Write to file
        year_readme_path.write_text(content, encoding='utf-8')
        print(f"✅ Updated {year_readme_path}")
        return True

    def update_day_readme(self, year: int, day: int) -> bool:
        """Create or update day-specific results file."""
        year_path = Path.cwd() / str(year)
        year_path.mkdir(exist_ok=True)

        day_readme_path = year_path / f"day{day}-results.md"

        # Generate detailed day stats
        content = self.generate_day_detailed_stats(year, day)

        # Write to file
        day_readme_path.write_text(content, encoding='utf-8')
        print(f"✅ Updated {day_readme_path}")
        return True

    def update_all_readmes(self) -> bool:
        """Update all README files (main + all years)."""
        print("📝 Updating all README files...")

        # Update main README
        self.update_main_readme()

        # Update each year
        available_years = self.tracker.get_available_years()
        for year in available_years:
            self.update_year_readme(year)

        print(f"✅ Updated README.md and {len(available_years)} year files")
        return True

