"""
Demo script to show hardware information functionality.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.hardware_info import get_hardware_info, format_hardware_info, format_hardware_info_compact


def main():
    print("=" * 60)
    print("Hardware Information Demo")
    print("=" * 60)
    print()

    # Get raw hardware info
    hw_info = get_hardware_info()

    print("1. Raw Hardware Info Dictionary:")
    print("-" * 60)
    for key, value in hw_info.items():
        print(f"  {key}: {value}")
    print()

    # Formatted for markdown (full)
    print("2. Formatted for Markdown (Full):")
    print("-" * 60)
    print(format_hardware_info(hw_info))

    # Compact format
    print("3. Compact Format:")
    print("-" * 60)
    print(format_hardware_info_compact(hw_info))
    print()

    print("=" * 60)
    print("This hardware information is now automatically included in")
    print("year-specific benchmark result markdown files!")
    print("=" * 60)


if __name__ == "__main__":
    main()

