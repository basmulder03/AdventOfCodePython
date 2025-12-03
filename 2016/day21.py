from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    s = list('abcdefgh')
    for l in ls:
        p = l.split()
        if 'swap position' in l:
            x, y = int(p[2]), int(p[5])
            s[x], s[y] = s[y], s[x]
        elif 'swap letter' in l:
            x, y = s.index(p[2]), s.index(p[5])
            s[x], s[y] = s[y], s[x]
        elif 'rotate based' in l:
            x = s.index(p[-1])
            r = 1 + x + (1 if x >= 4 else 0)
            r = r % len(s)
            s = s[-r:] + s[:-r]
        elif 'rotate' in l:
            r = int(p[2])
            if p[1] == 'left':
                s = s[r:] + s[:r]
            else:
                s = s[-r:] + s[:-r]
        elif 'reverse' in l:
            x, y = int(p[2]), int(p[4])
            s[x:y+1] = s[x:y+1][::-1]
        elif 'move' in l:
            x, y = int(p[2]), int(p[5])
            c = s.pop(x)
            s.insert(y, c)
    return ''.join(s)


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')[::-1]
    s = list('fbgdceah')
    for l in ls:
        p = l.split()
        if 'swap position' in l:
            x, y = int(p[2]), int(p[5])
            s[x], s[y] = s[y], s[x]
        elif 'swap letter' in l:
            x, y = s.index(p[2]), s.index(p[5])
            s[x], s[y] = s[y], s[x]
        elif 'rotate based' in l:
            c = p[-1]
            for r in range(len(s)):
                t = s[r:] + s[:r]
                x = t.index(c)
                rt = 1 + x + (1 if x >= 4 else 0)
                rt = rt % len(s)
                if t[-rt:] + t[:-rt] == s:
                    s = t
                    break
        elif 'rotate' in l:
            r = int(p[2])
            if p[1] == 'left':
                s = s[-r:] + s[:-r]
            else:
                s = s[r:] + s[:r]
        elif 'reverse' in l:
            x, y = int(p[2]), int(p[4])
            s[x:y+1] = s[x:y+1][::-1]
        elif 'move' in l:
            x, y = int(p[2]), int(p[5])
            c = s.pop(y)
            s.insert(x, c)
    return ''.join(s)

