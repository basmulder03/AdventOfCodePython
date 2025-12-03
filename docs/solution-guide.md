# Solution Writing Guide

Learn how to write effective Advent of Code solutions with this runner system.

## Solution Structure

### Template

When you run a new day, the system automatically creates a template:

```python
from typing import Any

def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    pass

def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    pass
```

### Key Points

- **Function Names:** Must be exactly `solve_part_1` and `solve_part_2`
- **Input Parameter:** Always `input_data: str` - the raw input as a string
- **Return Type:** Can be any type (`int`, `str`, `list`, etc.) - will be converted to string for display
- **Input Processing:** You handle parsing the input string yourself

## Best Practices

### Input Processing

```python
def solve_part_1(input_data: str) -> int:
    # Remove trailing whitespace
    lines = input_data.strip().split('\n')
    
    # Process each line
    numbers = [int(line) for line in lines]
    
    return sum(numbers)
```

### Code Organization

```python
def parse_input(input_data: str) -> list[int]:
    """Parse input into a usable format."""
    return [int(line) for line in input_data.strip().split('\n')]

def solve_part_1(input_data: str) -> int:
    numbers = parse_input(input_data)
    return sum(numbers)

def solve_part_2(input_data: str) -> int:
    numbers = parse_input(input_data)
    return sum(x * 2 for x in numbers)
```

### Error Handling

The runner handles most errors gracefully, but you can add your own:

```python
def solve_part_1(input_data: str) -> int:
    try:
        lines = input_data.strip().split('\n')
        if not lines:
            raise ValueError("Empty input")
        return int(lines[0])
    except ValueError as e:
        print(f"Error parsing input: {e}")
        raise
```

## Testing with Sample Input

### Using Sample Files

Create sample input files in the `input/YYYY/` directory:

```
input/
└── 2025/
    ├── day1.txt          # Actual input
    └── day1_sample.txt   # Sample input
```

Run with sample:
```bash
python main.py 2025 1 --sample
```

### Inline Sample Input

For quick testing:
```bash
python main.py 2025 1 --sample-input "1\n2\n3\n4\n5"
```

## Performance Considerations

### Optimization Tips

1. **Use appropriate data structures:**
   ```python
   # Good for lookups
   seen = set()
   
   # Good for counting
   from collections import Counter
   counts = Counter(items)
   ```

2. **Avoid unnecessary work:**
   ```python
   # Don't recalculate in loops
   def solve_part_1(input_data: str) -> int:
       lines = input_data.strip().split('\n')
       total = 0
       for line in lines:
           # Process line once
           processed = expensive_operation(line)
           total += processed
       return total
   ```

3. **Consider algorithmic complexity:**
   - O(n²) solutions might be too slow for large inputs
   - Look for patterns that allow O(n log n) or O(n) solutions

### Benchmarking

Use the built-in benchmarking to measure performance:

```bash
# Benchmark your solution
python main.py 2025 1 --benchmark

# Compare different approaches by editing and re-running
python main.py 2025 1 --benchmark --benchmark-runs 10
```

## Common Patterns

### Grid/Map Problems

```python
def parse_grid(input_data: str) -> dict[tuple[int, int], str]:
    """Parse input into a coordinate dictionary."""
    grid = {}
    lines = input_data.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid

def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    """Get 4-directional neighbors."""
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
```

### Path Finding

```python
from collections import deque

def bfs(start, end, is_valid):
    queue = deque([(start, 0)])  # (position, distance)
    visited = {start}
    
    while queue:
        pos, dist = queue.popleft()
        if pos == end:
            return dist
            
        for next_pos in get_neighbors(*pos):
            if next_pos not in visited and is_valid(next_pos):
                visited.add(next_pos)
                queue.append((next_pos, dist + 1))
    
    return -1  # No path found
```

### Parsing Complex Input

```python
def parse_complex_input(input_data: str):
    sections = input_data.strip().split('\n\n')
    
    # First section: rules
    rules = {}
    for line in sections[0].split('\n'):
        key, value = line.split(': ')
        rules[key] = int(value)
    
    # Second section: items
    items = []
    for line in sections[1].split('\n'):
        items.append(line.split(','))
    
    return rules, items
```

## Debugging Tips

### Print Debugging

```python
def solve_part_1(input_data: str) -> int:
    lines = input_data.strip().split('\n')
    
    # Debug: see what we're working with
    print(f"Processing {len(lines)} lines")
    print(f"First line: {lines[0]}")
    
    result = process_lines(lines)
    
    # Debug: check intermediate results
    print(f"Intermediate result: {result}")
    
    return result
```

### Sample Input Testing

Always test with sample input first:
```bash
# Test with sample before submitting
python main.py 2025 1 --sample
```

### Performance Tracking

Use the history to see if your changes improved performance:
```bash
python main.py 2025 1 --history
```

## File Organization

Keep your solution files organized:

```
2025/
├── day1.py     # Simple problems can be in one file
├── day5.py     # More complex problems might need helpers
└── day5_helpers.py  # Helper functions for day 5
```

For complex solutions, you can import helpers:
```python
from .day5_helpers import parse_input, complex_algorithm

def solve_part_1(input_data: str) -> int:
    data = parse_input(input_data)
    return complex_algorithm(data)
```

## Next Steps

- Check out [Performance Tracking](tracking.md) to understand how your solutions are benchmarked
- Read [Benchmarking](benchmarking.md) for detailed performance analysis
- See [CLI Reference](cli-reference.md) for all available commands
