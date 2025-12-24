
import os
from typing import Callable

DIAL_START_POS = 50
DIAL_SIZE = 100

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def read_input_file(file_path: str) -> list[str]:
    """Reads lines from a specified text file and strips whitespace from each line.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list[str]: A list of strings, where each string is a line from the file
                   with leading/trailing whitespace removed.
    """

    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    return lines

def get_rot_dir_and_distance(move: str) -> tuple[str, int]:
    """Parses a move string to extract the rotation direction and distance.

    Args:
        move (str): A string representing a move (e.g., "R31", "L49").

    Returns:
        tuple[str, int]: A tuple containing the direction ('L' or 'R') and the
                         integer distance.

    Raises:
        ValueError: If the move string is empty.
    """

    # Validate and parse the move string
    move = move.strip()
    if not move:
        raise ValueError("empty move string")

    # Extract direction and distance
    direction = move[0]
    distance_str = move[1:]

    # Normalize direction and convert distance to integer
    direction = direction.upper()
    distance = int(distance_str)
    
    return direction, distance


def get_position_after_move(position: int, move: str) -> tuple[int, int]:
    """Calculates the new dial position and the number of times zero was reached.

    Args:
        position (int): The current position of the dial (0-99).
        move (str): A string representing the rotation (e.g., "R31", "L49").

    Returns:
        tuple[int, int]: A tuple containing:
            - int: The new position of the dial (0-99).
            - int: The number of times the dial clicked on zero during the move,
                   calculated using direction-specific floor division to count
                   multiples of DIAL_SIZE crossed.
    """

    # Parse the move to get direction and distance
    direction, distance = get_rot_dir_and_distance(move)
    
    # Calculate the raw new position before wrapping
    if direction == 'R':
        raw_end_position = position + distance
        crossings = raw_end_position // DIAL_SIZE - position // DIAL_SIZE
    else: # direction == 'L'
        raw_end_position = position - distance
        crossings = (position - 1) // DIAL_SIZE - (raw_end_position - 1) // DIAL_SIZE
    
    # Handle wrap-around for the final position
    new_position = raw_end_position % DIAL_SIZE
            
    return new_position, crossings

def count_times_dial_at_zero(dial_start_pos: int, moves: list[str]) -> int:
    """Calculates how many times the dial lands exactly on position 0 after a sequence of moves.

    Args:
        dial_start_pos (int): The initial position of the dial (0-99).
        moves (list[str]): A list of move strings (e.g., ["R31", "L49"]).

    Returns:
        int: The total count of times the dial is at position 0 after each move.
    """

    # Initialize position and counter
    position = dial_start_pos
    times_at_zero_counter = 0

    # Process each move and check for position 0
    for move in moves:
        position, _ = get_position_after_move(position, move)
        if position == 0:
            times_at_zero_counter += 1
            
    return times_at_zero_counter

def count_times_dial_passed_zero(dial_start_pos: int, moves: list[str]) -> int:
    """Calculates the total number of times the dial passes over position 0 across all moves.

    This includes any clicks on 0 that occur *during* a rotation, not just at the end.

    Args:
        dial_start_pos (int): The initial position of the dial (0-99).
        moves (list[str]): A list of move strings (e.g., ["R31", "L49"]).

    Returns:
        int: The total count of times the dial registers a click on zero.
    """

    # Initialize position and counter
    position = dial_start_pos
    times_passed_zero_counter = 0

    # Process each move and check for passing over position 0
    for move in moves:
        position, passes = get_position_after_move(position, move)
        times_passed_zero_counter += abs(passes)
            
    return times_passed_zero_counter

def part01(input_lines: list[str]):
    """Executes Part 1 of the Advent of Code Day 1 puzzle.

    Calculates the number of times the dial is at zero and prints the result.

    Args:
        input_lines (list[str]): The list of move instructions.
    """

    print("Advent of Code 2025 - Day 1 - Part 1")
    dial_start_pos = DIAL_START_POS
    times_at_zero = count_times_dial_at_zero(dial_start_pos, input_lines)
    print(f"Time of Dial at Zero position: {times_at_zero}")

def part02(input_lines: list[str]):
    """Executes Part 2 of the Advent of Code Day 1 puzzle.

    Calculates the number of times the dial passes over zero and prints the result.

    Args:
        input_lines (list[str]): The list of move instructions.
    """
    print("Advent of Code 2025 - Day 1 - Part 2")
    dial_start_pos = DIAL_START_POS
    times_passed_zero = count_times_dial_passed_zero(dial_start_pos, input_lines)
    print(f"Time of Dial passed Zero position: {times_passed_zero}")

def main():
    """Main function to run the Advent of Code Day 1 solutions.
    Parse Input file and
    Calls Part 1 and Part 2 functions.
    """

    # Parse Input file
    input_lines = read_input_file(INPUT_FILE_PATH)
    
    part01(input_lines)
    
    part02(input_lines)


if __name__ == "__main__":
    main()
