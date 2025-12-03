# Markdown Documentation Generation

Automatically generate and update markdown documentation based on your benchmark results and solution statistics.

## Overview

The markdown generation system creates beautiful, organized documentation of your Advent of Code solutions, including:

- **Main README**: Overview table showing all years at a glance
- **Year-specific files**: Detailed performance statistics for each year
- **Day-specific files**: Comprehensive run history for individual days

All documentation is generated from benchmark data stored in the tracking database, ensuring accuracy and consistency.

## Quick Start

### Update Everything

```bash
python main.py --update-markdown --markdown-all
```

This updates:
- Main README overview table
- All year-specific results files (in `docs/`)
- Links everything together

### After Benchmarking

When you run benchmarks with `--benchmark-publish`, markdown files are automatically updated:

```bash
# Benchmark and auto-update documentation
python main.py 2025 1 --benchmark --benchmark-publish
```

## Command Reference

### Main README Update

Update only the main README.md overview table:

```bash
python main.py --update-markdown
```

### Year-Specific Update

Update a specific year's detailed results file:

```bash
# Update docs/2025-results.md and main README
python main.py --update-markdown --markdown-year 2025
```

### Day-Specific Update

Update documentation after running a specific day:

```bash
# Updates day results, year results, and main README
python main.py 2025 1 --update-markdown
```

### Update All Documentation

Update everything at once:

```bash
python main.py --update-markdown --markdown-all
```

## Generated Files

### Main README (README.md)

The main README contains an overview table showing:
- Year (linked to year-specific file)
- Total stars earned
- Problems solved
- Total runs and success rate
- Average execution time
- Fastest and slowest times

Example:

```markdown
## 🎄 Solutions Overview

| Year | Stars ⭐ | Problems 🧩 | Runs 🏃 | Success Rate | Avg Time ⚡ | Fastest 🚀 | Slowest 🐌 |
|------|----------|-------------|---------|--------------|-------------|------------|------------|
| [2025](./docs/2025-results.md) | 6 | 6 | 18 | 83.3% | 147.7ms | 556.5μs | 771.9ms |
| [2015](./docs/2015-results.md) | 50 | 50 | 100 | 91.0% | 633.8ms | 0.2μs | 11.54s |
```

### Year Results (docs/{year}-results.md)

Each year file includes:
- Year summary statistics
- Performance by day table (with star indicators)
- Performance distribution (fast/medium/slow)
- Links back to main README

Example structure:

```markdown
# 🎄 Advent of Code 2025 Results

[← Back to Overview](../README.md)

## Year Summary
- ⭐ **Stars**: 6
- 🧩 **Problems Solved**: 6
- 🏃 **Total Runs**: 18 (83.3% success)
- ⚡ **Average Time**: 147.7ms
...

## Performance by Day
| Day | Part 1 | Part 2 | Total | Status |
|-----|--------|--------|-------|--------|
|  1 | 556.5μs | 750.7μs |   1.3ms | ⭐⭐ |
...
```

### Day Results ({year}/day{day}-results.md)

Day-specific files show:
- Summary for each part (best time, result)
- Complete run history
- Links to year results

*Note: Day-specific results are currently generated separately and not created by default.*

## Workflow Integration

### Option 1: Benchmark and Auto-Update

The recommended workflow for maintaining up-to-date documentation:

```bash
# Benchmark specific day with database publishing
python main.py 2025 1 --benchmark --benchmark-publish

# Benchmark entire year with auto-update
python main.py --benchmark-year 2025 --benchmark-publish

# Benchmark everything and update all docs
python main.py --benchmark-all --benchmark-publish
```

Benefits:
- ✅ Automatic documentation updates
- ✅ Accurate performance data
- ✅ No manual maintenance needed

### Option 2: Manual Update

Update documentation separately from benchmarking:

```bash
# Run benchmarks with saving
python main.py 2025 1 --benchmark --benchmark-save

# Later, manually update markdown
python main.py --update-markdown --markdown-all
```

### Option 3: After Running Solutions

