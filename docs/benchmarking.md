# Benchmarking Documentation

## Overview

This Advent of Code project includes comprehensive benchmarking functionality to measure and compare the performance of your solutions at multiple levels:

- **Individual Problem Benchmarking** - Benchmark a single day/part with detailed statistics
- **Day Benchmarking** - Benchmark both parts of a specific day
- **Year Benchmarking** - Benchmark all solutions for a given year
- **Full Set Benchmarking** - Benchmark all available solutions across all years
- **Performance Comparison** - Track improvements and regressions over time

## Quick Start

### Basic Benchmarking

```bash
# Benchmark both parts of a specific day
python main.py 2025 1 --benchmark

# Benchmark only part 1
python main.py 2025 1 --benchmark --part 1

# Benchmark with more runs for accuracy
python main.py 2025 1 --benchmark --benchmark-runs 20
```

### Quick Presets

```bash
# Fast benchmark (3 runs, good for quick checks)
python benchmark_quick.py fast 2025 1

# Normal benchmark (10 runs, standard measurement)
python benchmark_quick.py normal 2025 1

# Thorough benchmark (25 runs, detailed analysis)
python benchmark_quick.py thorough 2025 1
```

### Year and All Solutions

```bash
# Benchmark all solutions for a year
python main.py --benchmark-year 2025

# Benchmark everything (with timeout to skip slow solutions)
python main.py --benchmark-all --benchmark-timeout 10
```

## Command Line Options

### Main Benchmark Options

| Option | Description | Default |
|--------|-------------|---------|
| `--benchmark` | Run benchmarking on specified problem/day | - |
| `--benchmark-runs N` | Number of benchmark runs | 10 |
| `--benchmark-warmup N` | Number of warmup runs | 3 |
| `--benchmark-timeout N` | Timeout per run in seconds | 30.0 |
| `--benchmark-save [FILE]` | Save results to JSON file | - |
| `--benchmark-year YEAR` | Benchmark all solutions for year | - |
| `--benchmark-all` | Benchmark all available solutions | - |

### Examples

```bash
# Quick test with minimal runs
python main.py 2025 1 --benchmark --benchmark-runs 3 --benchmark-timeout 5

# Thorough analysis with many runs
python main.py 2025 1 --benchmark --benchmark-runs 50 --benchmark-warmup 10

# Save results for later comparison
python main.py 2025 1 --benchmark --benchmark-save my_results.json

# Benchmark entire year with conservative timeout
python main.py --benchmark-year 2025 --benchmark-timeout 15
```

## Quick Benchmark Utility

The `benchmark_quick.py` utility provides common benchmarking scenarios with sensible presets:

### Individual Problems

```bash
python benchmark_quick.py fast 2025 1       # 3 runs, 2 warmup, 5s timeout
python benchmark_quick.py normal 2025 1     # 10 runs, 3 warmup, 30s timeout  
python benchmark_quick.py thorough 2025 1   # 25 runs, 5 warmup, 60s timeout
```

### Year Benchmarks

```bash
python benchmark_quick.py fast-year 2025    # Quick benchmark all of 2025
python benchmark_quick.py normal-year 2025  # Standard benchmark all of 2025
```

### All Solutions

```bash
python benchmark_quick.py fast-all          # Quick benchmark everything
```

### Save Results

```bash
python benchmark_quick.py normal 2025 1 --save           # Auto filename
python benchmark_quick.py normal 2025 1 --save my.json   # Custom filename
```

## Understanding the Output

### Individual Problem Statistics

```
📊 2025 Day 1 Part 1 Statistics:
  Success Rate: 100.0% (5/5)
  Min Time:     1.112ms
  Max Time:     21.447ms
  Mean Time:    5.477ms
  Median Time:  1.583ms
  Std Dev:      8.930ms
  ⚠️  High variation
```

- **Success Rate**: Percentage of runs that completed successfully
- **Min/Max Time**: Fastest and slowest execution times
- **Mean Time**: Average execution time
- **Median Time**: Middle value (less affected by outliers)
- **Std Dev**: Standard deviation (consistency indicator)
- **Variation Indicator**: 
  - ✅ Consistent performance (< 5% variation)
  - ⚠️ Moderate variation (5-15% variation)
  - ⚠️ High variation (> 15% variation)

### Year Summary

```
============================================================
📈 Year 2025 Summary
============================================================
Total Problems: 6
Successful: 6 (100.0%)
Fastest Solution: 0.548ms
Slowest Solution: 718.916ms
Average Time: 161.554ms
Total Runtime: 1938.653ms

🚀 Top 5 Fastest Solutions:
  1. Day  1 Part 1: 0.548ms
  2. Day  1 Part 2: 0.700ms
  3. Day  3 Part 1: 2.856ms
  4. Day  3 Part 2: 2.887ms
  5. Day  2 Part 1: 247.542ms
```

## Saved Results Format

