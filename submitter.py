"""
Advent of Code submission handler.
"""
import re
import requests
from pathlib import Path
from typing import Tuple

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup4 is required. Install with: pip install beautifulsoup4")
    raise


class AOCSubmitter:
    """Handles submissions to Advent of Code website."""

    def __init__(self, session_cookie: str = None):
        self.session = requests.Session()
        if session_cookie:
            self.session.cookies.set('session', session_cookie, domain='.adventofcode.com')
        else:
            self._load_session_cookie()

    def _load_session_cookie(self) -> None:
        """Load session cookie from file."""
        cookie_file = Path.cwd() / "session_cookie.txt"
        if cookie_file.exists():
            cookie = cookie_file.read_text().strip()
            self.session.cookies.set('session', cookie, domain='.adventofcode.com')

    def submit_answer(self, year: int, day: int, part: int, answer: str) -> Tuple[str, str, int]:
        """
        Submit an answer to AOC.

        Returns:
            Tuple of (status, message, wait_minutes)
            status: 'correct', 'incorrect', 'timeout', 'error'
            message: Response message from AOC
            wait_minutes: Minutes to wait before next submission (0 if no wait)
        """
        url = f"https://adventofcode.com/{year}/day/{day}/answer"
        data = {
            'level': str(part),
            'answer': str(answer)
        }

        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            main_content = soup.find('main')

            if not main_content:
                return 'error', 'Could not parse response', 0

            message = main_content.get_text().strip()

            # Parse response
            if "That's the right answer" in message:
                return 'correct', message, 0
            elif "That's not the right answer" in message:
                # Extract wait time if present
                wait_match = re.search(r'please wait (?:(\d+)m )?(\d+)s', message)
                if wait_match:
                    minutes = int(wait_match.group(1) or 0)
                    seconds = int(wait_match.group(2) or 0)
                    total_minutes = minutes + (seconds / 60)
                    return 'incorrect', message, int(total_minutes) + 1
                else:
                    return 'incorrect', message, 1  # Default 1 minute wait
            elif "You gave an answer too recently" in message:
                # Extract wait time
                wait_match = re.search(r'You have (?:(\d+)m )?(\d+)s left to wait', message)
                if wait_match:
                    minutes = int(wait_match.group(1) or 0)
                    seconds = int(wait_match.group(2) or 0)
                    total_minutes = minutes + (seconds / 60)
                    return 'timeout', message, int(total_minutes) + 1
                else:
                    return 'timeout', message, 5  # Default 5 minute wait
            else:
                return 'error', message, 0

        except requests.RequestException as e:
            return 'error', f'Network error: {str(e)}', 0
        except Exception as e:
            return 'error', f'Unexpected error: {str(e)}', 0

    def is_configured(self) -> bool:
        """Check if session cookie is configured."""
        return 'session' in self.session.cookies

