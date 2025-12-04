from typing import Any


def solve_part_1(input_data: str) -> Any:
    # Analysis of the assembly code shows it computes:
    # 1. d = a + 4*633 = a + 2532
    # 2. Then it outputs alternating bits from the binary representation
    # We need the smallest a where (a + 2532) produces alternating 0,1,0,1...

    # The pattern 010101... in binary is 0x2AAAAAAA...
    # We need to find the smallest a such that a + 2532 has this pattern

    target = 2532
    # Looking for pattern that starts with 01010101...
    # This corresponds to values like 0b101010101...

    # Try powers of 2 that would give us alternating bits
    for i in range(12):  # reasonable upper bound
        # Pattern 0b10101010... (0xAA prefix)
        candidate = (0b101010101010 << i) - target
        if candidate > 0:
            # Verify by simulation with limited steps
            if verify_clock_signal(input_data, candidate, 20):
                return candidate

        # Pattern 0b01010101... (0x55 prefix)
        candidate = (0b010101010101 << i) - target
        if candidate > 0:
            if verify_clock_signal(input_data, candidate, 20):
                return candidate

    # Fallback to original method if pattern matching fails
    return solve_part_1_original(input_data)

def verify_clock_signal(input_data: str, a: int, max_outputs: int = 20) -> bool:
    """Fast verification of clock signal pattern"""
    ls = input_data.strip().split('\n')
    r = {'a': a, 'b': 0, 'c': 0, 'd': 0}
    i = 0
    outputs = []

    while i < len(ls) and len(outputs) < max_outputs:
        p = ls[i].split()
        if p[0] == 'cpy':
            v = r[p[1]] if p[1] in r else int(p[1])
            if p[2] in r:
                r[p[2]] = v
        elif p[0] == 'inc':
            if p[1] in r:
                r[p[1]] += 1
        elif p[0] == 'dec':
            if p[1] in r:
                r[p[1]] -= 1
        elif p[0] == 'jnz':
            v = r[p[1]] if p[1] in r else int(p[1])
            if v != 0:
                j = r[p[2]] if p[2] in r else int(p[2])
                i += j
                continue
        elif p[0] == 'out':
            v = r[p[1]] if p[1] in r else int(p[1])
            outputs.append(v)
            if len(outputs) >= 2 and outputs[-1] == outputs[-2]:
                return False  # Not alternating
        i += 1

    return outputs == [i % 2 for i in range(len(outputs))]

def solve_part_1_original(input_data: str) -> Any:
    """Original brute force method as fallback"""
    ls = input_data.strip().split('\n')
    for a in range(1000):
        if verify_clock_signal(input_data, a, 50):
            return a


def solve_part_2(input_data: str) -> Any:
    return 'Merry Christmas!'

