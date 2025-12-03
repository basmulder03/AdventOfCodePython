from typing import Any


def solve_part_1(input_data: str) -> Any:
    s = input_data.strip()
    l = 272
    while len(s) < l:
        b = s[::-1].replace('0', 'x').replace('1', '0').replace('x', '1')
        s = s + '0' + b
    s = s[:l]
    while len(s) % 2 == 0:
        ns = ''
        for i in range(0, len(s), 2):
            ns += '1' if s[i] == s[i+1] else '0'
        s = ns
    return s


def solve_part_2(input_data: str) -> Any:
    s = input_data.strip()
    l = 35651584
    while len(s) < l:
        b = s[::-1].replace('0', 'x').replace('1', '0').replace('x', '1')
        s = s + '0' + b
    s = s[:l]
    while len(s) % 2 == 0:
        ns = ''
        for i in range(0, len(s), 2):
            ns += '1' if s[i] == s[i+1] else '0'
        s = ns
    return s

