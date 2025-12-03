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
- **[📝 Markdown Generation](docs/markdown-generation.md)** - Auto-generate documentation from benchmarks
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

# Benchmark and auto-update documentation
python main.py 2025 1 --benchmark --benchmark-publish

# Update all documentation files
python main.py --update-markdown --markdown-all
```

**See more examples in the [CLI Reference](docs/cli-reference.md)**

<!-- STATS_START -->
## 🎄 Solutions Overview

| Year | Stars ⭐ | Problems 🧩 | Runs 🏃 | Success Rate | Avg Time ⚡ | Fastest 🚀 | Slowest 🐌 |
|------|----------|-------------|---------|--------------|-------------|------------|------------|
| [2025](./docs/2025-results.md) | 0 | 6 | 29 | 89.7% | 85.5ms | 556.5μs | 771.9ms |
| [2016](./docs/2016-results.md) | 50 | 50 | 602 | 99.5% | 1.36s | 0.2μs | 20.03s |
| [2015](./docs/2015-results.md) | 50 | 50 | 604 | 95.0% | 351.7ms | 0.2μs | 11.54s |

### Overall Totals
- ⭐ **Total Stars**: 100
- 🧩 **Total Problems Solved**: 106
- 🏃 **Total Runs**: 1235 (97.1% success)
- ⚡ **Average Time**: 847.2ms
- 🚀 **Fastest Time**: 0.2μs
- 🐌 **Slowest Time**: 20.03s

*Last updated: 2025-12-03 21:28:21*
<!-- STATS_END -->

## 📋 Requirements

- Python 3.7+
- `requests` (for AOC communication)
- `colorama` (optional, for colored output)

## 📄 License

This project is for educational purposes. Please respect Advent of Code's [terms of service](https://adventofcode.com/about).
