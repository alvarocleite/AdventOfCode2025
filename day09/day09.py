import os
import sys
from typing import List, Tuple, TypeAlias

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

Point: TypeAlias = Tuple[int, int]
Edge: TypeAlias = Tuple[Point, Point]
Rect: TypeAlias = Tuple[int, int, int, int] # min_x, min_y, max_x, max_y

def parse_input(lines: List[str]) -> List[Point]:
    """
    Parses list of 'x,y' strings into tuples of integers.

    Args:
        lines: A list of strings, each containing "x,y" coordinates.

    Returns:
        A list of (x, y) integer tuples representing the red tiles.
    """
    points: List[Point] = []
    for line in lines:
        if not line.strip():
            continue
        parts = list(map(int, line.strip().split(',')))
        points.append((parts[0], parts[1]))
    return points

def get_polygon_edges(points: List[Point]) -> List[Edge]:
    """
    Generates the list of edges forming the polygon boundary.
    
    The edges connect sequential points in the list, wrapping around from the last to the first.

    Args:
        points: The ordered vertices of the polygon (red tiles).

    Returns:
        A list of edges, where each edge is a tuple of two points ((x1, y1), (x2, y2)).
    """
    n = len(points)
    edges = []
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        edges.append((p1, p2))
    return edges

def is_point_inside(x: float, y: float, edges: List[Edge]) -> bool:
    """
    Checks if point (x,y) is inside the polygon using Ray Casting (Even-Odd rule).
    
    This function is designed for points *strictly inside* or clearly outside.
    It casts a horizontal ray to the right from the given point and counts intersections.
    
    Args:
        x: The x-coordinate of the test point.
        y: The y-coordinate of the test point.
        edges: The list of polygon edges.

    Returns:
        True if the point is strictly inside the polygon, False otherwise.
    """
    inside = False
    for (x1, y1), (x2, y2) in edges:
        if (y1 > y) != (y2 > y):
            intersect_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < intersect_x:
                inside = not inside
    return inside

def rect_intersects_any_edge(rect: Rect, edges: List[Edge]) -> bool:
    """
    Checks if any polygon edge strictly crosses the boundary of the rectangle.
    
    A strict crossing implies the edge enters the rectangle's interior.
    Coincident edges (overlapping boundaries) are NOT considered "intersections"
    that invalidate the rectangle, because a valid rectangle can share a boundary with the polygon.

    Args:
        rect: A tuple (min_x, min_y, max_x, max_y) defining the rectangle.
        edges: The list of polygon edges.

    Returns:
        True if any edge strictly intersects the rectangle's boundary, False otherwise.
    """
    r_min_x, r_min_y, r_max_x, r_max_y = rect
    
    for (x1, y1), (x2, y2) in edges:
        ex_min, ex_max = min(x1, x2), max(x1, x2)
        ey_min, ey_max = min(y1, y2), max(y1, y2)
        
        if x1 == x2:
            if r_min_x < x1 < r_max_x:
                if max(r_min_y, ey_min) < min(r_max_y, ey_max):
                    return True
        
        elif y1 == y2:
            if r_min_y < y1 < r_max_y:
                if max(r_min_x, ex_min) < min(r_max_x, ex_max):
                    return True
                    
    return False

def calculate_max_area(points: List[Point]) -> int:
    """
    Finds the largest rectangle area formed by any two points as opposite corners.
    
    Area is calculated inclusively: (|x1 - x2| + 1) * (|y1 - y2| + 1).

    Args:
        points: List of (x, y) coordinates.

    Returns:
        The maximum integer area found.
    """
    max_area = 0
    n = len(points)
    
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            width = abs(p1[0] - p2[0]) + 1
            height = abs(p1[1] - p2[1]) + 1
            area = width * height
            if area > max_area:
                max_area = area
                
    return max_area

def calculate_constrained_max_area(points: List[Point]) -> int:
    """
    Finds the largest rectangle area formed by two points that lies strictly inside the polygon.
    
    This function verifies two conditions for a candidate rectangle:
    1. No polygon edge strictly intersects the rectangle's boundary.
    2. The center point of the rectangle is strictly inside the polygon.

    Args:
        points: List of (x, y) coordinates forming the polygon vertices.

    Returns:
        The maximum valid integer area found.
    """
    max_area = 0
    n = len(points)
    edges = get_polygon_edges(points)
    
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            
            # Form rectangle boundaries
            min_x = min(p1[0], p2[0])
            max_x = max(p1[0], p2[0])
            min_y = min(p1[1], p2[1])
            max_y = max(p1[1], p2[1])
            
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height
            
            if area <= max_area:
                continue
                
            rect = (min_x, min_y, max_x, max_y)
            
            if rect_intersects_any_edge(rect, edges):
                continue
            
            center_x = (min_x + max_x) / 2.0
            center_y = (min_y + max_y) / 2.0
            
            if is_point_inside(center_x, center_y, edges):
                max_area = area
                
    return max_area

def part01(lines: List[str]) -> None:
    """Executes Part 1 of the puzzle."""
    print("Advent of Code 2025 - Day 9 - Part 1")
    points = parse_input(lines)
    result = calculate_max_area(points)
    print(f"Largest rectangle area: {result}")

def part02(lines: List[str]) -> None:
    """Executes Part 2 of the puzzle."""
    print("Advent of Code 2025 - Day 9 - Part 2")
    points = parse_input(lines)
    result = calculate_constrained_max_area(points)
    print(f"Largest valid rectangle area: {result}")

def main():
    """Main execution function."""
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"Error: Input file not found at {INPUT_FILE_PATH}")
        return
        
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    part01(input_lines)
    part02(input_lines)

if __name__ == "__main__":
    main()
