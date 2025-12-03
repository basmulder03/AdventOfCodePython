import os
import requests
from datetime import datetime, timezone, timedelta


def is_input_available(year: int, day: int) -> bool:
    """Check if input is available for the given year and day.
    
    Input becomes available at 5 AM UTC on each day in December.
    """
    # Puzzle releases at 5 AM UTC
    puzzle_release_utc = datetime(year, 12, day, 5, 0, tzinfo=timezone.utc)
    current_time_utc = datetime.now(timezone.utc)
    
    return current_time_utc >= puzzle_release_utc


def get_input(year: int, day: int, sample: bool = False) -> str:
    if sample:
        filename = f"input/{year}/day{day}_sample.txt"
    else:
        filename = f"input/{year}/day{day}.txt"
    cookie_filename = "session_cookie.txt"
    if os.path.exists(filename):
        # Read the input data from the file
        with open(filename, "r") as f:
            return f.read()
    elif sample:
        # Create sample file if it doesn't exist
        current_dir = os.getcwd()
        for dir in filename.split("/")[:-1]:
            if not dir in os.listdir(current_dir):
                os.makedirs(os.path.join(current_dir, dir))
            current_dir = os.path.join(current_dir, dir)

        # Create empty sample file
        with open(filename, "w") as f:
            f.write("")

        print(f"Created empty sample input file: {filename}")
        print("Please add your sample input to this file and run again.")
        return ""
    else:
        # Read the session cookie from the file or prompt the user for a new one
        if os.path.exists(cookie_filename):
            with open(cookie_filename, "r") as f:
                session_cookie = f.read()
        else:
            session_cookie = input("Please enter your session cookie: ")
            with open(cookie_filename, "w+") as f:
                f.write(session_cookie)

        # Create a session and authenticate with the AOC website
        session = requests.Session()
        session.cookies.update({
            "session": session_cookie
        })
        # Set a proper user agent with GitHub repo to make Eric happy
        session.headers.update({
            "User-Agent": "https://github.com/basmulder03/AdventOfCodePython"
        })
        response = session.get(
            f"https://adventofcode.com/{year}/day/{day}/input")
        if response.status_code == 403:
            # The cookie is no longer valid, prompt the user for a new one
            new_cookie = input(
                "Your session cookie is no longer valid. Please enter a new one: ")
            session.cookies.update({
                "session": new_cookie
            })
            # Ensure user agent is still set for retry request
            session.headers.update({
                "User-Agent": "https://github.com/basmulder03/AdventOfCodePython"
            })
            response = session.get(
                f"https://adventofcode.com/{year}/day/{day}/input")
            # Save the new cookie to the file
            with open(cookie_filename, "w+") as f:
                f.write(new_cookie)
        response.raise_for_status()
        input_data = response.text

        current_dir = os.getcwd()
        for dir in filename.split("/")[:-1]:
            print(dir, current_dir)

            if not dir in os.listdir(current_dir):
                os.makedirs(os.path.join(current_dir, dir))
            current_dir = os.path.join(current_dir, dir)

        # Write the input data to the file
        with open(filename, "w+") as f:
            f.write(input_data)

        return input_data
