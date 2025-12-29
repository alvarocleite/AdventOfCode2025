import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def parse_input(data: list[str]) -> dict[str, list[str]]:
    """
    Parses the input data into an adjacency list representing the device connections.
    
    Args:
        data (list[str]): The lines of the input file.
        
    Returns:
        dict[str, list[str]]: A dictionary where keys are device names and values are lists of target devices.
    """
    graph = {}
    for line in data:
        if not line.strip():
            continue
        parts = line.split(':', 1)
        source = parts[0].strip()
        
        if len(parts) > 1:
            targets = parts[1].strip().split()
        else:
            targets = []
        
        graph[source] = targets
    
    return graph

def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Counts all paths from start to end using DFS with memoization.
    
    Args:
        graph (dict[str, list[str]]): The adjacency list of the graph.
        start (str): The starting node.
        end (str): The destination node.
        
    Returns:
        int: The number of distinct paths from start to end.
        
    Raises:
        ValueError: If a cycle is detected in the graph.
    """
    memo = {}
    visiting = set() # To detect cycles

    def dfs(node: str) -> int:
        if node == end:
            return 1
        if node in memo:
            return memo[node]
        if node in visiting:
            # Cycle detected.
            raise ValueError(f"Cycle detected involving node {node}")
        
        visiting.add(node)
        
        count = 0
        # If node has no outgoing edges defined in graph, count remains 0 (dead end)
        if node in graph:
            for neighbor in graph[node]:
                count += dfs(neighbor)
        
        visiting.remove(node)
        memo[node] = count
        return count

    return dfs(start)

def part01(input_lines: list[str]) -> None:
    """Executes Part 1 of the Advent of Code Day 11 puzzle.

    Args:
        input_lines (list[str]): The list of input lines.
    """
    print("Advent of Code 2025 - Day 11 - Part 1")
    graph = parse_input(input_lines)
    try:
        total_paths = count_paths(graph, 'you', 'out')
        print(f"Total paths from 'you' to 'out': {total_paths}")
    except ValueError as e:
        print(f"Error: {e}")

def part02(input_lines: list[str]) -> None:
    """Executes Part 2 of the Advent of Code Day 11 puzzle.

    Args:
        input_lines (list[str]): The list of input lines.
    """
    print("Advent of Code 2025 - Day 11 - Part 2")
    graph = parse_input(input_lines)
    try:
        # Sequence 1: svr -> ... -> dac -> ... -> fft -> ... -> out
        paths_dac_fft = (count_paths(graph, 'svr', 'dac') *
                         count_paths(graph, 'dac', 'fft') *
                         count_paths(graph, 'fft', 'out'))
                         
        # Sequence 2: svr -> ... -> fft -> ... -> dac -> ... -> out
        paths_fft_dac = (count_paths(graph, 'svr', 'fft') *
                         count_paths(graph, 'fft', 'dac') *
                         count_paths(graph, 'dac', 'out'))
        
        total_paths = paths_dac_fft + paths_fft_dac
        print(f"Total paths from 'svr' to 'out' via 'dac' and 'fft': {total_paths}")
    except ValueError as e:
        print(f"Error: {e}")

def main() -> None:
    """Main function to run the Advent of Code Day 11 solutions."""
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    
    part01(input_lines)
    part02(input_lines)

if __name__ == "__main__":
    main()
