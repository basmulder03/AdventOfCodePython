import argparse
import importlib
import importlib.util
from time import perf_counter
import os
from input import get_input

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="the year of the AOC challenge")
    parser.add_argument("day", type=int, help="the day of the AOC challenge")
    args = parser.parse_args()

    try:
        # Create a module spec for the specified year and day
        module_name = f"{args.year}/day{args.day}"
        module_path = os.path.join(os.getcwd(), f"{module_name}.py")
        module_spec = importlib.util.spec_from_file_location(
            module_name, module_path)

        # Create a module from the spec
        module = importlib.util.module_from_spec(module_spec)

        # Load the module into memory
        module_spec.loader.exec_module(module)
    except:
        if not str(args.year) in os.listdir(os.getcwd()):
            os.makedirs(str(args.year))
        if not f"day{args.day}.py" in os.listdir(os.path.join(os.getcwd(), str(args.year))):
            with open(os.path.join(os.getcwd(), str(args.year), f"day{args.day}.py"), "w+") as f:
                f.write(
                    f"def solve_part_1(input_data):\n    pass\n\ndef solve_part_2(input_data):\n    pass")
        print("Python script file created. Please fill in the functions.")

    # Get the input data for the specified day
    input_data = get_input(args.year, args.day)

    # Print header
    print("\n" + "=" * 60)
    if COLOR_SUPPORT:
        print(f"{Fore.CYAN}{Style.BRIGHT}🎄 Advent of Code {args.year} - Day {args.day} 🎄{Style.RESET_ALL}")
    else:
        print(f"Advent of Code {args.year} - Day {args.day}")
    print("=" * 60 + "\n")

    total_time = 0

    try:
        # Measure the elapsed time for solving Part 1
        start_time = perf_counter()
        result_1 = module.solve_part_1(input_data)
        end_time = perf_counter()
        elapsed_time = end_time - start_time

        # Print the result and elapsed time for Part 1
        if COLOR_SUPPORT:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⭐ Part 1:{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}Answer: {Style.BRIGHT}{result_1}{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}Time: {elapsed_time * 1000:.3f} ms{Style.RESET_ALL}")
        else:
            print(f"Part 1:")
            print(f"  Answer: {result_1}")
            print(f"  Time: {elapsed_time * 1000:.3f} ms")
        print()
        total_time += elapsed_time
    except Exception as e:
        if COLOR_SUPPORT:
            print(f"{Fore.RED}❌ Part 1 Error: {e}{Style.RESET_ALL}\n")
        else:
            print(f"Part 1 Error: {e}\n")

    try:
        # Measure the elapsed time for solving Part 2
        start_time = perf_counter()
        result_2 = module.solve_part_2(input_data)
        end_time = perf_counter()
        elapsed_time = end_time - start_time

        # Print the result and elapsed time for Part 2
        if COLOR_SUPPORT:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⭐ Part 2:{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}Answer: {Style.BRIGHT}{result_2}{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}Time: {elapsed_time * 1000:.3f} ms{Style.RESET_ALL}")
        else:
            print(f"Part 2:")
            print(f"  Answer: {result_2}")
            print(f"  Time: {elapsed_time * 1000:.3f} ms")
        print()
        total_time += elapsed_time
    except Exception as e:
        if COLOR_SUPPORT:
            print(f"{Fore.RED}❌ Part 2 Error: {e}{Style.RESET_ALL}\n")
        else:
            print(f"Part 2 Error: {e}\n")

    # Print footer with total time
    print("-" * 60)
    if COLOR_SUPPORT:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}⏱️  Total Time: {total_time * 1000:.3f} ms{Style.RESET_ALL}")
    else:
        print(f"Total Time: {total_time * 1000:.3f} ms")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
