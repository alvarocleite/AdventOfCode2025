# AdventOfCode2025

AdventOfCode2025 contains my solutions for the Advent of Code 2025 puzzles. 

All solutions are implemented in Python and developed with the assistance of AI (Gemini CLI) to draft approaches, refine logic, and ensure high code quality. This project serves as both a coding challenge and a focused learning journey.

**Overview**

- **Language:** Python 3.10+
- **AI Assistance:** Gemini CLI
- **Progress:** Days 01 through 12 complete.
- **Key Features:** Shared utility module (`utils.py`), automated unit tests (`unittest`), and adherence to Clean Code principles.

![AdventOfCode2025_img](resources/AdventOfCode2025_img.png)

**The Agentic Coding Experiment**

This repository is more than just puzzle solutions; it is an experiment in **Agentic Coding**. 

> *"I am the Senior Engineer. Gemini is the Junior - a very capable one."*

The goal is to transition from manual coding to directing AI agents, mastering the workflow of the future. The project follows a strict operational rule where my role shifts from writing syntax to defining specifications and reviewing architecture.

**Methodology: The "Senior/Junior" Workflow**

We adhere to a rigorous 3-step process to ensure engineering excellence:

1.  **Strategy First:** No code is written until an algorithmic approach is discussed and agreed upon in plain English.
2.  **Code Generation:** The AI agent implements the solution based on the agreed strategy, strictly following Clean Code and SOLID principles.
3.  **Review & Refine:** I review the code. If it fails or is suboptimal, I do not fix it manually. Instead, I explain the error to the agent, forcing a deep understanding of the root cause and an architectural fix.

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
python day01/day01.py
```

3. **Run tests**:

```bash
# Run all tests
python -m unittest discover -p "test_day*.py"

# Run a specific day's tests with verbose output
python day01/test_day01.py
```

**License**

See the repository [LICENSE](LICENSE).

**Links**

[Advent of Code 2025 Official Website](https://adventofcode.com/2025)

