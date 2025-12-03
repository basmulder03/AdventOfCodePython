# Performance Tracking

Understanding how the performance tracking system works and how to use it effectively.

## Overview

The tracking system automatically records execution data for every solution run, providing:
- **Performance metrics** - execution times, success rates
- **Historical comparison** - see improvements over time  
- **Code change detection** - tracks when your solution changes
- **Statistics generation** - comprehensive performance analysis

## How It Works

### Automatic Tracking

Every time you run a solution, the system automatically:

1. **Records execution time** down to milliseconds
2. **Tracks success/failure** and any error messages
3. **Detects code changes** using content hashing
4. **Stores input variations** (sample vs actual input)
5. **Links to submission attempts** if you use `--submit`

### Database Storage

All tracking data is stored in `aoc_tracking.db` (SQLite database) with these tables:

- **`runs`** - individual execution records
- **`submissions`** - AOC submission attempts and responses
- **`problems`** - problem metadata and best times

## Viewing Performance Data

### Recent History

See your recent runs for a specific problem:

```bash
python main.py 2025 1 --history
```

Example output:
```
📊 Recent runs for 2025 Day 1:

🥇 Personal Best: Part 1: 1.234ms, Part 2: 2.345ms
📈 Performance: Showing last 5 runs

Run #1 (2025-12-01 10:30:15)
├─ Part 1: ✅ 1.234ms (🥇 New best!)
└─ Part 2: ✅ 2.345ms (📈 +0.1ms vs best)

Run #2 (2025-12-01 10:25:30)
├─ Part 1: ✅ 1.456ms (+0.222ms vs best)
└─ Part 2: ✅ 2.567ms (+0.222ms vs best)
```

### Comprehensive Statistics

Generate statistics across all your solutions:

```bash
# All statistics
python main.py --stats

# Filter by year
python main.py --stats --year-filter 2025

# Update README with latest stats
python main.py --stats --update-readme
```

## Understanding Performance Comparisons

### Color Coding

When you run solutions, performance comparisons use color coding:

- **🥇 Gold:** New personal best
- **🥈 Silver:** Within 5% of personal best  
- **📈 Green:** Faster than recent average
- **📊 Blue:** Normal performance
- **📉 Red:** Slower than recent average

### Time Differences

The system shows time differences in context:

```
✅ 1.234ms (🥇 New best!)           # New personal record
✅ 1.256ms (+0.022ms vs best)       # 22ms slower than best
✅ 1.190ms (-0.044ms vs best)       # 44ms faster than best
```

## Code Change Detection

### How It Works

The system uses SHA-256 hashing to detect when your solution code changes:

1. **Hash calculation** - generates hash of solution file content
2. **Change detection** - compares with previous runs
3. **Performance attribution** - links performance changes to code changes

### What This Means

- **Same hash:** Performance differences are due to system load, not code changes
- **Different hash:** Performance differences likely due to your optimizations
- **First run:** No comparison data available yet

### Example

```
📊 Performance comparison:
├─ Current: 1.234ms (code hash: abc123...)
├─ Previous: 2.345ms (code hash: def456...)
└─ Improvement: -1.111ms (47.4% faster) 🚀 Code changed
```

## Disabling Tracking

### Temporary Disable

Skip tracking for a single run:

```bash
python main.py 2025 1 --no-tracking
```

### Use Cases

- **Testing/debugging:** Avoid cluttering history with debug runs
- **Benchmarking:** Use dedicated benchmarking tools instead
- **Sample input:** May want to avoid tracking sample runs

## Advanced Features

### Benchmark Integration

Benchmarking results can be published to the tracking database:

```bash
# Run benchmark and save to tracking database
python main.py 2025 1 --benchmark --benchmark-publish
```

This creates multiple tracking entries (one per benchmark run) for statistical analysis.

### Submission Tracking

When you submit answers, the system tracks:

- **Submission attempts** and their results
- **Rate limiting** compliance with AOC servers
- **Duplicate prevention** won't resubmit the same answer
- **Success tracking** remembers correct answers

```bash
python main.py 2025 1 --submit
```

## Database Schema

### `runs` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `year` | INTEGER | Problem year |
| `day` | INTEGER | Problem day |
| `part` | INTEGER | Problem part (1 or 2) |
| `execution_time_ms` | REAL | Execution time in milliseconds |
| `success` | BOOLEAN | Whether the run succeeded |
| `error_message` | TEXT | Error details if failed |
| `timestamp` | TEXT | When the run occurred |
| `code_hash` | TEXT | SHA-256 hash of solution code |
| `input_hash` | TEXT | SHA-256 hash of input data |
| `is_sample` | BOOLEAN | Whether sample input was used |
| `result` | TEXT | The computed result |

### Querying the Database

You can query the database directly for custom analysis:

```sql
-- Find your fastest solutions
SELECT year, day, part, MIN(execution_time_ms) as best_time
FROM runs 
WHERE success = 1 
GROUP BY year, day, part
ORDER BY best_time;

-- See performance trends over time
SELECT date(timestamp) as day, AVG(execution_time_ms) as avg_time
FROM runs 
WHERE success = 1 AND year = 2025 AND day = 1
GROUP BY date(timestamp)
ORDER BY day;
```

## Performance Tips

### Interpreting Results

- **Single runs** can vary due to system load
- **Multiple runs** give better average performance
- **Benchmarking** provides statistical analysis
- **Code changes** should show consistent improvements

### Optimization Workflow

1. **Baseline:** Run your initial solution several times
2. **Optimize:** Make improvements to your code
3. **Compare:** Run again and check the performance comparison
4. **Iterate:** Repeat until satisfied with performance

### System Considerations

Performance can be affected by:
- **System load** - other programs running
- **Python startup** - first run might be slower
- **File I/O** - input reading time
- **Memory usage** - garbage collection effects

For the most accurate measurements, use the benchmarking features which account for these factors.

## Next Steps

- Learn about [Benchmarking](benchmarking.md) for detailed performance analysis
- Check [Database Publishing](database-publishing.md) for advanced benchmarking features
- See [Statistics Generation](statistics.md) for understanding the stats system
