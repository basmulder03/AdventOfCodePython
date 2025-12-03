# Advent of Code Python Solutions

A comprehensive solution runner for [Advent of Code](https://adventofcode.com/) challenges with performance tracking, automated submission, and statistics generation.

## Features

- 🎄 **Solution Runner**: Execute AOC solutions with timing and error handling
- 📊 **Performance Tracking**: Track execution times and compare with previous runs  
- 🚀 **Auto Submission**: Submit answers directly to AOC with smart timeout handling
- 📈 **Statistics**: Generate comprehensive stats tables from tracked data
- 🎯 **Sample Input Support**: Test with sample data or custom input strings
- 📝 **Template Generation**: Auto-create solution templates for new problems
- 🎨 **Colorized Output**: Beautiful terminal output with progress indicators

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Session Cookie**
   - Get your session cookie from AOC website
   - Save it in `session_cookie.txt`

3. **Run a Solution**
   ```bash
   python main.py 2025 1
   ```

## Usage

### Basic Commands

```bash
# Run both parts for day 1 of 2025
python main.py 2025 1

# Run only part 1
python main.py 2025 1 --part 1

# Test with sample input
python main.py 2025 1 --sample

# Provide custom sample input
python main.py 2025 1 --sample-input "1\n2\n3"

# Submit answer to AOC
python main.py 2025 1 --submit

# Show run history
python main.py 2025 1 --history
```

### Statistics Generation

Generate comprehensive statistics tables from your tracked performance data:

```bash
# Generate all statistics
python main.py --stats

# Generate stats for specific year
python main.py --stats --year-filter 2025

# Generate stats and update README
python main.py --stats --update-readme
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `year day` | Year and day of the challenge to run |
| `--part, -p` | Run only specific part (1 or 2) |
| `--sample, -s` | Use sample input file |
| `--sample-input` | Provide sample input as string |
| `--submit` | Submit answer to AOC |
| `--history` | Show recent run history |
| `--no-tracking` | Disable performance tracking |
| `--stats` | Generate statistics tables |
| `--year-filter YEAR` | Filter stats by specific year |
| `--update-readme` | Update this README with latest stats |

## Project Structure

```
AdventOfCodePython/
├── main.py              # Main runner script
├── input.py             # Input fetching utilities
├── tracking.py          # Performance tracking system
├── submitter.py         # AOC submission handler
├── requirements.txt     # Python dependencies
├── session_cookie.txt   # Your AOC session cookie
├── aoc_tracking.db      # SQLite database for tracking
├── YYYY/                # Year directories
│   └── dayN.py         # Daily solutions
└── input/               # Input files
    └── YYYY/
        └── dayN.txt
```

## Solution Template

When you run a new day, a template is automatically created:

```python
from typing import Any

def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    pass

def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    pass
```

<!-- STATS_START -->
## 🎄 Overall Statistics

**Summary Across All Years (2015-2015):**
- ⭐ Total Stars: 43
- 🧩 Total Problems Solved: 42
- 🏃 Total Runs: 54 (100.0% success)
- ⚡ Average Time: 307.0ms
- 🚀 Fastest Time: 0.002ms
- 🐌 Slowest Time: 6.18s


## 2015 Statistics

**Year Summary:**
- ⭐ Stars: 41
- 🧩 Problems Solved: 42
- 🏃 Total Runs: 54 (100.0% success)
- ⚡ Average Time: 307.0ms
- 🚀 Fastest Time: 0.002ms

**Best Times by Day:**

| Day | Part 1 | Part 2 | Total |
|-----|--------|--------|-------|
|  1 | 0.326ms | 0.090ms | 0.415ms |
|  2 |   1.9ms | 0.488ms |   2.4ms |
|  3 |   4.5ms |   3.7ms |   8.2ms |
|  4 |  68.0ms |   2.18s |   2.25s |
|  5 |   2.8ms |   8.2ms |  11.0ms |
|  6 |  73.3ms |  18.2ms |  91.5ms |
|  7 | 0.281ms | 0.502ms | 0.782ms |
|  8 | 0.622ms | 0.320ms | 0.942ms |
|  9 |  33.8ms |  23.0ms |  56.8ms |
| 10 | 122.3ms |   2.28s |   2.40s |
| 11 |  19.8ms | 573.9ms | 593.7ms |
| 12 |   2.4ms |   1.4ms |   3.7ms |
| 13 |  19.2ms |  67.6ms |  86.8ms |
| 14 | 0.406ms |  11.0ms |  11.4ms |
| 15 | 407.4ms | 450.1ms | 857.5ms |
| 16 | 0.320ms | 0.690ms |   1.0ms |
| 17 |  17.9ms |  10.4ms |  28.3ms |
| 18 | 909.3ms | 913.9ms |   1.82s |
| 19 | 0.355ms |   1.5ms |   1.8ms |
| 20 |   2.16s |   6.18s |   8.34s |
| 21 | 0.003ms | 0.002ms | 0.005ms |

*Last updated: 2025-12-03 11:59:48*
<!-- STATS_END -->

## Performance Tracking

The tracker automatically records:
- Execution times for each run
- Code changes (via content hash)
- Success/failure status
- Input variations
- Submission attempts and results

Performance comparisons show:
- 🥇 Personal best times
- 📈 Improvements vs previous runs
- 📊 Run count and success rate

## Submission Features

- ✅ **Smart Timeout Handling**: Respects AOC's rate limits
- 🔍 **Duplicate Detection**: Won't resubmit the same answer
- 📝 **Response Tracking**: Stores submission results
- 🎯 **Correct Answer Cache**: Remembers accepted answers

## Requirements

- Python 3.7+
- `requests` (for AOC communication)
- `colorama` (optional, for colored output)

## License

This project is for educational purposes. Please respect Advent of Code's [terms of service](https://adventofcode.com/about).
