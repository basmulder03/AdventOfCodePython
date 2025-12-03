# Benchmark Database Publishing

The benchmark system now supports publishing results directly to the SQLite tracking database. This allows you to:

1. **Track performance over time** - See how your optimizations affect performance
2. **Compare with previous runs** - Leverage the existing performance comparison system
3. **Historical analysis** - Use the same data for statistics and history commands

## Usage

### Main CLI
```bash
# Benchmark and publish to database
python main.py 2025 1 --benchmark --benchmark-publish

# Benchmark specific part and publish
python main.py 2025 1 --benchmark --benchmark-publish --part 1

# Benchmark entire year and publish
python main.py --benchmark-year 2025 --benchmark-publish

# Benchmark everything and publish (careful!)
python main.py --benchmark-all --benchmark-publish
```

### Quick Benchmark Tool
```bash
# Fast benchmark with database publishing
python benchmark_quick.py fast 2025 1 --publish

# Normal benchmark with database publishing
python benchmark_quick.py normal 2025 1 --publish

# Thorough benchmark with database publishing
python benchmark_quick.py thorough 2025 1 --publish

# Year benchmarks with database publishing
python benchmark_quick.py fast-year 2025 --publish
```

## Database Integration

When `--benchmark-publish` or `--publish` is used:

- Each benchmark run is stored as a separate record in the `runs` table
- Results include execution time, success/failure status, and error messages
- Input and code hashes are stored for change tracking
- `is_sample` is set to `False` (benchmarks use real input data)
- Results can be viewed using existing history and stats commands

## Notes

- Database publishing requires tracking to be enabled (don't use `--no-tracking`)
- Only successful benchmark runs contribute to statistics
- Warmup runs are not published to the database
- Each individual run within a benchmark session is recorded separately

## Example Workflow

```bash
# Run baseline benchmark and publish
python main.py 2025 1 --benchmark --benchmark-publish --benchmark-runs 10

# Make code optimizations
# ...

# Run new benchmark and compare
python main.py 2025 1 --benchmark --benchmark-publish --benchmark-runs 10

# View performance history
python main.py 2025 1 --history

# Check statistics
python main.py --stats
```
