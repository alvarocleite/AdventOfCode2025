from typing import List

def read_input_file(file_path: str, strip_lines: bool = True) -> List[str]:
    """
    Reads lines from a specified text file.

    Args:
        file_path: The path to the input file.
        strip_lines: If True, strips leading/trailing whitespace. 
                     If False, only strips trailing newlines (preserves indentation).

    Returns:
        A list of strings, where each string is a line from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        if strip_lines:
            return [line.strip() for line in file]
        else:
            return [line.rstrip('\n') for line in file]

def read_grid_padded(file_path: str) -> List[str]:
    """
    Reads lines from a file, preserving whitespace and padding to max length.
    Useful for grid-based puzzles.

    Args:
        file_path: The path to the input file.

    Returns:
        A list of strings of equal length, forming a character grid.
    """
    lines = read_input_file(file_path, strip_lines=False)
    
    if not lines:
        return []

    max_len = max(len(line) for line in lines)
    # Pad lines to ensure rectangular grid
    return [line.ljust(max_len) for line in lines]

