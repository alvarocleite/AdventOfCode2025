# AdventOfCode2025
[Advent of Code 2025 Official Website](https://adventofcode.com/2025)

AdventOfCode2025 contains my solutions for the Advent of Code 2025 puzzles. 

All solutions are implemented in Python and developed with the assistance of AI (Gemini CLI) to draft approaches, refine logic, and ensure high code quality. This project serves as both a coding challenge and a focused learning journey.

**Overview**

- **Language:** Python 3.10+
- **AI Assistance:** Gemini CLI
- **Progress:** Days 01 through 07 complete.
- **Key Features:** Shared utility module (`utils.py`), automated unit tests (`unittest`), and adherence to Clean Code principles.

![AdventOfCode2025_img](resources/AdventOfCode2025_img.png)

**Learning Goals**

My primary objective is to master Python. Specifically, I focus on:
- **Syntax Mastery:** Gaining fluency in Pythonic idioms.
- **Problem Solving:** Designing efficient algorithms for grid simulations, combinatorial parsing, and pathfinding.
- **Engineering Excellence:** Implementing modular design, robust error handling, and comprehensive documentation.

**Project Structure**

- **`dayXX/`**: Organized by day.
    - `dayXX.py`: The solution script containing `part01` and `part02`.
    - `test_dayXX.py`: Unit tests verifying both logic and execution against real input.
    - `Puzzle.txt`: Description of the day's challenge.
    - `PuzzleInput.txt`: Personal puzzle data.
- **`utils.py`**: Shared helper functions (e.g., robust file reading, grid padding).
- **`aoc2025env/`**: Dedicated Python virtual environment.

**Quick Start**

1.  **Set up the environment**:

```bash
   python3 -m venv aoc2025env
   source aoc2025env/bin/activate  # On Windows use `aoc2025env\Scripts\activate`
```

*Note: This project relies on the Python Standard Library, so no `pip install` is required.*

2.  **Run a solution**:

```bash
python day07/day07.py
```

3. **Run tests**:

```bash
# Run all tests
python -m unittest discover -p "test_day*.py"

# Run a specific day's tests with verbose output
python day01/test_day01.py
```

**AI Assistance Details**

This repository uses the Gemini CLI as a mentor and reviewer. The workflow includes:
- **Collaborative Drafting:** Discussing algorithms and strategies.
- **Structural Refactoring:** Consolidating repetitive code into reusable utilities.
- **Automated Verification:** Using AI to assist in writing unit tests.

**License**

See the repository [LICENSE](LICENSE).


