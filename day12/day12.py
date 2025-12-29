import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def parse_input(data: list[str]) -> tuple:
    """Parses the input data into shapes and region tasks.

    Args:
        data (list[str]): The input lines representing shape definitions and tasks.

    Returns:
        tuple: A dictionary of shapes (index -> frozenset of coords) and a list of task dictionaries.
    """
    shapes = {}
    tasks = []
    
    current_shape_idx = None
    current_shape_lines = []
    
    parsing_shapes = True
    
    for line in data:
        line = line.strip()
        if not line:
            if current_shape_idx is not None:
                shapes[current_shape_idx] = parse_shape(current_shape_lines)
                current_shape_idx = None
                current_shape_lines = []
            continue
            
        if ':' in line and not 'x' in line: # Shape definition start
            if current_shape_idx is not None:
                 shapes[current_shape_idx] = parse_shape(current_shape_lines)
                 current_shape_lines = []
            
            idx_str = line.split(':')[0]
            current_shape_idx = int(idx_str)
        elif parsing_shapes and ('#' in line or '.' in line):
            current_shape_lines.append(line)
        elif 'x' in line and ':' in line: # Region task
            if current_shape_idx is not None:
                shapes[current_shape_idx] = parse_shape(current_shape_lines)
                current_shape_idx = None
                current_shape_lines = []
            parsing_shapes = False # Switch mode
            
            task = _parse_task_line(line)
            tasks.append(task)
            
    if current_shape_idx is not None:
        shapes[current_shape_idx] = parse_shape(current_shape_lines)

    return shapes, tasks

def _parse_task_line(line: str) -> dict:
    """Parses a single task line.

    Args:
        line (str): The line defining the task (e.g., '12x5: 1 0 1 0 2 2').

    Returns:
        dict: A dictionary containing 'width', 'height', and 'counts'.
    """
    parts = line.split(':')
    dims = parts[0].strip().split('x')
    width = int(dims[0])
    height = int(dims[1])
    
    counts = list(map(int, parts[1].strip().split()))
    return {
        'width': width,
        'height': height,
        'counts': counts
    }

def parse_shape(lines) -> frozenset:
    """Converts ASCII lines to a set of (r, c) coordinates.

    Args:
        lines (list[str]): ASCII representation of the shape.

    Returns:
        frozenset: A set of (row, col) coordinates representing the shape.
    """
    coords = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                coords.add((r, c))
    return normalize_shape(coords)

def normalize_shape(coords) -> frozenset:
    """Aligns shape to (0,0) top-left.

    Args:
        coords (set): Set of (row, col) coordinates.

    Returns:
        frozenset: Normalized set of coordinates where min_r and min_c are 0.
    """
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

def generate_variants(base_shape) -> list[frozenset]:
    """Generates all 8 unique rotation/flip variants of a shape.

    Args:
        base_shape (frozenset): The base shape coordinates.

    Returns:
        list[frozenset]: A list of unique shape variants (rotations and flips).
    """
    variants = set()
    
    current = base_shape
    for _ in range(2): # Flip
        for _ in range(4): # Rotate
            variants.add(normalize_shape(current))
            # Rotate 90 deg clockwise: (r, c) -> (c, -r)
            current = frozenset((c, -r) for r, c in current)
        # Flip: (r, c) -> (r, -c)
        current = frozenset((r, -c) for r, c in current)
        
    return list(variants)

def solve_region(width, height, present_list, shapes) -> bool:
    """Tries to fit all presents in present_list into the region.

    Args:
        width (int): Width of the region.
        height (int): Height of the region.
        present_list (list[int]): List of present shape indices to fit.
        shapes (dict): Dictionary mapping shape indices to lists of variants.

    Returns:
        bool: True if all presents fit, False otherwise.
    """
    # Calculate area for sort and validity check
    total_area = 0
    present_areas = []
    
    # Cache variant areas to avoid recomputing
    # We assume all variants of a shape have the same area (they must)
    shape_areas = {}
    
    for p_idx in present_list:
        if p_idx not in shape_areas:
            # Just pick the first variant to measure area
            shape_areas[p_idx] = len(shapes[p_idx][0])
        
        area = shape_areas[p_idx]
        present_areas.append((area, p_idx))
        total_area += area
        
    if total_area > width * height:
        return False
    
    # Sort descending by area
    present_areas.sort(key=lambda x: x[0], reverse=True)
    sorted_presents = [x[1] for x in present_areas]
    
    grid = set() # Set of occupied (r, c)
    
    # We pass -1 as the last_pos initially
    return backtrack(grid, sorted_presents, shapes, width, height, -1)

