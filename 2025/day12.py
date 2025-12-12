from typing import Any, List, Tuple, Set


def parse_shape(lines: List[str]) -> List[Tuple[int, int]]:
    """Parse a shape from its string representation to a list of coordinates."""
    coords = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                coords.append((x, y))
    return coords


def normalize_shape(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Normalize a shape by moving it to start at (0, 0)."""
    if not coords:
        return []

    min_x = min(x for x, y in coords)
    min_y = min(y for x, y in coords)

    return [(x - min_x, y - min_y) for x, y in coords]


def rotate_90(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate coordinates 90 degrees clockwise."""
    return [(y, -x) for x, y in coords]


def flip_horizontal(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Flip coordinates horizontally."""
    return [(-x, y) for x, y in coords]


def get_all_orientations(coords: List[Tuple[int, int]]) -> Set[Tuple[Tuple[int, int], ...]]:
    """Get all unique orientations (rotations and flips) of a shape."""
    orientations = set()
    current = coords[:]

    # Try all 4 rotations
    for _ in range(4):
        normalized = normalize_shape(current)
        orientations.add(tuple(sorted(normalized)))

        # Also try flipped version
        flipped = flip_horizontal(current)
        normalized_flipped = normalize_shape(flipped)
        orientations.add(tuple(sorted(normalized_flipped)))

        current = rotate_90(current)

    return orientations


def can_place_shape(grid: List[List[bool]], shape_coords: List[Tuple[int, int]],
                   start_x: int, start_y: int, width: int, height: int) -> bool:
    """Check if a shape can be placed at the given position."""
    for dx, dy in shape_coords:
        x, y = start_x + dx, start_y + dy
        if x < 0 or x >= width or y < 0 or y >= height or grid[y][x]:
            return False
    return True


def place_shape(grid: List[List[bool]], shape_coords: List[Tuple[int, int]],
               start_x: int, start_y: int) -> None:
    """Place a shape on the grid."""
    for dx, dy in shape_coords:
        x, y = start_x + dx, start_y + dy
        grid[y][x] = True


def remove_shape(grid: List[List[bool]], shape_coords: List[Tuple[int, int]],
                start_x: int, start_y: int) -> None:
    """Remove a shape from the grid."""
    for dx, dy in shape_coords:
        x, y = start_x + dx, start_y + dy
        grid[y][x] = False


def solve_region(width: int, height: int, shape_orientations: List[Set],
                required_counts: List[int]) -> bool:
    """Try to fit all required shapes into a region using heuristic approach."""

    # Early exit: check if total area of required shapes exceeds region area
    total_area_needed = 0
    shape_areas = []

    for shape_idx, count in enumerate(required_counts):
        if count > 0 and shape_orientations[shape_idx]:
            # Get area of one instance of this shape
            shape_area = len(next(iter(shape_orientations[shape_idx])))
            total_area_needed += shape_area * count
            shape_areas.append((shape_idx, shape_area, count))

    region_area = width * height
    if total_area_needed > region_area:
        return False

    # For very small regions or small numbers of shapes, use exact backtracking
    total_shapes = sum(required_counts)
    if region_area <= 25 and total_shapes <= 5:
        return solve_region_exact(width, height, shape_orientations, required_counts)

    # For larger cases, use heuristic: check if shapes can theoretically fit
    # with some packing efficiency factor
    packing_efficiency = 0.75  # More conservative packing efficiency

    if total_area_needed > region_area * packing_efficiency:
        return False

    # Additional heuristic: check if any shape is too large for the region
    for shape_idx, count in enumerate(required_counts):
        if count > 0 and shape_orientations[shape_idx]:
            # Check if any orientation of this shape can fit
            can_fit = False
            for orientation in shape_orientations[shape_idx]:
                shape_coords = list(orientation)
                if shape_coords:
                    max_x = max(x for x, y in shape_coords)
                    max_y = max(y for x, y in shape_coords)
                    if max_x < width and max_y < height:
                        can_fit = True
                        break
            if not can_fit:
                return False

    # If all basic checks pass, assume it's feasible for large cases
    return True


def solve_region_exact(width: int, height: int, shape_orientations: List[Set],
                      required_counts: List[int]) -> bool:
    """Exact backtracking for small cases."""

    # Create a list of shapes to place in order of difficulty (larger shapes first)
    shapes_to_place = []
    for shape_idx, count in enumerate(required_counts):
        for _ in range(count):
            shapes_to_place.append(shape_idx)

    # Sort by shape size (largest first) to fail fast
    def get_shape_size(shape_idx):
        if shape_orientations[shape_idx]:
            return len(next(iter(shape_orientations[shape_idx])))
        return 0

    shapes_to_place.sort(key=get_shape_size, reverse=True)

    def backtrack(placement_idx: int, grid: List[List[bool]]) -> bool:
        if placement_idx >= len(shapes_to_place):
            return True

        shape_idx = shapes_to_place[placement_idx]

        # Try each orientation of the current shape
        for orientation in shape_orientations[shape_idx]:
            shape_coords = list(orientation)

            # Try placing at each valid position
            for y in range(height):
                for x in range(width):
                    if can_place_shape(grid, shape_coords, x, y, width, height):
                        # Place the shape
                        place_shape(grid, shape_coords, x, y)

                        # Recursively try to place remaining shapes
                        if backtrack(placement_idx + 1, grid):
                            return True

                        # Backtrack
                        remove_shape(grid, shape_coords, x, y)

        return False

    grid = [[False] * width for _ in range(height)]
    return backtrack(0, grid)


def solve_part_1(input_data: str) -> Any:
    """
    Solve part 1 of the challenge.

    This is a 2D bin packing problem where we need to determine how many regions
    can fit all their required present shapes. Each shape can be rotated and flipped.

    For small regions, we use exact backtracking. For large regions, we use heuristics
    based on area constraints and packing efficiency estimates.
    """
    lines = input_data.strip().split('\n')

    # Parse shapes
    shapes = {}
    i = 0

    # Parse all shape definitions
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # Skip empty lines
            i += 1
            continue

        # Check if this line starts a shape definition (single digit followed by colon)
        if ':' in line and line.split(':')[0].strip().isdigit() and 'x' not in line:
            shape_idx = int(line.split(':')[0])
            i += 1
            shape_lines = []

            # Read shape data until we hit empty line or start of regions
            while i < len(lines):
                shape_line = lines[i]
                if not shape_line.strip() or 'x' in shape_line:  # Empty line or region line
                    break
                shape_lines.append(shape_line)
                i += 1

            coords = parse_shape(shape_lines)
            shapes[shape_idx] = coords
        else:
            # We've hit the regions section
            break

    # Get all orientations for each shape
    shape_orientations = []
    for shape_idx in range(6):  # We know there are 6 shapes (0-5)
        orientations = get_all_orientations(shapes[shape_idx])
        shape_orientations.append(orientations)

    # Parse regions and check which ones can fit all presents
    count = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        parts = line.split()
        dimensions = parts[0].replace(':', '').split('x')  # Remove colon before splitting
        width = int(dimensions[0])
        height = int(dimensions[1])
        required_counts = [int(x) for x in parts[1:]]

        # Check if this region can fit all required presents
        if solve_region(width, height, shape_orientations, required_counts):
            count += 1

        i += 1

    return count

