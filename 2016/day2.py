from typing import Any


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')
    
    keypad = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]
    
    row, col = 1, 1
    code = []
    
    for line in lines:
        for move in line:
            if move == 'U' and row > 0:
                row -= 1
            elif move == 'D' and row < 2:
                row += 1
            elif move == 'L' and col > 0:
                col -= 1
            elif move == 'R' and col < 2:
                col += 1
        
        code.append(keypad[row][col])
    
    return ''.join(code)


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')
    
    keypad = [
        [None, None, '1', None, None],
        [None, '2', '3', '4', None],
        ['5', '6', '7', '8', '9'],
        [None, 'A', 'B', 'C', None],
        [None, None, 'D', None, None]
    ]
    
    row, col = 2, 0
    code = []
    
    for line in lines:
        for move in line:
            new_row, new_col = row, col
            
            if move == 'U':
                new_row = row - 1
            elif move == 'D':
                new_row = row + 1
            elif move == 'L':
                new_col = col - 1
            elif move == 'R':
                new_col = col + 1
            
            if (0 <= new_row < 5 and 0 <= new_col < 5 and
                keypad[new_row][new_col] is not None):
                row, col = new_row, new_col
        
        code.append(keypad[row][col])
    
    return ''.join(code)