Benchmark results are saved in JSON format:

```json
{
  "timestamp": "2025-12-03T14:47:20.247626",
  "results": {
    "2025": {
      "1": {
        "1": {
          "runs": 10,
          "success_count": 10,
          "success_rate": 1.0,
          "min_time": 0.0005842,
          "max_time": 0.0006269,
          "mean_time": 0.0006055,
          "median_time": 0.0006055,
          "std_dev": 3.01934e-05,
          "times": [0.0005842, 0.0006269, ...]
        }
      }
    }
  }
}
```

## Performance Comparison Workflows

### Before/After Optimization

```bash
# Baseline measurement
python benchmark_quick.py normal 2025 1 --save baseline.json

# ... make optimizations ...

# Comparison measurement
python benchmark_quick.py normal 2025 1 --save optimized.json

# Compare results manually or with custom scripts
```

### Regression Testing

```bash
# Create performance baseline
python benchmark_quick.py fast-year 2025 --save baseline_2025.json

# After code changes, check for regressions
python benchmark_quick.py fast-year 2025 --save current_2025.json
```

### Finding Bottlenecks

```bash
# Quick scan of all solutions with short timeout
python main.py --benchmark-all --benchmark-runs 1 --benchmark-timeout 5

# Focus on slowest solutions found
python benchmark_quick.py thorough 2025 2  # If day 2 was slow
```

## Best Practices

### Choosing Run Counts

- **1-3 runs**: Quick smoke tests, development iteration
- **5-10 runs**: Standard measurements, CI/CD pipelines
- **15-25 runs**: Detailed analysis, optimization work
- **50+ runs**: Statistical significance, research purposes

### Timeout Settings

- **5s**: Quick development checks, skip very slow solutions
- **30s**: Standard timeout, catches most reasonable solutions
- **60s+**: Allow time for complex algorithms, complete coverage

### Warmup Considerations

- **2-3 warmup runs**: Standard for most cases
- **5+ warmup runs**: When measuring very fast operations
- **0 warmup runs**: When measuring cold-start performance

### When to Use Each Level

#### Individual Problem (`python main.py YEAR DAY --benchmark`)
- Optimizing a specific solution
- Detailed performance analysis
- A/B testing different approaches

#### Day Benchmark (`python benchmark_quick.py normal YEAR DAY`)
- Comparing both parts of a problem
- Daily performance check
- Before/after optimization comparison

#### Year Benchmark (`python benchmark_quick.py fast-year YEAR`)
- Performance overview of a complete year
- Identifying problematic solutions
- Regression testing after refactoring

#### Full Benchmark (`python benchmark_quick.py fast-all`)
- Complete performance audit
- Finding the slowest solutions overall
- Performance leaderboard generation

## Troubleshooting

### Common Issues

**Very Long Execution Times**: Use shorter timeouts (`--benchmark-timeout 5`)

**Inconsistent Results**: Increase warmup runs (`--benchmark-warmup 10`)

**Memory Issues**: Reduce concurrent operations, benchmark individually

**File Not Found Errors**: Ensure solution files exist and are properly formatted

### Performance Tips

1. **Close other applications** when doing thorough benchmarks
2. **Run multiple times** and compare results for important measurements  
3. **Use consistent environment** (same machine, similar system load)
4. **Start with fast presets** before doing detailed analysis
5. **Save results** to track improvements over time

## Hardware Information

All year-specific benchmark result markdown files automatically include hardware information to provide context for the performance measurements. This includes:

- **Operating System**: OS name and version
- **Python Version**: Python interpreter version used
- **Processor**: CPU model and specifications
- **CPU Cores**: Number of available CPU cores

### Example Output

```markdown
## 💻 System Information

- **OS**: Windows 11
- **Python**: 3.12.10
- **Processor**: Intel64 Family 6 Model 183 Stepping 1, GenuineIntel
- **CPU Cores**: 24
```

### Viewing Hardware Info

To see your system's hardware information:

```bash
python -c "from utils.hardware_info import format_hardware_info; print(format_hardware_info())"
```

Or run the demo script:

```bash
python utils/demo_hardware_info.py
```

This information is automatically included when you generate or update markdown files:

```bash
# Update year results (includes hardware info)
python main.py --markdown-year 2025

# Update all markdown files
python main.py --markdown-all
```

### Why Hardware Info Matters

Hardware information helps you:
- **Compare results** across different machines
- **Share benchmarks** with meaningful context
- **Track performance** as you upgrade hardware
- **Document environment** for reproducibility

## Integration with Tracking

The benchmark system integrates with the existing performance tracking:

- Individual solution runs are automatically tracked
- Benchmark results provide additional statistical analysis
- Both systems use the same underlying timing mechanisms
- Results can be cross-referenced for comprehensive performance history

## Examples and Use Cases

See `python benchmark_quick.py --examples` for comprehensive usage examples and common workflows.
