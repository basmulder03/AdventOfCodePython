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
                    error_message TEXT,
                    is_sample BOOLEAN NOT NULL DEFAULT 0
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

            # Migration: Add is_sample column if it doesn't exist
            cursor.execute("PRAGMA table_info(runs)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'is_sample' not in columns:
                cursor.execute("ALTER TABLE runs ADD COLUMN is_sample BOOLEAN NOT NULL DEFAULT 0")

            conn.commit()

    def _hash_content(self, content: str) -> str:
        """Create a hash of content for tracking changes."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def record_run(self, year: int, day: int, part: int, execution_time: float,
                   result: Any, input_data: str, code_content: str,
                   success: bool, error_message: str = None, is_sample: bool = False) -> int:
        """Record a solution run in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            input_hash = self._hash_content(input_data)
            code_hash = self._hash_content(code_content)

            cursor.execute("""
                INSERT INTO runs (year, day, part, timestamp, execution_time_ms, 
                                result, input_hash, code_hash, success, error_message, is_sample)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (year, day, part, datetime.now(), execution_time * 1000,
                  str(result) if result is not None else None, input_hash,
                  code_hash, success, error_message, is_sample))

            return cursor.lastrowid

    def get_performance_comparison(self, year: int, day: int, part: int,
                                 current_time: float, code_content: str) -> Optional[Dict]:
        """Get performance comparison with previous runs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            code_hash = self._hash_content(code_content)

            # Get statistics for this problem (excluding sample runs)
            cursor.execute("""
                SELECT MIN(execution_time_ms), AVG(execution_time_ms), COUNT(*) 
                FROM runs 
                WHERE year = ? AND day = ? AND part = ? AND success = 1 AND is_sample = 0
            """, (year, day, part))

            stats_result = cursor.fetchone()
            if not stats_result or stats_result[0] is None:
                return None

            best_time, avg_time, run_count = stats_result

            # Check if current time is the best
            is_best = current_time <= best_time

            # Calculate percentile (how many runs were slower than current)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM runs 
                WHERE year = ? AND day = ? AND part = ? AND success = 1 AND is_sample = 0 AND execution_time_ms > ?
            """, (year, day, part, current_time))

            slower_count = cursor.fetchone()[0]
            percentile = (slower_count / run_count * 100) if run_count > 0 else 0

            return {
                'is_best': is_best,
                'percentile': percentile,
                'avg_time': avg_time,
                'best_time': best_time,
                'run_count': run_count
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
                
                # Update previous runs with the same result to be marked as successful
                cursor.execute("""
                    UPDATE runs 
                    SET success = 1 
                    WHERE year = ? AND day = ? AND part = ? AND result = ? AND success = 0
                """, (year, day, part, answer))
            
            # If incorrect, mark runs with the same result as unsuccessful
            elif status == 'incorrect':
                cursor.execute("""
                    UPDATE runs 
                    SET success = 0 
                    WHERE year = ? AND day = ? AND part = ? AND result = ?
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
        """Get recent run history for a problem (excluding sample runs)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, execution_time_ms, result, success, error_message
                FROM runs 
                WHERE year = ? AND day = ? AND part = ? AND is_sample = 0
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

    def get_best_times_by_year(self, year: int = None) -> List[Dict]:
        """Get best execution times for each day/part, optionally filtered by year."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            where_clause = "WHERE success = 1 AND is_sample = 0"
            params = []
            if year:
                where_clause += " AND year = ?"
                params.append(year)

            cursor.execute(f"""
                WITH best_runs AS (
                    SELECT 
                        year, day, part,
                        MIN(execution_time_ms) as best_time_ms
                    FROM runs 
                    {where_clause}
                    GROUP BY year, day, part
                )
                SELECT 
                    br.year, br.day, br.part,
                    br.best_time_ms,
                    COUNT(r.id) as total_runs,
                    r.result,
                    r.timestamp as best_run_timestamp
                FROM best_runs br
                JOIN runs r ON (
                    r.year = br.year AND 
                    r.day = br.day AND 
                    r.part = br.part AND 
                    r.execution_time_ms = br.best_time_ms AND
                    r.success = 1
                )
                LEFT JOIN runs r2 ON (
                    r2.year = br.year AND 
                    r2.day = br.day AND 
                    r2.part = br.part AND 
                    r2.success = 1
                )
                GROUP BY br.year, br.day, br.part, r.result, r.timestamp
                ORDER BY br.year DESC, br.day ASC, br.part ASC
            """, params)

            return [
                {
                    'year': row[0],
                    'day': row[1],
                    'part': row[2],
                    'best_time_ms': row[3],
                    'total_runs': row[4],
                    'result': row[5],
                    'best_run_timestamp': row[6]
                }
                for row in cursor.fetchall()
            ]

    def get_year_summary(self, year: int = None) -> Dict:
        """Get summary statistics for a year or all years."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            where_clause = ""
            params = []
            if year:
                where_clause = "WHERE year = ?"
                params.append(year)

            # Total problems solved
            additional_where = " AND success = 1"
            if where_clause:
                full_where = where_clause + additional_where
            else:
                full_where = "WHERE success = 1"

            cursor.execute(f"""
                SELECT COUNT(DISTINCT year || '-' || day || '-' || part)
                FROM runs 
                {full_where}
            """, params)
            total_solved = cursor.fetchone()[0]

            # Total runs
            cursor.execute(f"""
                SELECT COUNT(*), SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END)
                FROM runs 
                {where_clause if where_clause else ""}
            """, params)
            total_runs, successful_runs = cursor.fetchone()

            # Best times
            success_where = " AND success = 1"
            if where_clause:
                times_where = where_clause + success_where
            else:
                times_where = "WHERE success = 1"

            cursor.execute(f"""
                SELECT 
                    MIN(execution_time_ms) as fastest,
                    MAX(execution_time_ms) as slowest,
                    AVG(execution_time_ms) as average
                FROM runs 
                {times_where}
            """, params)
            times = cursor.fetchone()

            # Stars (correct submissions)
            cursor.execute(f"""
                SELECT COUNT(*) FROM correct_answers
                {where_clause if where_clause else ""}
            """, params)
            stars = cursor.fetchone()[0]

            return {
                'total_solved': total_solved,
                'total_runs': total_runs,
                'successful_runs': successful_runs,
                'success_rate': (successful_runs / total_runs * 100) if total_runs > 0 else 0,
                'fastest_time_ms': times[0] if times[0] else 0,
                'slowest_time_ms': times[1] if times[1] else 0,
                'average_time_ms': times[2] if times[2] else 0,
                'stars': stars
            }

    def get_available_years(self) -> List[int]:
        """Get all years that have tracked data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT year FROM runs ORDER BY year DESC")
            return [row[0] for row in cursor.fetchall()]

    def get_completion_status(self, year: int) -> Dict[int, Dict[int, bool]]:
        """
        Get completion status for all days and parts in a year.

        Returns:
            Dict mapping day -> part -> is_correct (True if correct answer exists, False if only attempted)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get all correct answers for the year
            cursor.execute("""
                SELECT day, part FROM correct_answers
                WHERE year = ?
            """, (year,))
            correct = {(row[0], row[1]) for row in cursor.fetchall()}

            # Get all attempted parts (with successful runs)
            cursor.execute("""
                SELECT DISTINCT day, part FROM runs
                WHERE year = ? AND success = 1
            """, (year,))
            attempted = {(row[0], row[1]) for row in cursor.fetchall()}

            # Build the status dict
            status = {}
            all_parts = correct | attempted

            for day, part in all_parts:
                if day not in status:
                    status[day] = {}
                status[day][part] = (day, part) in correct

            return status

    def sync_completed_problems(self, year: int, completed_data: dict) -> int:
        """
        Sync completed problems from AOC website into the database.

        Args:
            year: Year to sync
            completed_data: Dict from submitter.sync_completed_problems()

        Returns:
            Number of new correct answers added
        """
        new_answers_count = 0

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for day, day_data in completed_data.items():
                completed_parts = day_data['completed_parts']
                answers = day_data['answers']

                for part in completed_parts:
                    # Check if we already have this correct answer
                    cursor.execute("""
                        SELECT answer FROM correct_answers 
                        WHERE year = ? AND day = ? AND part = ?
                    """, (year, day, part))

                    existing = cursor.fetchone()
                    answer = answers.get(part, f"[COMPLETED-{year}-{day}-{part}]")

                    if not existing:
                        # Add new correct answer
                        cursor.execute("""
                            INSERT INTO correct_answers (year, day, part, answer)
                            VALUES (?, ?, ?, ?)
                        """, (year, day, part, answer))
                        new_answers_count += 1

                        # Also add a submission record to show it was completed
                        cursor.execute("""
                            INSERT OR IGNORE INTO submissions 
                            (year, day, part, timestamp, answer, status, response_message, wait_until)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (year, day, part, datetime.now(), answer, 'correct',
                              'Synced from AOC website - already completed', None))

                    elif existing[0] != answer and answer != f"[COMPLETED-{year}-{day}-{part}]":
                        # Update if we found the actual answer and it's different
                        cursor.execute("""
                            UPDATE correct_answers 
                            SET answer = ? 
                            WHERE year = ? AND day = ? AND part = ?
                        """, (answer, year, day, part))

            conn.commit()

        return new_answers_count

