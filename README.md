*This project has been created as part of the 42 curriculum by olpachec and dpleschu.*

# A-Maze-ing

## Description
A-Maze-ing is a Python-based maze generator. It creates a customizable maze that can be either "perfect" (a single winding path with no loops) or a "playable board" (optimized for Pac-Man-like games with full connectivity and multiple routes).
The resulting structure is processed in two ways:
1. Saved to disk using a hexadecimal wall representation format.
2. Visually rendered in the terminal using an interactive `curses`-based interface with dynamic Unicode box-drawing characters and customizable color layers.

## Instructions
This project uses `uv` for lightning-fast dependency and virtual environment management.

**Installation**
```bash
make install
```
*This command automatically creates the Python 3.14 virtual environment and installs all dependencies (like `pydantic` and `pytest`) defined in the `uv.lock` file.*

**Interactive Viewer Controls**

Once the application is running, you can interact with the live maze visualization using the following keys:
* `[H]` - Toggle visibility of the shortest solution path.
* `[C]` - Cycle through different color palettes for the maze walls (White, Matrix Green, Neon Cyan).
* `[R]` - Regenerate a new maze dynamically (Work in Progress).
* `[Q]` - Quit the application and restore the terminal

**Execution**

To ensure safe processing, the application strictly requires the configuration file to have a .txt extension. You can run the project in two different ways:

*Method 1: Automated (Recommended)*
```bash
make run
```
*By default, this will execute the generator using the provided `config.txt` you can change the name in the Makefile `CONFIG = <your_filename>.txt`, inside the isolated `uv` environment.*

*Method 2: Manual*
```bash
source .venv/bin/activate
python3 a_maze_ing.py <your_filename>.txt
```

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
The project is strictly separated into two components to ensure external reusability:
1. **CLI & UI (`a_maze_ing.py`):** Handles argument parsing, configuration validation, and output rendering.
2. **Core Engine (`mazegen/`):** A standalone, pure-logic module containing the maze generation algorithms. This module contains no UI logic and is designed to be packaged as a `.whl` or `.tar.gz` file for easy installation in future projects.

### Using the `mazegen` Module
### Using the `mazegen` Module
The core logic relies on an abstract base class (`BaseMazeGenerator`). To create a new algorithm, you must inherit from this class and fulfill its strict contract. 

The UI engine (`CursesViewer`) automatically renders the maze based on the sets populated during generation.

**Implementation Example:**
```python
from mazegen.core import BaseMazeGenerator
from config import MazeConfig

class MyCustomGenerator(BaseMazeGenerator):
    
    def generate(self) -> None:
        # 1. Carve paths by modifying self.grid using bitwise operators
        # 2. Populate the exact coordinates of the 42 pattern (if applicable)
        self.pattern_42 = {(3, 3), (4, 3), (3, 4), (4, 4)}

    def solve(self) -> str:
        # 1. Calculate the shortest path using algorithms like BFS or A*
        # 2. Populate the path coordinates for the UI engine to render
        self.shortest_path_coords = {(0, 0), (0, 1), (1, 1)}
        
        return "ESS"  # Return the directional string (East, South, South)
```

## Algorithm Overview
*TODO: Detail the maze generation algorithm chosen (e.g., Depth-First Search, Prim's) and explain the reasoning behind this technical choice.*

## Team & Project Management
*TODO: Describe team roles, anticipated planning vs. actual evolution, what worked well, and what could be improved, any specific tools (uv, pydantic, pytest)*
This project enforces strict software engineering practices:
* **Separation of Concerns:** The maze logic (`mazegen/core.py`) is completely decoupled from the visualization layer (`mazegen/viewer.py`), ensuring scalability and testability.
* **Strict Typing:** Configured with `mypy` strict mode and `pyright` to catch type-related bugs at compile time. Data validation is rigidly handled by Pydantic.
* **Testing:** Comprehensive test suite utilizing `unittest.mock` to simulate real-time curses terminal interactions without requiring an active display.
* **Environment Isolation:** Managed entirely via `uv` to guarantee reproducible dependencies across all developer machines.

## Resources
* **AI Usage:** AI was utilized to configure the `uv` environment, establish CI/CD workflows, and draft some unit tests and README.
* https://opensource.guide/legal/#which-open-source-license-is-appropriate-for-my-project

* https://peps.python.org/pep-0257/

* https://en.wikipedia.org/wiki/Maze_generation_algorithm

* https://docs.astral.sh/uv/

* https://docs.python.org/3/library/curses.html

*(Add other tutorials, articles, or documentation links here as the project evolves)*