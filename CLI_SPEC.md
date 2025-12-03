# Advent of Code Python CLI Specification

## Overview

The Advent of Code Python CLI is a comprehensive solution runner that provides execution, tracking, submission, and statistics functionality for Advent of Code challenges. The CLI is implemented in Python and provides a rich terminal interface with optional colorized output.

## Command Syntax

```
python main.py [year] [day] [options]
```

## Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `year` | int | Conditional* | The year of the AOC challenge (e.g., 2015, 2023, 2025) |
| `day` | int | Conditional* | The day of the AOC challenge (1-25) |

*Required when running solutions, optional for other operations like `--stats`, `--sync`, etc.

## Options

### Execution Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--part` | `-p` | int | None | Run only specific part (1 or 2). If omitted, runs both parts |
| `--sample` | `-s` | flag | False | Use sample input instead of actual input |
| `--sample-input` | | string | None | Provide sample input directly as a string (implies --sample) |
| `--submit` | | flag | False | Submit the answer to AOC (only for actual input) |
| `--no-tracking` | | flag | False | Disable run tracking and performance comparison |

### Information & Statistics Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--history` | flag | False | Show recent run history for the specified problem |
| `--stats` | flag | False | Generate statistics tables from tracked data |
| `--year-filter` | int | None | Filter stats by specific year (used with --stats) |
| `--update-readme` | flag | False | Update README.md with latest statistics |
| `--sync` | int | None | Sync already completed problems from AOC website for specified year |

## Usage Examples

### Basic Execution
```bash
# Run both parts for day 1 of 2025
python main.py 2025 1

# Run only part 1
python main.py 2025 1 --part 1

# Run only part 2  
python main.py 2025 1 --part 2
```

### Sample Input Testing
```bash
# Use sample input file (input/2025/day1_sample.txt)
python main.py 2025 1 --sample

# Provide sample input directly as string
python main.py 2025 1 --sample-input "1\n2\n3"

# Multi-line sample input with escape sequences
python main.py 2025 1 --sample-input "line1\nline2\ttab"
```

### Submission
```bash
# Run and submit answer to AOC
python main.py 2025 1 --submit

# Submit only part 1
python main.py 2025 1 --part 1 --submit

# Note: Submission only works with actual input, not sample
```

### Performance Tracking
```bash
# Run without tracking (faster, no database operations)
python main.py 2025 1 --no-tracking

# View recent run history for a problem
python main.py 2025 1 --history

# View history for specific part only
python main.py 2025 1 --part 1 --history
```

### Statistics & Analysis
```bash
# Show statistics for all years
python main.py --stats

# Show statistics for specific year
python main.py --stats --year-filter 2025

# Update README.md with latest statistics
python main.py --update-readme

# Sync completed problems from AOC website
python main.py --sync 2025
```

## File Structure Requirements

### Solution Files
- Solutions must be placed in `{year}/day{day}.py`
- Each solution file must contain:
  - `solve_part_1(input_data: str) -> Any`
  - `solve_part_2(input_data: str) -> Any`

### Input Files
- Actual input: `input/{year}/day{day}.txt`
- Sample input: `input/{year}/day{day}_sample.txt`

### Configuration Files
- `session_cookie.txt`: AOC session cookie for input downloading and submission
- `aoc_tracking.db`: SQLite database for performance tracking (auto-created)

## Output Format

### Execution Output
```
============================================================
🎄 Advent of Code 2025 - Day 1 🎄
============================================================

⭐ Part 1:
  Answer: 142
  Time: 0.123 ms
  🚀 2.3% faster than best (0.126 ms)
  📈 5.1% faster than previous run
  Run #15

⭐ Part 2:
  Answer: 281
  Time: 0.089 ms
  🥇 New personal best!
  Run #8

------------------------------------------------------------
⏱️  Total Time: 0.212 ms
============================================================
```

### Statistics Output
- Overall summary across all years
- Year-by-year breakdowns
- Best times per day/part
- Success rates and run counts
- Performance comparisons

### Error Handling
- Missing solution files: Auto-creates template
- Missing input files: Downloads from AOC (if cookie provided) or creates empty sample
- Solution errors: Displays error message and continues with other parts
- Submission errors: Shows timeout information and retry guidance

## Dependencies

### Required Python Packages
- `requests>=2.25.1`: HTTP requests for input/submission
- `beautifulsoup4>=4.9.3`: HTML parsing for submission responses
- `colorama>=0.4.4`: Terminal color support (optional, graceful fallback)

### Python Version
- Requires Python 3.7+ (uses `pathlib`, type hints, f-strings)

## Database Schema

The CLI uses SQLite for performance tracking:

### Tables
- `runs`: Individual solution executions with timing data
- `submissions`: AOC submission attempts and results
- `correct_answers`: Known correct answers for validation

### Tracking Features
- Execution time comparison vs personal best
- Success/failure rates
- Code change detection (via hashing)
- Submission timeout management

## Session Management

### AOC Session Cookie
Required for:
- Automatic input downloading
- Answer submission
- Completed problem syncing

### Cookie Setup
1. Log into adventofcode.com
2. Copy session cookie from browser
3. Save to `session_cookie.txt` in project root

## Error Codes & Exit Behavior

- **Success**: Normal execution, exits with code 0
- **Missing Arguments**: Shows help and exits
- **File Not Found**: Creates templates/files when possible
- **Network Errors**: Graceful handling with user-friendly messages
- **Solution Errors**: Continues execution, doesn't exit

## Advanced Features

### Automatic Template Creation
When a solution file doesn't exist, automatically creates:
```python
from typing import Any

def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    pass

def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    pass
```

### Smart Submission Management
- Prevents duplicate submissions
- Respects AOC timeout periods
- Validates against known correct answers
- Tracks submission history

### Performance Intelligence
- Detects code changes via hashing
- Compares performance across code versions
- Identifies performance regressions
- Tracks improvement over time

### README Integration
- Auto-updates README.md with statistics
- Generates markdown tables
- Includes performance summaries
- Timestamps for freshness tracking

## Extensibility

The CLI is designed for extensibility:
- Modular design with separate concerns (input, tracking, submission)
- Plugin-ready architecture
- Database schema supports additional metrics
- Configurable output formatting
