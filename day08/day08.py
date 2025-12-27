import os
import sys
import math
from typing import List, Tuple

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

class UnionFind:
    """
    A Disjoint Set Union (DSU) data structure with path compression and union by rank.
    
    This class efficiently tracks partitioned sets of elements. It supports two primary operations:
    1. Finding the representative (root) of the set containing a specific element.
    2. Merging (unioning) two sets together.
    
    It also maintains the size of each set, allowing for easy retrieval of connected component sizes.
    """
    
    def __init__(self, size: int):
        """
        Initializes the UnionFind structure.

        Args:
            size: The total number of elements to track (indices 0 to size-1).
                  Each element starts in its own disjoint set of size 1.
        """
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size
        self.size: List[int] = [1] * size  # Tracks the number of elements in the set rooted at i

    def find(self, i: int) -> int:
        """
        Finds the representative (root) of the set containing element 'i'.
        
        Implements path compression: As the method recursively traverses up the tree
        to find the root, it updates the parent of each visited node to point directly 
        to the root. This flattens the tree structure, optimizing future lookups.

        Args:
            i: The element to search for.

        Returns:
            The index of the root element of the set containing 'i'.
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Merges the set containing element 'i' with the set containing element 'j'.
        
        Implements union by rank: To keep the tree height small, the shorter tree (lower rank)
        is always attached to the root of the taller tree (higher rank).
        
        Also updates the 'size' attribute of the new root to reflect the combined number of elements.

        Args:
            i: An element in the first set.
            j: An element in the second set.

        Returns:
            True if the two elements were in different sets and a merge occurred.
            False if they were already in the same set (no changes made).
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank optimization
            if self.rank[root_i] < self.rank[root_j]:
                root_i, root_j = root_j, root_i
            
            # Attach the shorter tree to the taller one
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1
            return True
        return False

def parse_input(lines: List[str]) -> List[Tuple[int, int, int]]:
    """
    Parses list of 'x,y,z' strings into tuples of integers.
    
    Args:
        lines: The input list of coordinates as string.
        
    Returns:
        A list of tuples representing the (x, y, z) coordinates.
    """
    points = []
    for line in lines:
        if not line.strip():
            continue
        parts = list(map(int, line.strip().split(',')))
        points.append(tuple(parts))
    return points

def calculate_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> float:
    """
    Calculates Euclidean distance between two 3D points.
    
    Args:
        p1: Tuple of 3 ints, representing the coordinates of a point.
        p2: Tuple of 3 ints, representing the coordinates of a point.

    Returns:
        A float representing the distance between the two points.
    """
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def gen_edges(num_jb: int, points: List[Tuple[int, int, int]]) -> List[Tuple[float, int, int]]:
    """
    Generates and sorts all possible edges between junction boxes based on distance.
    
    Args:
        num_jb: The number of junction boxes.
        points: The list of coordinate tuples.

    Returns:
        A list of tuples (distance, index_i, index_j), sorted by distance (ascending).
    """
    edges = []
    for i in range(num_jb):
        for j in range(i + 1, num_jb):
            dist = calculate_distance(points[i], points[j])
            edges.append((dist, i, j))
    
    # Sort edges by distance (smallest first)
    edges.sort()

    return edges

def solve(lines: List[str], max_connections: int = 1000) -> int:
    """
    Solves the Day 8 puzzle.
    
    Args:
        lines: Input lines containing coordinates.
        max_connections: Number of shortest connections to process (default 1000).
        
    Returns:
        The product of the sizes of the three largest circuits.
    """
    points = parse_input(lines)
    n = len(points)
    
    # Generate all edges
    sorted_edges = gen_edges(n, points)

    # Process the top `max_connections` edges
    uf = UnionFind(n)
    
    # Process exactly max_connections, or number of edges if fewer exist
    limit = min(len(sorted_edges), max_connections)
    for k in range(limit):
        _, edge_A, edge_B = sorted_edges[k]
        uf.union(edge_A, edge_B)
    
    # Calculate circuit sizes
    # Find the unique roots and their sizes
    root_map = {} # root_index -> size
    for i in range(n):
        root = uf.find(i)
        # We rely on the size array in the root
        if root not in root_map:
            root_map[root] = uf.size[root]
            
    sizes = list(root_map.values())
    sizes.sort(reverse=True)
    
    # Multiply top 3
    if len(sizes) < 3:
        result = 1
        for s in sizes:
            result *= s
        return result
    else:
        return sizes[0] * sizes[1] * sizes[2]

def part01(lines: List[str]) -> None:
    """Executes Part 1 of the puzzle."""
    print("Advent of Code 2025 - Day 8 - Part 1")

    result = solve(lines)
    print(f"Product of three largest circuits: {result}")

def main():
    """Main execution function."""
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    part01(input_lines)

if __name__ == "__main__":
    main()