# CLI Quick Reference

## Running Solutions (Default Mode)

```bash
# Run both parts
python main.py 2025 1

# Run specific part
python main.py 2025 1 --part 1

# Use sample input
python main.py 2025 1 -s
python main.py 2025 1 --sample

# Provide inline sample input
python main.py 2025 1 --sample-input "1\n2\n3"

# Submit answer
python main.py 2025 1 --part 1 --submit

# View run history
python main.py 2025 1 --history

# Disable timeout
python main.py 2025 1 --no-timeout

# Custom timeout
python main.py 2025 1 --timeout 10.0

# Validate output
python main.py 2025 1 --part 1 --expected 12345
python main.py 2025 1 --expected-p1 12345 --expected-p2 67890
```

## Output Validation

Validate solution outputs against expected values:

```bash
# Validate single part
python main.py 2025 1 --part 1 --expected 12345

# Validate both parts
python main.py 2025 1 --expected-p1 12345 --expected-p2 67890

# With sample input
python main.py 2025 1 --sample-input "test" --expected-p1 100 --expected-p2 200

# In benchmark mode
python main.py benchmark 2025 1 --expected-p1 12345 --expected-p2 67890
```

See [validation.md](validation.md) for detailed documentation.

## Sync Command

Sync completed problems from AOC website:

```bash
# Sync a specific year
python main.py sync 2025

# Sync without tracking
python main.py sync 2025 --no-tracking
```

## Benchmark Command

Run performance benchmarks:

```bash
# Benchmark a specific day
python main.py benchmark 2025 1

# Benchmark specific part
python main.py benchmark 2025 1 --part 1

# Benchmark all solutions in a year
python main.py benchmark --year 2025

# Benchmark all available solutions
python main.py benchmark --all

# Custom benchmark settings
python main.py benchmark 2025 1 --runs 25 --warmup 5 --timeout 60

# Save results
python main.py benchmark 2025 1 --save
python main.py benchmark 2025 1 --save results.json

# Publish to database (auto-updates markdown)
python main.py benchmark 2025 1 --publish

# Show detailed help
python main.py benchmark --help-full
```

## Stats Command

Display statistics from tracked runs:

```bash
# Show all statistics
python main.py stats

# Filter by year
python main.py stats --year 2025
```

## Markdown Command

Update documentation:

```bash
# Update main README only
python main.py markdown

# Update all markdown files
python main.py markdown --all

# Update specific year
python main.py markdown --year 2025

# Update specific day
python main.py markdown 2025 1
python main.py markdown --year 2025 --day 1
```

## Getting Help

```bash
# Main help
python main.py --help

# Subcommand help
python main.py sync --help
python main.py benchmark --help
python main.py stats --help
python main.py markdown --help

# Detailed benchmark help
python main.py benchmark --help-full
```

## Common Workflows

### Daily Solving
```bash
# Run with sample
python main.py 2025 1 -s

# Run with actual input
python main.py 2025 1

# Submit part 1
python main.py 2025 1 --part 1 --submit

# Submit part 2
python main.py 2025 1 --part 2 --submit
```

### Performance Tuning
```bash
# Quick benchmark
python main.py benchmark 2025 1

# Detailed benchmark
python main.py benchmark 2025 1 --runs 50 --warmup 10

# Save and publish
python main.py benchmark 2025 1 --publish --save
```

### Documentation Updates
```bash
# After solving a problem
python main.py markdown --year 2025

# After benchmarking
python main.py markdown --all
```

### Year-End Workflows
```bash
# Sync all completed problems
python main.py sync 2025

# Benchmark entire year
python main.py benchmark --year 2025 --publish

# Update all documentation
python main.py markdown --all

# View statistics
python main.py stats --year 2025
```

