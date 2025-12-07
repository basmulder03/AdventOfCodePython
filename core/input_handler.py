"""
Input handling functionality for Advent of Code solutions.
"""
import os
import requests
from datetime import datetime, timezone
from .year_config import get_max_day


def is_input_available(year: int, day: int) -> bool:
    """Check if input is available for the given year and day.

    Input becomes available at 5 AM UTC on each day in December.
    """
    # Check for valid AOC date range
    max_day = get_max_day(year)
    if not (1 <= day <= max_day) or year < 2015:
        return False

    try:
        # Puzzle releases at 5 AM UTC
        puzzle_release_utc = datetime(year, 12, day, 5, 0, tzinfo=timezone.utc)
        current_time_utc = datetime.now(timezone.utc)

        return current_time_utc >= puzzle_release_utc
    except ValueError:
        return False


class InputHandler:
    """Handles input downloading and caching for Advent of Code."""

    def __init__(self, cookie_filename: str = "session_cookie.txt"):
        self.cookie_filename = cookie_filename

    def get_input(self, year: int, day: int, sample: bool = False) -> str:
        """Get input data for the specified year and day.

        Args:
            year: The AOC year
            day: The AOC day
            sample: Whether to get sample input instead of actual input

        Returns:
            The input data as a string
        """
        if sample:
            filename = f"input/{year}/day{day}_sample.txt"
        else:
            filename = f"input/{year}/day{day}.txt"

        if os.path.exists(filename):
            # Read the input data from the file
            with open(filename, "r") as f:
                return f.read()
        elif sample:
            # Create sample file if it doesn't exist
            self._ensure_directory_exists(filename)

            # Create empty sample file
            with open(filename, "w") as f:
                f.write("")

            print(f"Created empty sample input file: {filename}")
            print("Please add your sample input to this file and run again.")
            return ""
        else:
            # Download actual input from AOC website
            return self._download_input(year, day, filename)

    def _ensure_directory_exists(self, filename: str) -> None:
        """Ensure the directory structure exists for the given filename."""
        current_dir = os.getcwd()
        for dir in filename.split("/")[:-1]:
            if not dir in os.listdir(current_dir):
                os.makedirs(os.path.join(current_dir, dir))
            current_dir = os.path.join(current_dir, dir)

    def _download_input(self, year: int, day: int, filename: str) -> str:
        """Download input from the AOC website."""
        session_cookie = self._get_session_cookie()

        # Create a session and authenticate with the AOC website
        session = requests.Session()
        session.cookies.update({"session": session_cookie})
        # Set a proper user agent with GitHub repo to make Eric happy
        session.headers.update({
            "User-Agent": "https://github.com/basmulder03/AdventOfCodePython"
        })

        response = session.get(f"https://adventofcode.com/{year}/day/{day}/input")

        if response.status_code == 403:
            # The cookie is no longer valid, prompt the user for a new one
            new_cookie = input(
                "Your session cookie is no longer valid. Please enter a new one: ")
            session.cookies.update({"session": new_cookie})
            # Ensure user agent is still set for retry request
            session.headers.update({
                "User-Agent": "https://github.com/basmulder03/AdventOfCodePython"
            })
            response = session.get(f"https://adventofcode.com/{year}/day/{day}/input")
            # Save the new cookie to the file
            with open(self.cookie_filename, "w+") as f:
                f.write(new_cookie)

        response.raise_for_status()
        input_data = response.text

        self._ensure_directory_exists(filename)

        # Write the input data to the file
        with open(filename, "w+") as f:
            f.write(input_data)

        return input_data

    def _get_session_cookie(self) -> str:
        """Get the session cookie from file or prompt user."""
        if os.path.exists(self.cookie_filename):
            with open(self.cookie_filename, "r") as f:
                return f.read().strip()
        else:
            session_cookie = input("Please enter your session cookie: ")
            with open(self.cookie_filename, "w+") as f:
                f.write(session_cookie)
            return session_cookie


# Backward compatibility functions
_default_handler = InputHandler()

def get_input(year: int, day: int, sample: bool = False) -> str:
    """Backward compatibility function for getting input."""
    return _default_handler.get_input(year, day, sample)
