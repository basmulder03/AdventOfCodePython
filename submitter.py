"""
Advent of Code submission handler.
"""
import re
import requests
from pathlib import Path
from typing import List, Tuple

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

    def get_completed_parts(self, year: int, day: int) -> Tuple[List[int], dict]:
        """
        Get which parts are completed for a given day and extract answers if possible.

        Returns:
            Tuple of (completed_parts, answers)
            completed_parts: List of part numbers (1, 2) that are completed
            answers: Dict with part numbers as keys and answers as values (if found in page)
        """
        url = f"https://adventofcode.com/{year}/day/{day}"

        try:
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            completed_parts = []
            answers = {}

            # Look for completed stars - they show as gold stars in the page
            # The page structure shows stars for completed parts
            main_content = soup.find('main')
            if not main_content:
                return completed_parts, answers

            # Find all star indicators - these are typically shown as ⭐ or in class names
            article_elements = main_content.find_all('article', class_='day-desc')

            # Check for completed parts by looking for answer submission responses
            # These appear as paragraphs with specific text patterns
            response_paras = main_content.find_all('p')

            for para in response_paras:
                text = para.get_text()
                # Look for success messages that indicate completion
                if "Your puzzle answer was" in text:
                    # Extract the answer from the text
                    # Format is usually "Your puzzle answer was [answer]."
                    match = re.search(r'Your puzzle answer was (.+?)\.', text)
                    if match:
                        answer = match.group(1).strip()

                        # Determine which part this is for
                        # Usually part 2 answers appear after part 1
                        if len(answers) == 0:
                            completed_parts.append(1)
                            answers[1] = answer
                        elif 1 in answers and len(answers) == 1:
                            completed_parts.append(2)
                            answers[2] = answer

            # Alternative: Look for stars in the page title or headers
            h2_elements = main_content.find_all('h2')
            for h2 in h2_elements:
                text = h2.get_text()
                if '⭐' in text or '*' in text:
                    # Count stars to determine completed parts
                    star_count = text.count('⭐') + text.count('*')
                    for i in range(1, min(3, star_count + 1)):
                        if i not in completed_parts:
                            completed_parts.append(i)

            return sorted(completed_parts), answers

        except requests.RequestException as e:
            print(f"Network error fetching problem page: {e}")
            return [], {}
        except Exception as e:
            print(f"Error parsing problem page: {e}")
            return [], {}

    def sync_completed_problems(self, year: int, start_day: int = 1, end_day: int = 25) -> dict:
        """
        Sync completed problems for a given year.

        Returns:
            Dict with day numbers as keys and completion info as values
        """
        sync_results = {}

        for day in range(start_day, end_day + 1):
            completed_parts, answers = self.get_completed_parts(year, day)
            if completed_parts:
                sync_results[day] = {
                    'completed_parts': completed_parts,
                    'answers': answers
                }

        return sync_results

