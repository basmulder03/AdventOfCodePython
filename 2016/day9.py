from typing import Any


def solve_part_1(input_data: str) -> Any:
    d = input_data.strip()
    l = 0
    i = 0
    while i < len(d):
        if d[i] == '(':
            e = d.index(')', i)
            m = d[i+1:e]
            n, r = map(int, m.split('x'))
            l += n * r
            i = e + 1 + n
        else:
            l += 1
            i += 1
    return l


def solve_part_2(input_data: str) -> Any:
    def dec(s):
        if '(' not in s:
            return len(s)
        t = 0
        i = 0
        while i < len(s):
            if s[i] == '(':
                e = s.index(')', i)
                m = s[i+1:e]
                n, r = map(int, m.split('x'))
                t += dec(s[e+1:e+1+n]) * r
                i = e + 1 + n
            else:
                t += 1
                i += 1
        return t
    return dec(input_data.strip())

