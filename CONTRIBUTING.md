# Contributing Guidelines

This document outlines the coding standards, workflows, and architectural agreements for the A-Maze-ing project. By following these guidelines, we ensure a unified codebase and a smooth collaboration process.

## 1. Git Workflow & Collaboration

To maintain a clean and readable history, we use a structured branching and merging strategy.

### Branch Naming Conventions
All active development must happen on dedicated branches. Never commit directly to `main`. Use the following prefixes:
* `feat/`: For new features or significant logic additions (e.g., `feat/maze-core`, `feat/config-parser`).
* `fix/`: For bug fixes (e.g., `fix/unreachable-exit`).
* `refactor/`: For code structure improvements that do not change behavior.
* `docs/`: For documentation updates (e.g., `docs/readme-update`).

### Commit Message Standard
Commit messages must be clear and concise. Use the imperative mood and prefix the message to indicate the scope:
* `FEAT: Add depth-first search for perfect maze generation`
* `FIX: Handle missing output file parameter in config`
* `DOCS: Update setup instructions in README`

### Merge Request Rules
* Open a Merge Request on GitLab once a feature is ready.
* The author cannot merge their own branch. The other team member must review the code.
* Before approval, the reviewer must ensure the branch passes `make lint` and runs without exceptions.

## 2. Local Environment Setup

Consistency in our local environments prevents "it works on my machine" issues. We use `uv` for lightning-fast dependency and Python version management.

### Virtual Environment
You do not need to create a virtual environment manually. Simply run the install command, and `uv` will automatically create the `.venv` (using Python 3.14+) and sync the dependencies from `uv.lock`.
```bash
make install
```
(Under the hood, this runs uv sync).

### Execution and Tooling
Always use the Makefile to run the project, tests, or linters, as it guarantees the execution happens inside the isolated `uv` environment.
```bash
make run
make test # optional if you create some tests
make lint
make lint-strict
```
*Ensure your editor is configured to use the `.venv/bin/python` interpreter so that type hints and linters work dynamically during development.*

## 3. Code Architecture & Style

This project strictly enforces code quality and static typing. 

### Type Hinting
All functions, methods, and variables must include type hints using the `typing` module. The codebase must pass `mypy` strict checks without errors.
* Use explicit return types, even for `None`.
* Avoid using `Any` unless absolutely necessary.

### Docstrings (PEP 257)
Every module, class, and function must be documented using the **Google Style** docstrings. It must clearly state the purpose, parameters (`Args:`), and return values (`Returns:`).
```python
def generate_perfect_maze(width: int, height: int, seed: int | None = None) -> list[list[int]]:
    """
    Generates a perfect maze using a depth-first search algorithm.

    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.
        seed (int | None, optional): Seed for the random generator. Defaults to None.

    Returns:
        list[list[int]]: A 2D array representing the maze walls in hexadecimal.
    """
```

### Error Handling & Resource Management
* **No hard crashes:** Use `try-except` blocks to handle unexpected behaviors gracefully (e.g., invalid configurations, missing files). 
* **Custom Exceptions:** Prefer raising context-specific errors (e.g., `InvalidConfigError`) rather than generic exceptions.
* **Context Managers:** Always use `with` statements when opening files or managing resources to prevent memory leaks.

## 4. Project Structure

To meet the reusability requirements, the codebase is strictly divided into two main parts:
1. **The CLI & UI (`a_maze_ing.py`):** Handles argument parsing, configuration reading, and the visual representation (Terminal/MLX).
2. **The Reusable Module (`mazegen/`):** Contains purely the maze generation and solving logic. This module must not contain print statements or UI logic, as it will be packaged into a `.whl` or `.tar.gz` file for external use.

## 5. Definition of Done (DoD)

Before requesting a review on a Merge Request, ensure the following checklist is met:
- [ ] Code passes `make lint` (both `flake8` and `mypy`) with no warnings or errors.
- [ ] All new functions and classes have PEP 257 compliant docstrings and type hints.
- [ ] Files and resources are managed using context managers.
- [ ] The program handles edge cases and does not crash on invalid inputs.
- [ ] If applicable, the feature was tested using `make run` and `make debug`.

