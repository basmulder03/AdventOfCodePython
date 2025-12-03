"""
Solution loading and template creation functionality.
"""
import importlib.util
from pathlib import Path
from typing import Any
from .input_handler import InputHandler, is_input_available


class SolutionLoader:
    """Handles loading and creating AOC solution modules."""

    def __init__(self):
        self.input_handler = InputHandler()

    def get_available_parts(self, module: Any) -> list[int]:
        """Get list of available parts (1, 2) in a solution module."""
        available_parts = []
        for part in [1, 2]:
            if hasattr(module, f"solve_part_{part}"):
                available_parts.append(part)
        return available_parts

    def load_solution_module(self, year: int, day: int) -> Any:
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
            self.create_solution_file(year, day)
            raise FileNotFoundError(f"Solution file created at {module_path}. Please implement the functions.")

    def create_solution_file(self, year: int, day: int) -> None:
        """Create a template solution file for the given year and day."""
        year_dir = Path.cwd() / str(year)
        year_dir.mkdir(exist_ok=True)

        solution_file = year_dir / f"day{day}.py"
        if not solution_file.exists():
            template = (
                "from typing import Any\n\n\n"
                "def solve_part_1(input_data: str) -> Any:\n"
                "    \"\"\"Solve part 1 of the challenge.\"\"\"\n"
                "    pass\n"
            )

            # Day 25 traditionally only has one part in Advent of Code
            if day != 25:
                template += (
                    "\n\n"
                    "def solve_part_2(input_data: str) -> Any:\n"
                    "    \"\"\"Solve part 2 of the challenge.\"\"\"\n"
                    "    pass\n"
                )
            else:
                template += (
                    "\n\n"
                    "# Note: Day 25 traditionally only has one part in Advent of Code\n"
                    "# You get the second star for free after completing all other days!\n"
                )

            solution_file.write_text(template)

            # Attempt to download input if available
            if is_input_available(year, day):
                try:
                    print(f"Input is available for {year} day {day}. Downloading...")
                    self.input_handler.get_input(year, day, sample=False)
                    print(f"✓ Input downloaded for {year} day {day}")
                except Exception as e:
                    print(f"⚠ Failed to download input for {year} day {day}: {e}")
                    print("You can download it manually later by running the solution.")
            else:
                print(f"Input not yet available for {year} day {day}. It will be available at 5 AM UTC (6 AM local time).")
                print("Run the solution again after the input becomes available to download it automatically.")


# Backward compatibility
_default_loader = SolutionLoader()

def load_solution_module(year: int, day: int) -> Any:
    """Backward compatibility function for loading solution modules."""
    return _default_loader.load_solution_module(year, day)

def create_solution_file(year: int, day: int) -> None:
    """Backward compatibility function for creating solution files."""
    return _default_loader.create_solution_file(year, day)
