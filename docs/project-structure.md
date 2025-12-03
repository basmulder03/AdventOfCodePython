# Project Structure

Understanding the organization and architecture of the Advent of Code Python solution runner.

## Directory Structure

```
AdventOfCodePython/
├── main.py                  # Main entry point and CLI
├── input.py                 # Input fetching and caching
├── tracking.py              # Performance tracking system
├── submitter.py             # AOC answer submission
├── benchmark.py             # Comprehensive benchmarking
├── benchmark_quick.py       # Quick benchmark presets
├── requirements.txt         # Python dependencies
├── session_cookie.txt       # Your AOC session cookie (private)
├── aoc_tracking.db          # SQLite tracking database
├── README.md                # Project documentation
├── docs/                    # Detailed documentation
│   ├── README.md           # Documentation index
│   ├── setup.md            # Installation guide
│   ├── cli-reference.md    # CLI documentation
│   ├── solution-guide.md   # How to write solutions
│   ├── tracking.md         # Performance tracking docs
│   ├── benchmarking.md     # Benchmarking documentation
│   ├── database-publishing.md # Database integration
│   ├── statistics.md       # Statistics generation
│   └── project-structure.md # This file
├── YYYY/                    # Year directories (e.g., 2015/, 2025/)
│   ├── day1.py             # Solution files
│   ├── day2.py
│   └── ...
├── input/                   # Input file storage
│   └── YYYY/               # Year subdirectories
│       ├── day1.txt        # Actual problem input
│       ├── day1_sample.txt # Sample input (optional)
│       └── ...
└── __pycache__/            # Python bytecode cache
```

## Core Modules

### `main.py` - CLI Entry Point

**Purpose:** Main command-line interface and orchestration

**Key Functions:**
- `main()` - Entry point and argument parsing
- `run_solution()` - Execute solutions with timing and tracking
- `handle_stats()` - Statistics generation
- `handle_benchmarking()` - Benchmark execution

**Dependencies:** All other modules

### `input.py` - Input Management

**Purpose:** Handle input fetching, caching, and processing

**Key Functions:**
- `get_input()` - Fetch input from cache or AOC
- `get_sample_input()` - Load sample input files
- `fetch_input_from_aoc()` - Download input from AOC website

**Features:**
- Automatic caching to avoid re-downloading
- Sample input file support
- Inline sample input handling
- Session cookie validation

### `tracking.py` - Performance Tracking

**Purpose:** Record and analyze solution performance over time

**Key Classes:**
- `PerformanceTracker` - Main tracking interface
- Database schema management
- Performance comparison logic

**Key Functions:**
- `record_run()` - Store execution results
- `get_performance_comparison()` - Compare with previous runs
- `get_recent_history()` - Retrieve run history
- `generate_statistics()` - Create performance summaries

**Database Tables:**
- `runs` - Individual execution records
- `submissions` - AOC submission attempts  
- `problems` - Problem metadata and best times

### `submitter.py` - Answer Submission

**Purpose:** Submit solutions to Advent of Code website

**Key Functions:**
- `submit_answer()` - Submit answer with rate limiting
- `parse_response()` - Parse AOC response messages
- `store_submission()` - Record submission attempts

**Features:**
- Rate limiting compliance
- Duplicate answer prevention
- Response parsing and storage
- Correct answer caching

### `benchmark.py` - Performance Benchmarking

**Purpose:** Comprehensive solution performance analysis

**Key Functions:**
- `benchmark_solution()` - Detailed single-solution benchmarking
- `benchmark_day()` - Both parts of a day
- `benchmark_year()` - All solutions for a year
- `benchmark_all()` - Everything with timeout protection

**Features:**
- Statistical analysis (mean, median, std dev)
- Warm-up runs for accuracy
- Timeout protection for slow solutions
- Database publishing integration

### `benchmark_quick.py` - Quick Benchmarking

**Purpose:** Convenient benchmark presets

**Presets:**
- `fast` - 3 runs, quick feedback
- `normal` - 10 runs, standard measurement  
- `thorough` - 25 runs, detailed analysis
- Year-level presets for batch benchmarking

## Solution Architecture

### Solution File Structure

Each solution file follows this pattern:

```python
from typing import Any

def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    # Your solution code here
    pass

def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    # Your solution code here
    pass
```

**Requirements:**
- Exact function names: `solve_part_1` and `solve_part_2`
- Single parameter: `input_data: str`
- Return any type (converted to string for display)

### Dynamic Loading

Solutions are loaded dynamically:

