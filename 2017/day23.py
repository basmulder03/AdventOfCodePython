from collections import defaultdict


def solve_part_1(input_data):
    """Coprocessor conflagration - count mul instructions."""
    lines = input_data.strip().split('\n')
    registers = defaultdict(int)
    pc = 0
    mul_count = 0

    def get_value(x):
        if x.lstrip('-').isdigit():
            return int(x)
        return registers[x]

    while 0 <= pc < len(lines):
        parts = lines[pc].split()
        cmd = parts[0]

        if cmd == 'set':
            registers[parts[1]] = get_value(parts[2])
        elif cmd == 'sub':
            registers[parts[1]] -= get_value(parts[2])
        elif cmd == 'mul':
            registers[parts[1]] *= get_value(parts[2])
            mul_count += 1
        elif cmd == 'jnz':
            if get_value(parts[1]) != 0:
                pc += get_value(parts[2])
                continue

        pc += 1

    return mul_count


def solve_part_2(input_data):
    """Coprocessor conflagration - optimized version."""
    # The program is checking for composite numbers in a range
    # We can determine this by analyzing the assembly code

    # From analyzing typical AoC 2017 day 23 input:
    # The program counts non-prime numbers between b and c (inclusive)
    # where b starts at some value and c = b + 17000
    # and it steps by 17

    # Parse to find the initial values
    lines = input_data.strip().split('\n')

    # Usually b is set in the first few instructions
    # For the general case, let's simulate just the initialization
    registers = defaultdict(int)
    registers['a'] = 1  # Part 2 starts with a=1

    # Run initial setup (usually first ~8 instructions before the main loop)
    for i in range(min(8, len(lines))):
        parts = lines[i].split()
        cmd = parts[0]

        def get_value(x):
            if x.lstrip('-').isdigit():
                return int(x)
            return registers[x]

        if cmd == 'set':
            registers[parts[1]] = get_value(parts[2])
        elif cmd == 'sub':
            registers[parts[1]] -= get_value(parts[2])
        elif cmd == 'mul':
            registers[parts[1]] *= get_value(parts[2])

    # Extract b value (typically set early in the program)
    b = registers['b']
    c = b + 17000

    # Count composite numbers between b and c, step by 17
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    h = 0
    for num in range(b, c + 1, 17):
        if not is_prime(num):
            h += 1

    return h
