from typing import Any


def solve_part_1(input_data: str) -> Any:
    r = input_data.strip()
    c = r.count('.')
    for _ in range(39):
        nr = ''
        for i in range(len(r)):
            l = r[i-1] if i > 0 else '.'
            ct = r[i]
            rt = r[i+1] if i < len(r)-1 else '.'
            if (l == '^' and ct == '^' and rt == '.') or \
               (l == '.' and ct == '^' and rt == '^') or \
               (l == '^' and ct == '.' and rt == '.') or \
               (l == '.' and ct == '.' and rt == '^'):
                nr += '^'
            else:
                nr += '.'
                c += 1
        r = nr
    return c


def solve_part_2(input_data: str) -> Any:
    r = input_data.strip()
    c = r.count('.')
    for _ in range(399999):
        nr = ''
        for i in range(len(r)):
            l = r[i-1] if i > 0 else '.'
            ct = r[i]
            rt = r[i+1] if i < len(r)-1 else '.'
            if (l == '^' and ct == '^' and rt == '.') or \
               (l == '.' and ct == '^' and rt == '^') or \
               (l == '^' and ct == '.' and rt == '.') or \
               (l == '.' and ct == '.' and rt == '^'):
                nr += '^'
            else:
                nr += '.'
                c += 1
        r = nr
    return c

