"""
Maze generation package.

This package provides the core logic for generating and solving mazes.
It exposes the concrete `MazeGenerator` class to be used as
a standalone module.
"""
from .maze_generator import MazeGenerator

__all__ = ["MazeGenerator"]
