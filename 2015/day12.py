import json
import re

def solve_part_1(input_data):
    numbers = re.findall(r'-?\d+', input_data.strip())
    return sum(int(num) for num in numbers)

def solve_part_2(input_data):
    data = json.loads(input_data.strip())

    def sum_numbers(obj):
        if isinstance(obj, int):
            return obj
        elif isinstance(obj, list):
            return sum(sum_numbers(item) for item in obj)
        elif isinstance(obj, dict):
            # Check if any value in the dictionary is "red"
            if "red" in obj.values():
                return 0  # Ignore this object and all its children
            return sum(sum_numbers(value) for value in obj.values())
        else:
            # String or other type - no numbers to sum
            return 0

    return sum_numbers(data)