Update documentation after normal solution runs (uses tracked data):

```bash
# Run solutions (with tracking enabled)
python main.py 2025 1

# Update markdown when ready
python main.py --update-markdown --markdown-year 2025
```

## Data Sources

The markdown generator pulls data from the tracking database (`aoc_tracking.db`):

- **Best times**: Fastest successful run for each part
- **Run counts**: Total number of attempts
- **Success rates**: Percentage of successful runs
- **Results**: Actual answers for completed problems

### Populating the Database

To have data for markdown generation, you need runs in the database:

1. **Run solutions normally** (creates tracked runs):
   ```bash
   python main.py 2025 1
   ```

2. **Benchmark and publish** (creates benchmark runs):
   ```bash
   python main.py 2025 1 --benchmark --benchmark-publish
   ```

3. **Sync from AOC website** (for completed problems):
   ```bash
   python main.py --sync 2025
   ```

## Customization

### Time Formatting

Times are automatically formatted for readability:
- Microseconds: `556.5μs` (< 1ms)
- Milliseconds: `1.3ms`, `147.7ms` (< 1s)
- Seconds: `2.18s`, `11.54s` (≥ 1s)

### Performance Categories

Solutions are categorized by speed:
- 🚀 **Fast**: < 10ms
- ⚡ **Medium**: 10ms - 1s
- 🐌 **Slow**: ≥ 1s

### Timestamps

All generated files include a "Last updated" timestamp showing when they were generated.

## Tips and Best Practices

### 1. Keep Documentation Fresh

Update documentation after major benchmarking sessions:

```bash
python main.py --benchmark-year 2025 --benchmark-runs 25 --benchmark-publish
```

The `--benchmark-publish` flag ensures automatic markdown updates.

### 2. Regular Updates

Set up a routine for keeping docs updated:

```bash
# Weekly: Re-benchmark everything with more runs
python main.py --benchmark-all --benchmark-runs 10 --benchmark-publish
```

### 3. Quick Updates

For quick documentation updates without re-running benchmarks:

```bash
python main.py --update-markdown --markdown-all
```

### 4. Version Control

Commit generated markdown files to track your progress:

```bash
git add README.md docs/*-results.md
git commit -m "Update performance documentation"
```

## Troubleshooting

### No Data Available

If markdown shows "No tracked data available":

1. Verify the tracking database exists: `aoc_tracking.db`
2. Run some solutions to populate data
3. Or use `--benchmark-publish` to create benchmark entries

### Markdown Not Updating

If running update commands but seeing no changes:

1. Check that tracking is enabled (don't use `--no-tracking`)
2. Verify there's actual data in the database
3. Check file permissions for README.md and docs/ directory

### Links Not Working

Ensure the directory structure matches expectations:
- Main README.md at project root
- Year results in `docs/{year}-results.md`
- Day results in `{year}/day{day}-results.md`

## Example Workflow

Complete workflow from solving to documentation:

```bash
# 1. Solve the problem
python main.py 2025 1

# 2. Benchmark for accurate performance data
python main.py 2025 1 --benchmark --benchmark-runs 25 --benchmark-publish

# 3. Documentation is auto-updated!
# View the results:
cat README.md
cat docs/2025-results.md

# 4. Commit to version control
git add README.md docs/2025-results.md
git commit -m "Add day 1 solution with benchmarks"
```

## Related Documentation

- [CLI Reference](cli-reference.md) - Complete command documentation
- [Benchmarking](benchmarking.md) - Performance testing guide
- [Tracking](tracking.md) - Database and tracking system
- [Statistics](statistics.md) - Statistics generation

## Summary

The markdown generation system provides:

✅ **Automatic documentation** from benchmark results  
✅ **Clean, organized structure** with overview and detailed views  
✅ **Easy maintenance** with simple CLI commands  
✅ **Integration with benchmarking** for automatic updates  
✅ **Beautiful formatting** with emoji indicators and tables  

Keep your Advent of Code documentation up-to-date effortlessly!

