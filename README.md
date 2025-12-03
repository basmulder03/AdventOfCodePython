# Advent of Code Python Solutions

A comprehensive solution runner for [Advent of Code](https://adventofcode.com/) challenges with performance tracking, automated submission, and statistics generation.

## ✨ Features

- 🎄 **Solution Runner**: Execute AOC solutions with timing and error handling
- 📊 **Performance Tracking**: Track execution times and compare with previous runs  
- 🚀 **Auto Submission**: Submit answers directly to AOC with smart timeout handling
- 📈 **Statistics**: Generate comprehensive stats tables from tracked data
- 🎯 **Sample Input Support**: Test with sample data or custom input strings
- 📝 **Template Generation**: Auto-create solution templates for new problems
- 🎨 **Colorized Output**: Beautiful terminal output with progress indicators

## 🚀 Quick Start

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

**Need more details?** Check the [Installation & Setup Guide](docs/setup.md) for comprehensive instructions.

## 📖 Documentation

- **[📋 Installation & Setup](docs/setup.md)** - Detailed setup instructions
- **[⌨️ CLI Reference](docs/cli-reference.md)** - Complete command-line documentation  
- **[✍️ Solution Writing Guide](docs/solution-guide.md)** - How to write effective solutions
- **[📊 Performance Tracking](docs/tracking.md)** - Understanding the tracking system
- **[🏃 Benchmarking](docs/benchmarking.md)** - Performance analysis tools
- **[📈 Statistics](docs/statistics.md)** - Statistics generation and analysis
- **[🏗️ Project Structure](docs/project-structure.md)** - Understanding the codebase

## 💡 Quick Examples

```bash
# Run both parts for day 1 of 2025
python main.py 2025 1

# Test with sample input
python main.py 2025 1 --sample

# Submit answer to AOC  
python main.py 2025 1 --submit

# Show run history
python main.py 2025 1 --history

# Generate statistics
python main.py --stats
```

**See more examples in the [CLI Reference](docs/cli-reference.md)**

<!-- STATS_START -->
## 🎄 Overall Statistics

**Summary Across All Years (2015-2025):**
- ⭐ Total Stars: 52
- 🧩 Total Problems Solved: 56
- 🏃 Total Runs: 118 (89.8% success)
- ⚡ Average Time: 565.0ms
- 🚀 Fastest Time: 0.2μs
- 🐌 Slowest Time: 11.54s


## 2025 Statistics

**Year Summary:**
- ⭐ Stars: 0
- 🧩 Problems Solved: 6
- 🏃 Total Runs: 18 (83.3% success)
- ⚡ Average Time: 147.7ms
- 🚀 Fastest Time: 556.5μs

**Best Times by Day:**

| Day | Part 1 | Part 2 | Total |
|-----|--------|--------|-------|
|  1 | 556.5μs | 750.7μs |   1.3ms |
|  2 | 295.2ms | 768.3ms |   1.06s |
|  3 |   1.7ms |   2.3ms |   4.0ms |

## 2015 Statistics

**Year Summary:**
- ⭐ Stars: 50
- 🧩 Problems Solved: 50
- 🏃 Total Runs: 100 (91.0% success)
- ⚡ Average Time: 633.8ms
- 🚀 Fastest Time: 0.2μs

**Best Times by Day:**

| Day | Part 1 | Part 2 | Total |
|-----|--------|--------|-------|
|  1 | 196.6μs |  89.8μs | 286.4μs |
|  2 |   1.9ms | 487.7μs |   2.4ms |
|  3 |   4.5ms |   3.7ms |   8.2ms |
|  4 |  68.0ms |   2.18s |   2.25s |
|  5 |   2.8ms |   8.2ms |  11.0ms |
|  6 |  73.3ms |  18.2ms |  91.5ms |
|  7 | 280.7μs | 501.8μs | 782.5μs |
|  8 | 622.3μs | 320.2μs | 942.5μs |
|  9 |  33.8ms |  23.0ms |  56.8ms |
| 10 | 122.3ms |   2.28s |   2.40s |
| 11 |  19.8ms | 573.9ms | 593.7ms |
| 12 |   2.4ms |   1.4ms |   3.7ms |
| 13 |  19.2ms |  67.6ms |  86.8ms |
| 14 | 406.2μs |  11.0ms |  11.4ms |
| 15 | 407.4ms | 450.1ms | 857.5ms |
| 16 | 320.1μs | 689.6μs |   1.0ms |
| 17 |  17.9ms |  10.4ms |  28.3ms |
| 18 | 909.3ms | 913.9ms |   1.82s |
| 19 | 355.4μs |   1.5ms |   1.8ms |
| 20 |   2.16s |   6.18s |   8.34s |
| 21 |   1.5ms |   2.6ms |   4.1ms |
| 22 |  14.9ms |   5.6ms |  20.5ms |
| 23 |  10.0μs |  22.4μs |  32.4μs |
| 24 | 130.9ms | 444.4ms | 575.3ms |
| 25 | 709.4ms |   0.2μs | 709.4ms |

*Last updated: 2025-12-03 16:07:54*
<!-- STATS_END -->

## 📋 Requirements

- Python 3.7+
- `requests` (for AOC communication)
- `colorama` (optional, for colored output)

## 📄 License

This project is for educational purposes. Please respect Advent of Code's [terms of service](https://adventofcode.com/about).
