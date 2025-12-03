from typing import Any
from collections import Counter


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    m = ''
    for i in range(len(ls[0])):
        c = Counter([l[i] for l in ls])
        m += c.most_common(1)[0][0]
    return m


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    m = ''
    for i in range(len(ls[0])):
        c = Counter([l[i] for l in ls])
        m += c.most_common()[-1][0]
    return m

