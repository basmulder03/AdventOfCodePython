# Statistics Generation

Learn how the statistics system works and how to generate comprehensive performance reports.

## Overview

The statistics system analyzes your performance tracking data to generate:
- **Overall summaries** across all years
- **Year-specific breakdowns** with detailed metrics
- **Best time tables** showing your fastest solutions
- **Success rate analysis** and run counts
- **Automatic README updates** to showcase your progress

## Generating Statistics

### Basic Usage

```bash
# Generate all statistics
python main.py --stats
```

This will display:
1. Overall summary across all years
2. Year-by-year breakdowns
3. Best times tables for each year
4. Formatted output ready for documentation

### Filtering by Year

```bash
# Show only 2025 statistics
python main.py --stats --year-filter 2025
```

### Updating Documentation

```bash
# Generate stats and update README.md
python main.py --stats --update-readme
```

This automatically updates the `<!-- STATS_START -->` to `<!-- STATS_END -->` section in your README.md file.

## Statistics Structure

### Overall Summary

The overall summary shows aggregated data across all years:

```
🎄 Overall Statistics

Summary Across All Years (2015-2025):
- ⭐ Total Stars: 48
- 🧩 Total Problems Solved: 48  
- 🏃 Total Runs: 67 (100.0% success)
- ⚡ Average Time: 786.3ms
- 🚀 Fastest Time: 0.010ms
- 🐌 Slowest Time: 11.54s
```

**Metrics Explained:**
- **Stars:** Total stars earned (based on completed parts)
- **Problems Solved:** Unique day/part combinations with successful runs
- **Total Runs:** All recorded executions and their success rate
- **Average Time:** Mean execution time across all successful runs
- **Fastest/Slowest:** Best and worst individual execution times

### Year Summary

Each year gets a detailed breakdown:

```
## 2025 Statistics

Year Summary:
- ⭐ Stars: 6
- 🧩 Problems Solved: 3
- 🏃 Total Runs: 8 (100.0% success)
- ⚡ Average Time: 2.6ms
- 🚀 Fastest Time: 1.7ms
```

### Best Times Table

Shows your personal best times for each completed day:

```
Best Times by Day:

| Day | Part 1 | Part 2 | Total |
|-----|--------|--------|-------|
|  1  | 0.326ms | 0.090ms | 0.415ms |
|  2  |   1.9ms | 0.488ms |   2.4ms |
|  3  |   4.5ms |   3.7ms |   8.2ms |
```

**Table Details:**
- **Day:** The problem day (1-25)
- **Part 1/2:** Best execution time for each part
- **Total:** Sum of both parts' best times
- Missing entries indicate unsolved problems

## Data Sources

### Database Queries

Statistics are generated from the `aoc_tracking.db` database:

```sql
-- Problems solved (unique day/part combinations)
SELECT COUNT(DISTINCT year || '-' || day || '-' || part) 
FROM runs WHERE success = 1;

-- Best times per problem
SELECT year, day, part, MIN(execution_time_ms) as best_time
FROM runs 
WHERE success = 1 
GROUP BY year, day, part;

-- Success rates
SELECT 
  COUNT(*) as total_runs,
  SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_runs
FROM runs;
```

### Star Calculation

Stars are calculated based on completed parts:
- **Part 1 complete:** 1 star
- **Both parts complete:** 2 stars
- **Incomplete:** 0 stars

The system automatically detects which parts you've solved based on successful runs in the database.

## README Integration

### Automatic Updates

When you use `--stats --update-readme`, the system:

1. **Finds markers:** Locates `<!-- STATS_START -->` and `<!-- STATS_END -->` in README.md
2. **Replaces content:** Overwrites everything between the markers
3. **Preserves formatting:** Maintains consistent markdown structure  
4. **Updates timestamp:** Adds "Last updated" timestamp

### Manual Integration

If you want to customize the README integration:

```markdown
<!-- STATS_START -->
Your statistics will be inserted here
<!-- STATS_END -->
```

### Customizing Format

The statistics output uses markdown formatting:
- **Headers:** `## Year Statistics`
- **Emoji indicators:** 🎄⭐🧩🏃⚡🚀🐌
- **Tables:** Standard markdown table format
- **Code blocks:** For time values and numbers

## Performance Insights

### Interpreting the Data

**Average Times:**
- **Sub-millisecond:** Very fast solutions (usually simple problems)
- **1-10ms:** Fast solutions (good algorithmic complexity)
- **10-100ms:** Moderate solutions (may have room for optimization)
- **100ms+:** Slower solutions (complex problems or suboptimal algorithms)

**Success Rates:**
- **100%:** All runs successful (stable solutions)
- **<100%:** Some failed runs (might indicate buggy or incomplete solutions)

**Run Counts:**
- **High counts:** Lots of testing/optimization iterations
- **Low counts:** Solutions worked well from the start

### Tracking Progress

Use statistics to track your improvement over time:

1. **Compare years:** See if your average times are improving
2. **Identify patterns:** Which types of problems are you fastest at?
3. **Find optimization targets:** Focus on your slowest solutions
4. **Celebrate milestones:** Track your star count growth

## Advanced Features

### Custom Analysis

You can query the database directly for custom statistics:

```python
import sqlite3

conn = sqlite3.connect('aoc_tracking.db')

# Custom query: average time by year
results = conn.execute('''
    SELECT year, AVG(execution_time_ms) as avg_time, COUNT(*) as runs
    FROM runs 
    WHERE success = 1 
    GROUP BY year 
    ORDER BY year
''').fetchall()

for year, avg_time, runs in results:
    print(f"{year}: {avg_time:.1f}ms average ({runs} runs)")
```

### Export Options

While not built-in, you can easily export statistics:

```bash
# Generate stats and save to file
python main.py --stats > stats_output.md

# JSON export (custom script needed)
python custom_export.py --format json > stats.json
```

### Integration with Other Tools

Statistics can be integrated with:
- **GitHub Actions:** Auto-update README on solution commits
- **Progress tracking:** Monitor your AOC completion over time  
- **Performance dashboards:** Visualize your solving trends
- **Social sharing:** Share your progress and best times

## Troubleshooting

### Missing Statistics

**Problem:** No statistics shown or very low counts

**Solutions:**
- Run some solutions to populate the tracking database
- Check that tracking isn't disabled (`--no-tracking`)
- Verify the database file exists and isn't corrupted

### Incorrect Times

**Problem:** Times seem wrong or inconsistent

**Solutions:**
- Times include Python startup and input parsing
- Single runs can vary due to system load
- Use benchmarking for more accurate measurements

### README Not Updating

**Problem:** `--update-readme` doesn't modify the file

**Solutions:**
- Ensure `<!-- STATS_START -->` and `<!-- STATS_END -->` markers exist in README.md
- Check file permissions - the script needs write access
- Verify you're in the correct directory

## Best Practices

### Regular Updates

- **Generate stats regularly** to track your progress
- **Update README frequently** to showcase your improvements  
- **Use year filters** when working on specific years

### Performance Analysis

- **Look for patterns** in your solving times
- **Identify optimization opportunities** from slowest solutions
- **Track improvement trends** over time

### Documentation

- **Keep README current** with automated updates
- **Add context** to your statistics (what optimizations you made)
- **Share insights** about interesting performance discoveries

## Next Steps

- Learn more about [Performance Tracking](tracking.md) to understand the underlying data
- Check out [Benchmarking](benchmarking.md) for more detailed performance analysis  
- Read [Database Publishing](database-publishing.md) for advanced benchmark integration
