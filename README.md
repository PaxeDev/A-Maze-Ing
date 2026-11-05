*This project has been created as part of the 42 curriculum by olpachec and dpleschu.*

# A-Maze-ing

## Description
A-Maze-ing is a Python-based maze generator. It creates a customizable maze that can be either "perfect" (a single winding path with no loops) or a "playable board" (optimized for Pac-Man-like games with full connectivity and multiple routes).
The resulting structure is processed in two ways:
1. Saved to disk using a hexadecimal wall representation format.
2. Visually rendered in the terminal using an interactive `curses`-based interface with dynamic Unicode box-drawing characters and customizable color layers.

## Instructions
This project uses `uv` for dependency and virtual environment management.

**Installation**
```bash
make install
```
*This command automatically creates the Python 3.14.* virtual environment and installs all dependencies (like `pydantic` and `pytest`) defined in the `uv.lock` file.*

**Execution**

To ensure safe processing, the application strictly requires the configuration file to have a .txt extension. You can run the project in two different ways:

*Method 1: Automated (Recommended)*
```bash
make
```
*By default, this will execute the generator using the provided `config.txt` you can change the name in the Makefile `CONFIG=<your_filename>.txt`, inside the isolated `uv` environment.*

*Method 2: Manual*
```bash
uv run a_maze_ing.py <your_config_file>.txt
```

**Interactive Viewer Controls**

Once the application is running, you can interact with the live maze visualization using the following keys:
* `[H]` - Toggle visibility of the shortest solution path.
* `[C]` - Cycle through different color palettes for the maze walls (White, Matrix Green, Neon Cyan).
* `[R]` - Regenerate a new maze dynamically.
* `[Q]` - Quit the application and restore the terminal.

**Development & Quality**
```bash
make test          # Runs the comprehensive pytest suite
make lint          # Runs flake8 and mypy checks
make lint-strict   # Runs mypy in strict mode
```

## Configuration File Format
The program is controlled via a plain text configuration file utilizing a `KEY=VALUE` format. Lines starting with `#` are ignored as comments.

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Is the maze perfect? (True/False) | `PERFECT=True` |
| `SEED` | To replicate the maze (optional) | `Seed=int` |

## Architecture & Reusability
The project is separated into two components to ensure external reusability:
1. **CLI & UI (`a_maze_ing.py`, `viewer.py`):** Handles argument parsing, configuration validation, and interactive terminal rendering.
2. **Core Engine (`mazegen/`):** A standalone, pure-logic module containing the maze generation algorithms. This module contains no UI logic and is designed to be packaged as a `.whl` or `.tar.gz` file for easy installation in future projects.

### Using the `mazegen` Module
The `mazegen` package provides a standalone maze generation class designed for easy integration into future projects (such as game engines or web servers). It requires no external dependencies or CLI tools to operate.

**1. Instantiate and use the generator**
You can initialize the generator using standard Python data types.

```python
from mazegen import MazeGenerator

# Basic initialization
maze = MazeGenerator(
    width=25,
    height=20,
    entry_coord=(0, 0),
    exit_coord=(24, 19),
    output_file="my_maze.txt"
)

# Carve the maze paths
maze.generate()
```
**2. Pass custom parameters**
You can customize the algorithmic behavior by passing optional parameters, such as making the maze "perfect" (no loops) or setting a random seed for reproducibility.
```python
# Custom initialization for a reproducible, perfect maze
custom_maze = MazeGenerator(
    width=15,
    height=15,
    entry_coord=(1, 1),
    exit_coord=(13, 13),
    output_file="custom_maze.txt",
    perfect=True,
    seed=42 # Ensures the same maze layout is generated every time
)
custom_maze.generate()
```
**3. Access the generated structure and solution**
```python
# Access the 2D grid structure (List[List[int]] using bitwise walls)
grid_structure = maze.grid

# Get the directional string solution (e.g., "EESSWW")
solution_moves = maze.solve()

# Access the exact (x, y) coordinates of the calculated shortest path
solution_coords = maze.shortest_path_coords

# Export the raw hexadecimal structure to disk
maze.export_to_hex()
```

## Algorithm Overview
For the maze creation algorithm we chose to implement Depth-First Search algorithm.
The reasonign behind this choice was mainly because we could use the the same algorithm for both creating the initial perfect maze (only one valid way from starting point to end point) as well as the braiding itself (additionally breaking down walls to create a more pacman-esque board where the player doesnt get stuck if tehy choose to go down a dead end).

## Team & Project Management
### Team Roles

- **olpachec (Software Architecture & UI):** Responsible for strict configuration parsing (`Pydantic`), environment setup (`uv`, Makefile), testing suite, and the interactive terminal rendering engine (`CursesViewer`) and solving logic.
- **dpleschu (Algorithmic Engineering):** Responsible for implementing the core generation within the concrete `MazeGenerator` class.

### Anticipated Planning & Evolution
Our initial plan was to build and manage the project using standard Python virtual environments (`venv`). However, during the early research phase, we discovered `uv`. We adapted our plan to adopt `uv` because it provided dependency management and significantly simplified the architecture needed to eventually export our `mazegen` directory as a standalone, reusable package.

### What Worked Well & What Could Be Improved
- **What worked well:** 
  - **Test-First Approach:** Writing unit tests even before writing the logic helped us understand the exact architectural structure required and anticipate edge cases, especially when implementing the `Pydantic` data validators.
  - **Git Branching Strategy:** Since we worked on independent, utilizing strict feature branches and merge requests provided great learnings. It allowed us to review the project piece by piece, making it much easier to understand how the codebase was evolving compared to reviewing a massive single merge.
- **What could be improved:** While independent work was highly effective, scheduling regular briefs before defining complex architectural structures (like the Square class) could further reduce the back-and-forth during code reviews.

### Technical Tooling
This project enforces strict software engineering practices using specific tools:

* **Separation of Concerns:** The maze logic (`mazegen/core.py`) is completely decoupled from the visualization layer (`viewer.py` at the project root), ensuring scalability and testability.
* **Strict Typing:** Configured with `mypy` strict mode and `pyright` to catch type-related bugs at compile time. Data validation is rigidly handled by Pydantic.
* **Environment Isolation:** Managed entirely via `uv` to guarantee reproducible dependencies across all developer machines.
* **Testing:** Comprehensive test suite utilizing `pytest` and `unittest.mock` to simulate real-time curses terminal interactions without requiring an active display.
* **Terminal UI:** Utilizes curses for interactive UI rendering without heavy external graphical libraries.

## Resources
* **AI Usage:** AI was utilized to configure the `uv` environment, establish CI/CD workflows, and draft some unit tests.
* https://opensource.guide/legal/#which-open-source-license-is-appropriate-for-my-project

* https://peps.python.org/pep-0257/

* https://en.wikipedia.org/wiki/Maze_generation_algorithm

* https://docs.astral.sh/uv/

* https://docs.python.org/3/library/curses.html

* https://www.youtube.com/watch?v=uctN47p_KVk "What School Didn't Tell You About Mazes" by mattbatwings for a very nice overview of different maze creation algorithms.
