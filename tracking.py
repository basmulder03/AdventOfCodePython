"""
Run tracking and submission management for Advent of Code solutions.
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib


class AOCTracker:
    """Tracks runs, submissions, and performance for Advent of Code solutions."""

    def __init__(self, db_path: Path = None):
        if db_path is None:
            db_path = Path.cwd() / "aoc_tracking.db"
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Runs table - tracks each execution
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    part INTEGER NOT NULL,
                    timestamp DATETIME NOT NULL,
                    execution_time_ms REAL NOT NULL,
                    result TEXT,
                    input_hash TEXT NOT NULL,
                    code_hash TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT
                )
            """)

            # Submissions table - tracks AOC submissions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    part INTEGER NOT NULL,
                    timestamp DATETIME NOT NULL,
                    answer TEXT NOT NULL,
                    status TEXT NOT NULL,  -- 'correct', 'incorrect', 'timeout', 'error'
                    response_message TEXT,
                    wait_until DATETIME,  -- when we can submit again after wrong answer
                    UNIQUE(year, day, part, answer)
                )
            """)

            # Correct answers table - stores known correct answers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS correct_answers (
                    year INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    part INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    PRIMARY KEY (year, day, part)
                )
            """)

            conn.commit()

    def _hash_content(self, content: str) -> str:
        """Create a hash of content for tracking changes."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def record_run(self, year: int, day: int, part: int, execution_time: float,
                   result: Any, input_data: str, code_content: str,
                   success: bool, error_message: str = None) -> int:
        """Record a solution run in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            input_hash = self._hash_content(input_data)
            code_hash = self._hash_content(code_content)

            cursor.execute("""
                INSERT INTO runs (year, day, part, timestamp, execution_time_ms, 
                                result, input_hash, code_hash, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (year, day, part, datetime.now(), execution_time * 1000,
                  str(result) if result is not None else None, input_hash,
                  code_hash, success, error_message))

            return cursor.lastrowid

    def get_performance_comparison(self, year: int, day: int, part: int,
                                 current_time: float, code_content: str) -> Optional[Dict]:
        """Get performance comparison with previous runs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            code_hash = self._hash_content(code_content)

            # Get best time for this solution
            cursor.execute("""
                SELECT MIN(execution_time_ms), COUNT(*) 
                FROM runs 
                WHERE year = ? AND day = ? AND part = ? AND success = 1
            """, (year, day, part))

            best_result = cursor.fetchone()
            if not best_result or best_result[0] is None:
                return None

            best_time, total_runs = best_result
            current_time_ms = current_time * 1000

            # Get previous run with same code
            cursor.execute("""
                SELECT execution_time_ms 
                FROM runs 
                WHERE year = ? AND day = ? AND part = ? AND code_hash = ? AND success = 1
                ORDER BY timestamp DESC 
                LIMIT 1 OFFSET 1
            """, (year, day, part, code_hash))

            prev_result = cursor.fetchone()
            prev_time = prev_result[0] if prev_result else None

            return {
                'current_time': current_time_ms,
                'best_time': best_time,
                'previous_time': prev_time,
                'total_runs': total_runs,
                'improvement_vs_best': ((best_time - current_time_ms) / best_time * 100) if best_time > 0 else 0,
                'improvement_vs_prev': ((prev_time - current_time_ms) / prev_time * 100) if prev_time else None
            }

    def can_submit(self, year: int, day: int, part: int) -> Tuple[bool, Optional[datetime]]:
        """Check if we can submit for this problem (respects timeout after wrong answers)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT wait_until FROM submissions 
                WHERE year = ? AND day = ? AND part = ? AND wait_until > ?
                ORDER BY timestamp DESC LIMIT 1
            """, (year, day, part, datetime.now()))

            result = cursor.fetchone()
            if result:
                return False, datetime.fromisoformat(result[0])
            return True, None

    def record_submission(self, year: int, day: int, part: int, answer: str,
                         status: str, response_message: str = None,
                         wait_minutes: int = None) -> None:
        """Record a submission attempt."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            wait_until = None
            if wait_minutes and status == 'incorrect':
                wait_until = datetime.now() + timedelta(minutes=wait_minutes)

            cursor.execute("""
                INSERT OR REPLACE INTO submissions 
                (year, day, part, timestamp, answer, status, response_message, wait_until)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (year, day, part, datetime.now(), answer, status, response_message, wait_until))

            # If correct, store as correct answer
            if status == 'correct':
                cursor.execute("""
                    INSERT OR REPLACE INTO correct_answers (year, day, part, answer)
                    VALUES (?, ?, ?, ?)
                """, (year, day, part, answer))

            conn.commit()

    def get_correct_answer(self, year: int, day: int, part: int) -> Optional[str]:
        """Get the known correct answer for this problem."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT answer FROM correct_answers 
                WHERE year = ? AND day = ? AND part = ?
            """, (year, day, part))

            result = cursor.fetchone()
            return result[0] if result else None

    def has_been_submitted(self, year: int, day: int, part: int, answer: str) -> bool:
        """Check if this exact answer has been submitted before."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM submissions 
                WHERE year = ? AND day = ? AND part = ? AND answer = ?
            """, (year, day, part, answer))

            return cursor.fetchone() is not None

    def get_run_history(self, year: int, day: int, part: int, limit: int = 10) -> List[Dict]:
        """Get recent run history for a problem."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, execution_time_ms, result, success, error_message
                FROM runs 
                WHERE year = ? AND day = ? AND part = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (year, day, part, limit))

            return [
                {
                    'timestamp': row[0],
                    'execution_time_ms': row[1],
                    'result': row[2],
                    'success': bool(row[3]),
                    'error_message': row[4]
                }
                for row in cursor.fetchall()
            ]

