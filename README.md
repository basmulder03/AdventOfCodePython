# Advent of Code Python Solutions

A comprehensive solution runner for [Advent of Code](https://adventofcode.com/) challenges with performance tracking, automated submission, and statistics generation.

## ✨ Features

- 🎄 **Solution Runner**: Execute AOC solutions with timing and error handling
- 📊 **Performance Tracking**: Track execution times and compare with previous runs  
- 🚀 **Auto Submission**: Submit answers directly to AOC with smart timeout handling
- 📈 **Statistics**: Generate comprehensive stats tables from tracked data
- 🎯 **Sample Input Support**: Test with sample data or custom input strings
- 🎬 **Algorithm Animations**: Interactive 3D visualizations with matplotlib and GIF export capabilities
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
- **[🎬 Algorithm Animations](docs/animation.md)** - Create and export animated visualizations
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

# Interactive 3D animation (if available)
python main.py 2025 8 --animation --sample

# Export 3D animation as GIF
python main.py animation 2025 8 --sample --export-gif my_3d_animation.gif

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
| [2025](./docs/2025-results.md) | 16 | 16 | 397 | 98.7% | 137.3ms | 0.1ms | 937.8ms |
| [2024](./docs/2024-results.md) | 50 | 2 | 61 | 100.0% | 6.7μs | 0.2μs | 0.3ms |
| [2023](./docs/2023-results.md) | 50 | 15 | 603 | 77.9% | 27.1ms | 0.4μs | 712.2ms |
| [2022](./docs/2022-results.md) | 50 | 2 | 61 | 100.0% | 6.9μs | 0.3μs | 0.3ms |
| [2021](./docs/2021-results.md) | 6 | 6 | 210 | 85.7% | 0.7ms | 0.2ms | 3.3ms |
| [2017](./docs/2017-results.md) | 49 | 50 | 1217 | 89.0% | 663.3ms | 0.6μs | 8.36s |
| [2016](./docs/2016-results.md) | 50 | 50 | 2102 | 98.9% | 1.45s | 0.1μs | 28.77s |
| [2015](./docs/2015-results.md) | 50 | 50 | 2104 | 95.7% | 345.9ms | 0.2μs | 11.54s |

### Overall Totals
- ⭐ **Total Stars**: 323
- 🧩 **Total Problems Solved**: 191
- 🏃 **Total Runs**: 6755 (93.8% success)
- ⚡ **Average Time**: 710.2ms
- 🚀 **Fastest Time**: 0.1μs
- 🐌 **Slowest Time**: 28.77s

*Last updated: 2025-12-08 06:33:18*
<!-- STATS_END -->

## 📋 Requirements

- Python 3.7+
- `requests` (for AOC communication)
- `matplotlib` (for 3D animations)
- `Pillow` (for GIF export)
- `colorama` (optional, for colored output)

## 📄 License

This project is for educational purposes. Please respect Advent of Code's [terms of service](https://adventofcode.com/about).
