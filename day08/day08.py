import os
import sys
import math
from typing import List, Tuple, TypeAlias

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

# Point3D: (X, Y, Z)
Point3D: TypeAlias = Tuple[int, int, int]
# Edge: (distance, index_u, index_v)
Edge: TypeAlias = Tuple[float, int, int]

DEFAULT_MAX_CONNECTIONS = 1000

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
        self.num_components = size

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
            self.num_components -= 1
            
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1
            return True
        return False

    def get_component_sizes(self) -> List[int]:
        """
        Retrieves the sizes of all disjoint sets (connected components).

        Returns:
            A list of integer sizes, sorted in descending order.
        """
        root_map = {}
        # Iterate over all elements to ensure we find the representative of each set
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in root_map:
                root_map[root] = self.size[root]
        
        return sorted(root_map.values(), reverse=True)

def parse_input(lines: List[str]) -> List[Point3D]:
    """
    Parses list of 'x,y,z' strings into tuples of integers.
    
    Args:
        lines: The input list of coordinates as string.
        
    Returns:
        A list of tuples representing the (x, y, z) coordinates.
    """
    points: List[Point3D] = []
    for line in lines:
        if not line.strip():
            continue
        parts = list(map(int, line.strip().split(',')))
        points.append((parts[0], parts[1], parts[2]))
    return points

def calculate_distance(p1: Point3D, p2: Point3D) -> float:
    """
    Calculates Euclidean distance between two 3D points.
    
    Args:
        p1: Tuple of 3 ints, representing the coordinates of a point.
        p2: Tuple of 3 ints, representing the coordinates of a point.

    Returns:
        A float representing the distance between the two points.
    """
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def get_sorted_edges(points: List[Point3D]) -> List[Edge]:
    """
    Generates and sorts all possible edges between junction boxes based on distance.
    
    Args:
        points: The list of coordinate tuples.

    Returns:
        A list of tuples (distance, index_i, index_j), sorted by distance (ascending).
    """
    edges: List[Edge] = []
    num_jb = len(points)
    for i in range(num_jb):
        for j in range(i + 1, num_jb):
            dist = calculate_distance(points[i], points[j])
            edges.append((dist, i, j))
    
    # Sort edges by distance (smallest first)
    edges.sort(key=lambda x: x[0])

    return edges

def initialize_system(lines: List[str]) -> Tuple[List[Point3D], List[Edge], UnionFind]:
    """
    Parses input, generates edges, and initializes the DSU structure.
    
    Args:
        lines: Raw input lines.
        
    Returns:
        Tuple containing:
        - List of 3D points
        - Sorted list of edges (distance, u, v)
        - Initialized UnionFind instance
    """
    points = parse_input(lines)
    sorted_edges = get_sorted_edges(points)
    uf = UnionFind(len(points))
    return points, sorted_edges, uf

def solve_part1(lines: List[str], max_connections: int = DEFAULT_MAX_CONNECTIONS) -> int:
    """
    Solves the Day 8 Part 1 puzzle.
    
    Connects the closest pairs of junction boxes exactly `max_connections` times,
    regardless of whether they are already connected.
    
    Args:
        lines: Input lines containing coordinates.
        max_connections: Number of shortest connections to process (default 1000).
        
    Returns:
        The product of the sizes of the three largest circuits.
    """
    _, sorted_edges, uf = initialize_system(lines)
    
    # Process exactly max_connections, or number of edges if fewer exist
    limit = min(len(sorted_edges), max_connections)
    for k in range(limit):
        _, edge_A, edge_B = sorted_edges[k]
        uf.union(edge_A, edge_B)
        # Note: We ignore the return value of union(). In Part 1, redundant connections
        # still count towards the 'max_connections' limit.
    
    # Gather circuit sizes
    sizes = uf.get_component_sizes()
    
    # Return product of top 3
    if len(sizes) < 3:
        return math.prod(sizes)
    
    return sizes[0] * sizes[1] * sizes[2]

def solve_part2(lines: List[str]) -> int:
    """
    Solves the Day 8 Part 2 puzzle.
    
    Continues connecting the closest unconnected junction boxes until 
    a single connected component (circuit) remains.
    
    Args:
        lines: Input lines containing coordinates.
        
    Returns:
        The product of the X-coordinates of the last two junction boxes connected.
    """
    points, sorted_edges, uf = initialize_system(lines)
    
    # Kruskal's Algorithm logic
    for _, u, v in sorted_edges:
        if uf.union(u, v):
            # A merge occurred (reduced component count)
            if uf.num_components == 1:
                # This was the final connection!
                return points[u][0] * points[v][0]
                
    return 0 # Should not be reached

def main():
    """Main execution function."""
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    
    print("Advent of Code 2025 - Day 8 - Part 1")
    result1 = solve_part1(input_lines)
    print(f"Product of three largest circuits: {result1}")

    print("Advent of Code 2025 - Day 8 - Part 2")
    result2 = solve_part2(input_lines)
    print(f"Product of X coordinates of last connection: {result2}")

if __name__ == "__main__":
    main()