def rotate_pattern(pattern):
    """Rotate pattern 90 degrees clockwise."""
    size = len(pattern)
    return [''.join(pattern[size-1-j][i] for j in range(size)) for i in range(size)]


def flip_pattern(pattern):
    """Flip pattern horizontally."""
    return [row[::-1] for row in pattern]


def get_all_variations(pattern):
    """Get all 8 possible rotations and flips of a pattern."""
    variations = set()
    current = pattern[:]

    for _ in range(4):
        variations.add('/'.join(current))
        variations.add('/'.join(flip_pattern(current)))
        current = rotate_pattern(current)

    return variations


def solve_part_1(input_data):
    """Fractal art - 5 iterations."""
    lines = input_data.strip().split('\n')
    rules = {}

    # Parse rules
    for line in lines:
        input_pattern, output_pattern = line.split(' => ')
        input_grid = input_pattern.split('/')
        output_grid = output_pattern.split('/')

        # Add all rotations and flips of input pattern
        for variation in get_all_variations(input_grid):
            rules[variation] = output_grid

    # Start with initial pattern
    grid = ['.#.', '..#', '###']

    for iteration in range(5):
        size = len(grid)

        if size % 2 == 0:
            # Divide into 2x2 squares
            square_size = 2
            new_square_size = 3
        else:
            # Divide into 3x3 squares
            square_size = 3
            new_square_size = 4

        squares_per_row = size // square_size
        new_size = squares_per_row * new_square_size
        new_grid = [['.' for _ in range(new_size)] for _ in range(new_size)]

        for square_r in range(squares_per_row):
            for square_c in range(squares_per_row):
                # Extract square
                square = []
                for r in range(square_size):
                    row = ''
                    for c in range(square_size):
                        row += grid[square_r * square_size + r][square_c * square_size + c]
                    square.append(row)

                # Apply rule
                pattern_key = '/'.join(square)
                new_square = rules[pattern_key]

                # Place new square
                for r in range(new_square_size):
                    for c in range(new_square_size):
                        new_grid[square_r * new_square_size + r][square_c * new_square_size + c] = new_square[r][c]

        grid = [''.join(row) for row in new_grid]

    # Count pixels that are on
    return sum(row.count('#') for row in grid)


def solve_part_2(input_data):
    """Fractal art - 18 iterations."""
    lines = input_data.strip().split('\n')
    rules = {}

    # Parse rules
    for line in lines:
        input_pattern, output_pattern = line.split(' => ')
        input_grid = input_pattern.split('/')
        output_grid = output_pattern.split('/')

        # Add all rotations and flips of input pattern
        for variation in get_all_variations(input_grid):
            rules[variation] = output_grid

    # Start with initial pattern
    grid = ['.#.', '..#', '###']

    for iteration in range(18):
        size = len(grid)

        if size % 2 == 0:
            square_size = 2
            new_square_size = 3
        else:
            square_size = 3
            new_square_size = 4

        squares_per_row = size // square_size
        new_size = squares_per_row * new_square_size
        new_grid = [['.' for _ in range(new_size)] for _ in range(new_size)]

        for square_r in range(squares_per_row):
            for square_c in range(squares_per_row):
                # Extract square
                square = []
                for r in range(square_size):
                    row = ''
                    for c in range(square_size):
                        row += grid[square_r * square_size + r][square_c * square_size + c]
                    square.append(row)

                # Apply rule
                pattern_key = '/'.join(square)
                new_square = rules[pattern_key]

                # Place new square
                for r in range(new_square_size):
                    for c in range(new_square_size):
                        new_grid[square_r * new_square_size + r][square_c * new_square_size + c] = new_square[r][c]

        grid = [''.join(row) for row in new_grid]

    # Count pixels that are on
    return sum(row.count('#') for row in grid)