```python
# main.py logic (simplified)
import importlib

def load_solution(year: int, day: int):
    module_name = f"{year}.day{day}"
    module = importlib.import_module(module_name)
    
    return {
        1: getattr(module, 'solve_part_1', None),
        2: getattr(module, 'solve_part_2', None)
    }
```

This allows:
- No registration required - just create the file
- Template auto-generation for missing solutions
- Flexible solution organization

## Data Flow

### Typical Execution Flow

1. **CLI Parsing** (`main.py`)
   - Parse command line arguments
   - Validate year/day parameters

2. **Input Handling** (`input.py`)
   - Check for cached input files
   - Fetch from AOC if needed
   - Handle sample input if requested

3. **Solution Loading** (`main.py`)
   - Import solution module dynamically
   - Extract part functions
   - Generate template if missing

4. **Execution & Timing** (`main.py`)
   - Execute solution functions
   - Measure execution time
   - Capture results and errors

5. **Performance Tracking** (`tracking.py`)
   - Record run details in database
   - Compare with previous runs
   - Generate performance insights

6. **Optional: Submission** (`submitter.py`)
   - Submit answers to AOC
   - Handle response and rate limits
   - Store submission results

### Database Schema

```sql
-- Individual run records
CREATE TABLE runs (
    id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    day INTEGER NOT NULL,
    part INTEGER NOT NULL,
    execution_time_ms REAL NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    timestamp TEXT NOT NULL,
    code_hash TEXT,
    input_hash TEXT,
    is_sample BOOLEAN DEFAULT FALSE,
    result TEXT
);

-- Submission tracking
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    day INTEGER NOT NULL,
    part INTEGER NOT NULL,
    answer TEXT NOT NULL,
    response TEXT,
    success BOOLEAN,
    timestamp TEXT NOT NULL
);

-- Problem metadata
CREATE TABLE problems (
    year INTEGER NOT NULL,
    day INTEGER NOT NULL,
    part1_best_time REAL,
    part2_best_time REAL,
    PRIMARY KEY (year, day)
);
```

## Extension Points

### Adding New Features

**New CLI Commands:**
- Add argument parsing in `main.py`
- Implement handler function
- Add to main dispatch logic

**New Tracking Metrics:**
- Extend database schema
- Update `PerformanceTracker` class
- Modify statistics generation

**New Benchmarking Options:**
- Add to `benchmark.py`
- Create quick presets in `benchmark_quick.py`
- Update CLI integration

### Custom Solution Helpers

You can create shared utilities:

```python
# 2025/helpers.py
def parse_grid(input_data: str):
    """Common grid parsing logic."""
    pass

# 2025/day5.py  
from .helpers import parse_grid

def solve_part_1(input_data: str) -> int:
    grid = parse_grid(input_data)
    # ... rest of solution
```

## Development Workflow

### Setting Up for Development

1. **Environment Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Database Initialization:**
   ```bash
   # Database is created automatically on first run
   python main.py 2025 1  # This will create the schema
   ```

### Testing Changes

1. **Test with sample input:**
   ```bash
   python main.py 2025 1 --sample
   ```

2. **Test tracking:**
   ```bash
   python main.py 2025 1 --history
   ```

3. **Test benchmarking:**
   ```bash
   python benchmark_quick.py fast 2025 1
   ```

### Code Style

The project follows standard Python conventions:
- **PEP 8** style guidelines
- **Type hints** where appropriate
- **Docstrings** for public functions
- **Error handling** with meaningful messages

## Dependencies

### Required (`requirements.txt`)

```
requests>=2.25.0     # AOC communication
colorama>=0.4.0      # Terminal colors (optional)
```

### Standard Library Usage

- `sqlite3` - Database operations
- `importlib` - Dynamic module loading
- `argparse` - Command line parsing
- `hashlib` - Code change detection
- `time` - Performance measurement
- `json` - Data serialization
- `pathlib` - File system operations

## Performance Considerations

### Memory Usage

- **Input caching:** Input files are cached to disk, not kept in memory
- **Database:** SQLite provides efficient storage with minimal memory overhead
- **Solution isolation:** Each solution runs in isolation without persistent state

### I/O Optimization

- **Input caching:** Avoids repeated network requests
- **Database batching:** Multiple operations can be batched for efficiency
- **File system:** Uses pathlib for cross-platform compatibility

### Benchmarking Accuracy

- **Warm-up runs:** Account for Python startup and JIT effects
- **Multiple samples:** Statistical analysis for reliable measurements
- **Timeout protection:** Prevents hanging on inefficient solutions

## Next Steps

- Read [Setup Guide](setup.md) to get started
- Check [Solution Writing Guide](solution-guide.md) for best practices
- Explore [CLI Reference](cli-reference.md) for all available commands
