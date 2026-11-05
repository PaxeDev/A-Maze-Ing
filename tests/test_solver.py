# pyright: reportPrivateUsage=false
"""Unit tests for the AStarSolver pathfinding module."""

from typing import Set, Tuple
from mazegen.solver import AStarSolver
from mazegen.square import Square


def test_manhattan_distance() -> None:
    """Test Manhattan distance calculation between two points."""
    point_a = (0, 0)
    point_b = (3, 4)
    # |0 - 3| + |0 - 4| = 3 + 4 = 7
    distance = AStarSolver._manhattan_distance(point_a, point_b)
    assert distance == 7


def test_solve_simple_2x2_maze() -> None:
    """Test A* solver on a 2x2 Square grid with a deterministic path.

    Grid setup (2x2):
    (0,0): East wall open
    (1,0): West and South walls open
    (0,1): All walls closed
    (1,1): North wall open

    Path from (0,0) to (1,1): (0,0) -> East -> (1,0) -> South -> (1,1)
    """
    sq_0_0 = Square()
    sq_0_0.set_square(number=13)  # N, S, W closed; E open

    sq_1_0 = Square()
    sq_1_0.set_square(number=3)   # N, E closed; S, W open

    sq_0_1 = Square()
    sq_0_1.set_square(number=15)  # All walls closed

    sq_1_1 = Square()
    sq_1_1.set_square(number=14)  # E, S, W closed; N open

    grid = [
        [sq_0_0, sq_1_0],
        [sq_0_1, sq_1_1]
    ]
    path_str, path_coords = AStarSolver.solve(
        grid=grid,
        entry=(0, 0),
        exit_coord=(1, 1),
        width=2,
        height=2
    )

    assert path_str == "ES"
    expected_coords: Set[Tuple[int, int]] = {(0, 0), (1, 0), (1, 1)}
    assert path_coords == expected_coords


def test_solve_blocked_maze_returns_empty() -> None:
    """Test solver behavior when destination is completely walled off."""
    grid = [
        [Square(), Square()],
        [Square(), Square()]
    ]
    path_str, path_coords = AStarSolver.solve(
        grid=grid,
        entry=(0, 0),
        exit_coord=(1, 1),
        width=2,
        height=2
    )

    assert path_str == ""
    assert path_coords == set()


def test_a_star_open_grid() -> None:
    """Test A* solver on a 2x2 grid where all walls are open."""
    sq_open_1 = Square()
    sq_open_1.set_square(number=0)
    sq_open_2 = Square()
    sq_open_2.set_square(number=0)
    sq_open_3 = Square()
    sq_open_3.set_square(number=0)
    sq_open_4 = Square()
    sq_open_4.set_square(number=0)

    grid = [
        [sq_open_1, sq_open_2],
        [sq_open_3, sq_open_4]
    ]
    path, coords = AStarSolver.solve(grid, (0, 0), (1, 1), 2, 2)

    assert len(path) > 0
    assert (0, 0) in coords
    assert (1, 1) in coords
