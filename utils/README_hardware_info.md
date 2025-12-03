# Hardware Information Utility

The hardware information utility automatically collects and formats system information for inclusion in benchmark result markdown files.

## Features

- Automatically detects OS, Python version, processor, and CPU core count
- Formats information for markdown display
- Provides both full and compact formatting options
- Zero configuration required

## Usage

### In Code

```python
from utils.hardware_info import get_hardware_info, format_hardware_info

# Get hardware info dictionary
hw_info = get_hardware_info()

# Format for markdown
markdown = format_hardware_info(hw_info)
print(markdown)
```

### Command Line

View your system's hardware information:

```bash
python -c "from utils.hardware_info import format_hardware_info; print(format_hardware_info())"
```

Or run the demo script:

```bash
python utils/demo_hardware_info.py
```

## Output Example

```markdown
## 💻 System Information

- **OS**: Windows 11
- **Python**: 3.12.10
- **Processor**: Intel64 Family 6 Model 183 Stepping 1, GenuineIntel
- **CPU Cores**: 24
```

## Integration

Hardware information is automatically included in:
- Year-specific benchmark result files (`docs/{year}-results.md`)
- Generated when using `--update-markdown` or `--markdown-year` commands
- No manual intervention required

## Functions

### `get_hardware_info()`
Returns a dictionary with system information:
- `os`: Operating system name
- `os_version`: OS version
- `os_release`: OS release
- `python_version`: Python interpreter version
- `processor`: CPU model
- `machine`: Machine architecture
- `cpu_count`: Number of CPU cores
- `platform`: Full platform string

### `format_hardware_info(info=None)`
Formats hardware information for markdown display with section header and bullet points.

### `format_hardware_info_compact(info=None)`
Returns a compact single-line format of hardware information.

## Why Hardware Info?

Including hardware information in benchmark results is important because:

1. **Context**: Performance numbers are meaningless without knowing the hardware
2. **Comparison**: Compare results across different machines
3. **Tracking**: See how upgrades affect performance
4. **Reproducibility**: Document the environment for others
5. **Sharing**: Share benchmarks with complete context

## See Also

- [Benchmarking Documentation](../docs/benchmarking.md)
- [Markdown Generation Documentation](../docs/markdown-generation.md)