def _can_place_variant(grid, variant, r, c, width, height) -> tuple[bool, list[tuple[int, int]]]:
    """Checks if a variant can be placed at (r, c).
    
    Args:
        grid (set): The current grid state.
        variant (frozenset): The shape variant coordinates.
        r (int): Row position.
        c (int): Column position.
        width (int): Grid width.
        height (int): Grid height.
        
    Returns:
        tuple[bool, list]: A boolean indicating success, and a list of cells to occupy.
    """
    cells_to_occupy = []
    for vr, vc in variant:
        nr, nc = r + vr, c + vc
        
        # Boundary checks
        if nr < 0 or nr >= height or nc < 0 or nc >= width:
            return False, []
        
        if (nr, nc) in grid:
            return False, []
        
        cells_to_occupy.append((nr, nc))
        
    return True, cells_to_occupy

def backtrack(grid, remaining_presents, shapes, width, height, last_pos) -> bool:
    """Recursive backtracking function to place presents.

    Args:
        grid (set): Set of currently occupied (r, c) coordinates.
        remaining_presents (list[int]): Sorted list of present indices to place.
        shapes (dict): Dictionary of shape variants.
        width (int): Grid width.
        height (int): Grid height.
        last_pos (int): Linear index of the last placed identical item (optimization).

    Returns:
        bool: True if a valid placement is found, False otherwise.
    """
    if not remaining_presents:
        return True
    
    current_p_idx = remaining_presents[0]
    next_presents = remaining_presents[1:]
    
    # Optimization: Identical consecutive items
    start_search = 0
    if last_pos != -1:
        start_search = last_pos
        
    variants = shapes[current_p_idx]
    
    for i in range(start_search, width * height):
        r = i // width
        c = i % width
        
        if (r, c) in grid:
            continue
        
        for variant in variants:
            can_place, cells_to_occupy = _can_place_variant(grid, variant, r, c, width, height)
            
            if can_place:
                # Place
                for cell in cells_to_occupy:
                    grid.add(cell)
                
                # Prepare next recursion
                next_start_pos = -1
                if next_presents and next_presents[0] == current_p_idx:
                    next_start_pos = i
                
                if backtrack(grid, next_presents, shapes, width, height, next_start_pos):
                    return True
                
                # Backtrack
                for cell in cells_to_occupy:
                    grid.remove(cell)

    return False

def solve(input_lines: list[str]) -> None:
    """Executes the solution for the Day 12 puzzle.

    Args:
        input_lines (list[str]): The lines from the puzzle input file.
    """
    print("Advent of Code 2025 - Day 12")
    raw_shapes, tasks = parse_input(input_lines)
    
    # Precompute variants
    shapes = {}
    for idx, base_shape in raw_shapes.items():
        shapes[idx] = generate_variants(base_shape)
        
    print(f"Parsed {len(tasks)} tasks.")
    
    solved_count = 0
    total_tasks = len(tasks)
    
    for i, task in enumerate(tasks):
        width = task['width']
        height = task['height']
        counts = task['counts']
        
        # Flatten counts into a list of presents
        present_list = []
        for s_idx, count in enumerate(counts):
            present_list.extend([s_idx] * count)
            
        if solve_region(width, height, present_list, shapes):
            solved_count += 1
        
        # simple progress indicator
        if i % 10 == 0:
            print(f"Processed {i}/{total_tasks}...", end='\r')
            
    print(f"Total solved regions: {solved_count}")

def main() -> None:
    """Main function to run the Day 12 solution."""
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    solve(input_lines)

if __name__ == "__main__":
    main()
