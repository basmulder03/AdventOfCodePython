#!/usr/bin/env python3
"""
Quick benchmark utility for Advent of Code solutions.
This provides common benchmarking scenarios with sensible defaults.
"""

import argparse
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from main
sys.path.insert(0, str(Path(__file__).parent))

from benchmark import BenchmarkRunner

def quick_benchmark():
    """Quick benchmark utility with preset scenarios."""
    parser = argparse.ArgumentParser(
        description="Quick Advent of Code Benchmark Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s fast 2025 1        # Quick test (3 runs, 5s timeout)
  %(prog)s normal 2025 1      # Normal benchmark (10 runs, 30s timeout)  
  %(prog)s thorough 2025 1    # Thorough benchmark (25 runs, 60s timeout)
  %(prog)s fast-year 2025     # Quick benchmark all of 2025
  %(prog)s fast-all           # Quick benchmark everything (WARNING: May take a while!)
  
Presets:
  fast     - 3 runs, 2 warmup, 5s timeout (good for quick checks)
  normal   - 10 runs, 3 warmup, 30s timeout (standard benchmarking)
  thorough - 25 runs, 5 warmup, 60s timeout (detailed performance analysis)
        """)
    
    subparsers = parser.add_subparsers(dest='command', help='Benchmark preset commands')
    
    # Fast benchmark presets
    fast_parser = subparsers.add_parser('fast', help='Quick benchmark (3 runs, 5s timeout)')
    fast_parser.add_argument('year', type=int, help='Year of the challenge')
    fast_parser.add_argument('day', type=int, help='Day of the challenge')
    fast_parser.add_argument('--part', type=int, choices=[1, 2], help='Specific part only')
    fast_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    # Normal benchmark presets
    normal_parser = subparsers.add_parser('normal', help='Standard benchmark (10 runs, 30s timeout)')
    normal_parser.add_argument('year', type=int, help='Year of the challenge')
    normal_parser.add_argument('day', type=int, help='Day of the challenge')
    normal_parser.add_argument('--part', type=int, choices=[1, 2], help='Specific part only')
    normal_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    # Thorough benchmark presets
    thorough_parser = subparsers.add_parser('thorough', help='Detailed benchmark (25 runs, 60s timeout)')
    thorough_parser.add_argument('year', type=int, help='Year of the challenge')
    thorough_parser.add_argument('day', type=int, help='Day of the challenge')
    thorough_parser.add_argument('--part', type=int, choices=[1, 2], help='Specific part only')
    thorough_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    # Year benchmark presets
    fast_year_parser = subparsers.add_parser('fast-year', help='Quick benchmark all days in year')
    fast_year_parser.add_argument('year', type=int, help='Year to benchmark')
    fast_year_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    normal_year_parser = subparsers.add_parser('normal-year', help='Standard benchmark all days in year')
    normal_year_parser.add_argument('year', type=int, help='Year to benchmark')
    normal_year_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    # All benchmark presets
    fast_all_parser = subparsers.add_parser('fast-all', help='Quick benchmark everything')
    fast_all_parser.add_argument('--save', type=str, nargs='?', const='auto', help='Save results to file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    runner = BenchmarkRunner()
    
    # Define presets
    presets = {
        'fast': {'runs': 3, 'warmup': 2, 'timeout': 5.0},
        'normal': {'runs': 10, 'warmup': 3, 'timeout': 30.0},
        'thorough': {'runs': 25, 'warmup': 5, 'timeout': 60.0}
    }
    
    # Individual day benchmarks
    if args.command in ['fast', 'normal', 'thorough']:
        preset = presets[args.command]
        
        if args.part:
            # Benchmark single part
            print(f"🚀 Running {args.command} benchmark: {args.year} Day {args.day} Part {args.part}")
            stats = runner.benchmark_problem(
                args.year, args.day, args.part,
                runs=preset['runs'], 
                warmup_runs=preset['warmup'],
                timeout=preset['timeout']
            )
            runner.print_benchmark_stats(f"{args.year} Day {args.day} Part {args.part}", stats)
            
            if args.save:
                filename = None if args.save == 'auto' else args.save
                results = {args.year: {args.day: {args.part: stats}}}
                runner.save_benchmark_results(results, filename)
        else:
            # Benchmark full day
            print(f"🚀 Running {args.command} benchmark: {args.year} Day {args.day}")
            results = {args.year: runner.benchmark_day(
                args.year, args.day, 
                runs=preset['runs'],
                timeout=preset['timeout']
            )}
            
            if args.save:
                filename = None if args.save == 'auto' else args.save
                runner.save_benchmark_results(results, filename)
    
    # Year benchmarks
    elif args.command in ['fast-year', 'normal-year']:
        preset_name = args.command.split('-')[0]
        preset = presets[preset_name]
        
        print(f"🚀 Running {preset_name} benchmark for year {args.year}")
        results = runner.benchmark_year(
            args.year,
            runs=preset['runs'],
            timeout=preset['timeout']
        )
        
        if args.save:
            filename = None if args.save == 'auto' else args.save
            runner.save_benchmark_results({args.year: results}, filename)
    
    # All benchmarks
    elif args.command == 'fast-all':
        preset = presets['fast']
        
        print("🚀 Running fast benchmark for all solutions")
        print("⚠️  This may take a while, depending on how many solutions you have!")
        
        results = runner.benchmark_all(
            runs=preset['runs'],
            timeout=preset['timeout']
        )
        
        if args.save:
            filename = None if args.save == 'auto' else args.save
            runner.save_benchmark_results(results, filename)


def show_benchmark_examples():
    """Show benchmark usage examples."""
    examples = """
🎄 Advent of Code Benchmarking Examples

Basic Usage:
  python main.py 2025 1 --benchmark                           # Benchmark both parts
  python main.py 2025 1 --benchmark --part 1                  # Benchmark part 1 only
  python main.py 2025 1 --benchmark --benchmark-runs 20       # More thorough (20 runs)
  python main.py 2025 1 --benchmark --benchmark-timeout 5     # Quick timeout (5s)

Year and All Solutions:
  python main.py --benchmark-year 2025                        # Benchmark all of 2025
  python main.py --benchmark-all --benchmark-runs 1           # Quick test of everything
  python main.py --benchmark-all --benchmark-timeout 10       # Benchmark all (10s limit per problem)

Save Results:
  python main.py 2025 1 --benchmark --benchmark-save          # Auto-generate filename
  python main.py 2025 1 --benchmark --benchmark-save my.json  # Custom filename
  python main.py --benchmark-year 2025 --benchmark-save       # Save year results

Quick Presets (using benchmark_quick.py):
  python benchmark_quick.py fast 2025 1                       # 3 runs, 5s timeout
  python benchmark_quick.py normal 2025 1                     # 10 runs, 30s timeout
  python benchmark_quick.py thorough 2025 1                   # 25 runs, 60s timeout
  python benchmark_quick.py fast-year 2025                    # Quick year benchmark
  python benchmark_quick.py fast-all                          # Quick all benchmark

Comparison Examples:
  # Compare different implementations of the same problem
  python main.py 2025 1 --benchmark --benchmark-runs 15 --benchmark-save before.json
  # ... make changes to your code ...
  python main.py 2025 1 --benchmark --benchmark-runs 15 --benchmark-save after.json
  
  # Find your slowest solutions
  python main.py --benchmark-all --benchmark-runs 3 --benchmark-timeout 5
  
  # Performance regression testing
  python benchmark_quick.py fast-year 2025 --save baseline.json
  # ... after code changes ...
  python benchmark_quick.py fast-year 2025 --save comparison.json

Performance Tips:
  - Use fewer runs (--benchmark-runs 3) for quick checks
  - Use shorter timeouts (--benchmark-timeout 5) to skip slow solutions
  - Use --part 1 or --part 2 to focus on specific parts
  - Save results to track improvements over time
  - Start with 'fast' presets, then use 'normal' or 'thorough' for final measurements
    """
    print(examples)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--examples':
        show_benchmark_examples()
    else:
        quick_benchmark()
