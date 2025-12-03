# Quick Reference: Markdown Documentation

## TL;DR

Update all documentation from benchmark results:
```bash
python main.py --update-markdown --markdown-all
```

Benchmark and auto-update:
```bash
python main.py 2025 1 --benchmark --benchmark-publish
```

## Commands

| Command | What it does |
|---------|-------------|
| `--update-markdown --markdown-all` | Update main README + all year files |
| `--update-markdown --markdown-year 2025` | Update specific year + main README |
| `--update-markdown` (with year/day args) | Update based on context |
| `--benchmark --benchmark-publish` | Benchmark + auto-update markdown |

## File Structure

```
README.md                    # Overview table with all years
docs/
  ├── 2025-results.md       # Detailed 2025 stats
  ├── 2015-results.md       # Detailed 2015 stats
  └── markdown-generation.md # Full documentation
```

## Workflow

1. **Solve problems** (with tracking)
2. **Benchmark** with `--benchmark-publish`
3. **Documentation auto-updates** ✨
4. **Commit to git**

Or manually:
```bash
python main.py --update-markdown --markdown-all
```

## Full Documentation

See [markdown-generation.md](markdown-generation.md) for complete guide.

