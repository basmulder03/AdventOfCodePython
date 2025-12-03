# Installation & Setup

This guide will help you get the Advent of Code Python solution runner up and running.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An Advent of Code account

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AdventOfCodePython
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Session Cookie

To automatically fetch input and submit answers, you need your AOC session cookie:

1. **Get Your Session Cookie:**
   - Log in to [Advent of Code](https://adventofcode.com/)
   - Open your browser's developer tools (F12)
   - Go to the Network tab
   - Refresh the page
   - Find any request to `adventofcode.com`
   - In the request headers, find the `Cookie` header
   - Copy the value of `session=<long_string>`

2. **Save the Session Cookie:**
   ```bash
   echo "your_session_cookie_here" > session_cookie.txt
   ```

   **Important:** Keep your session cookie private! Add `session_cookie.txt` to your `.gitignore` if sharing this code.

## Verification

Test your setup by running a solution:

```bash
# This should work if you have a solution for 2025 day 1
python main.py 2025 1
```

If everything is set up correctly, you should see:
- Input automatically fetched
- Solution executed with timing
- Results displayed with performance comparison

## Configuration

### Optional: Colorized Output

For the best experience, install colorama for colorized terminal output:

```bash
pip install colorama
```

### Database Location

The performance tracking database (`aoc_tracking.db`) will be created automatically in the project root when you first run a solution.

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check that you're using the correct Python version

**"Session cookie invalid" errors:**
- Verify your session cookie is correct and not expired
- Session cookies expire after about a month - you may need to get a new one

**"Input file not found" errors:**
- Make sure your session cookie is set up correctly
- The system should automatically fetch input files on first run

**Permission errors:**
- Make sure you have write permissions in the project directory
- The system needs to create/modify files for tracking and input storage

### Getting Help

If you're still having issues:
1. Check that all files are in the correct locations
2. Verify your Python version: `python --version`
3. Try running with verbose output (if available)
4. Check the GitHub issues for similar problems

## Next Steps

Once everything is working:
- Read the [CLI Reference](cli-reference.md) for all available commands
- Check out the [Solution Writing Guide](solution-guide.md) for tips on writing solutions
- Explore [Performance Tracking](tracking.md) to understand the benchmarking features
