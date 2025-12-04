# Output Validation

The CLI now supports validating solution outputs against expected values. This is useful for:
- Testing with sample inputs where the expected output is known
- Regression testing to ensure solutions still produce correct results
- Benchmarking with validation to ensure performance optimizations don't break correctness

## Usage

### Basic Validation

Validate a single part with `--expected`:

```bash
# Run part 1 with validation
python main.py 2025 1 --part 1 --expected 12345

# Run with sample input and validate
python main.py 2025 1 --part 1 --sample-input "1\n2\n3" --expected 6
```

### Validating Both Parts

Use `--expected-p1` and `--expected-p2` to validate both parts in a single run:

```bash
# Run both parts with validation
python main.py 2025 1 --expected-p1 12345 --expected-p2 67890

# With sample input
python main.py 2025 1 --sample-input "test data" --expected-p1 100 --expected-p2 200
```

### Validation with Benchmarking

Validation works seamlessly with benchmarking:

```bash
# Benchmark a single part with validation
python main.py benchmark 2025 1 --part 1 --runs 10 --expected 12345

# Benchmark both parts with validation
python main.py benchmark 2025 1 --expected-p1 12345 --expected-p2 67890

# Quick benchmark with validation
python benchmarking/quick.py fast 2025 1 --expected-p1 12345 --expected-p2 67890
```

## Output Examples

### Successful Validation

When the output matches the expected value:

```
Part 1: 12345 (5.23ms)
✅ Part 1 validation PASSED: 12345
```

### Failed Validation

When the output doesn't match:

```
Part 1: 12340 (5.23ms)
❌ Part 1 validation FAILED:
   Expected: 12345
   Got:      12340
```

### Benchmark Validation

During benchmarking, validation status appears inline with timing:

```
Warmup 1/3: 5.234ms ✅
  Run 1/10: 5.123ms ✅
  Run 2/10: 5.234ms ✅
  Run 3/10: 5.345ms ✅

📊 Part 1 Statistics:
  Success Rate: 100.0% (10/10)
  Validation:   ✅ 10/10 passed (expected: 12345)
  Min Time:     5.123ms
  Max Time:     5.456ms
  Mean Time:    5.234ms
```

If validation fails:

```
📊 Part 1 Statistics:
  Success Rate: 100.0% (10/10)
  Validation:   ❌ 0/10 passed (0.0%)
                Expected: 12345
  Min Time:     5.123ms
```

## Use Cases

### 1. Testing Sample Inputs

The official Advent of Code problems provide sample inputs with known outputs. Use validation to verify your solution works correctly:

```bash
python main.py 2025 1 --sample-input "sample data here" --expected-p1 42 --expected-p2 123
```

### 2. Regression Testing

After refactoring or optimizing, ensure the solution still produces correct results:

```bash
# Store your known correct answers
python main.py 2025 1 --expected-p1 12345 --expected-p2 67890
```

### 3. Performance Optimization with Safety

When optimizing for speed, validate that correctness is maintained:

```bash
# Benchmark with validation to ensure optimization didn't break correctness
python main.py benchmark 2025 1 --runs 50 --expected-p1 12345 --expected-p2 67890
```

### 4. Continuous Integration

In CI/CD pipelines, validate solutions automatically:

```bash
# Run all solutions with validation
python main.py benchmark --all --runs 3 --expected-p1 VALUE1 --expected-p2 VALUE2
```

## Tips

1. **Whitespace Handling**: The validation automatically strips leading/trailing whitespace from both expected and actual values.

2. **Type Conversion**: All outputs are converted to strings for comparison, so numeric outputs work seamlessly.

3. **Partial Validation**: You can validate only one part by using `--expected` with `--part`, or `--expected-p1` without `--expected-p2`.

4. **No Impact on Performance**: Validation happens after timing measurement, so it doesn't affect benchmark accuracy.

5. **Works with All Input Types**: Validation works with:
   - Sample input (`--sample`)
   - Direct input (`--sample-input`)
   - Regular input files
   - Benchmarking runs

## Integration with Tracking

Validation results are tracked along with execution times when tracking is enabled. This allows you to:
- See historical validation success rates
- Track when solutions started producing incorrect results
- Compare validation results across different implementations

## Command Reference

### Regular Run Mode

| Argument | Description | Example |
|----------|-------------|---------|
| `--expected VALUE` | Validate against VALUE (for single part) | `--expected 12345` |
| `--expected-p1 VALUE` | Validate part 1 against VALUE | `--expected-p1 12345` |
| `--expected-p2 VALUE` | Validate part 2 against VALUE | `--expected-p2 67890` |

### Benchmark Mode

Same arguments work with the `benchmark` subcommand:

```bash
python main.py benchmark 2025 1 --expected-p1 12345 --expected-p2 67890
```

## Troubleshooting

### Validation Always Fails

Check that:
1. The expected value matches exactly (case-sensitive)
2. There's no extra whitespace in the expected value
3. The output type is correct (numbers vs strings)

### Validation Not Showing

Ensure you've provided the validation arguments correctly:
- Use `--expected` with `--part` for single part validation
- Use `--expected-p1` and/or `--expected-p2` for multi-part validation

