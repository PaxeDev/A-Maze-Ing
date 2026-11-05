from typing import Set, Tuple, List
from mazegen.solver import AStarSolver
from .square import Square
from mazegen.grid import Grid


class MazeGenerator:
    """Concrete class for maze generation.

    Attributes:
        width (int): The width of the maze measured in cells.
        height (int): The height of the maze measured in cells.
        entry (Tuple[int, int]): The (x, y) coordinates of the entry cell.
        exit (Tuple[int, int]): The (x, y) coordinates of the exit cell.
        output_file (str): The path where the maze will be exported.
        perfect (bool): Determines if the maze should be perfect (no loops).
        seed (int | None): The random seed used for maze generation.
        grid (List[List[Square]]): The 2D matrix holding the Square objects.
        pattern_42 (Set[Tuple[int, int]]): Coordinates for the 42 pattern.
        shortest_path_coords (Set[Tuple[int, int]]): Coordinates of the
            solution path.
    """

    def __init__(self, width: int,
                 height: int,
                 entry_coord: Tuple[int, int],
                 exit_coord: Tuple[int, int],
                 output_file: str,
                 perfect: bool = False,
                 seed: int | None = None) -> None:
        """Initializes the generator with decoupled configuration parameters.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.
            entry_coord (Tuple[int, int]): The (x, y) entry coordinates.
            exit_coord (Tuple[int, int]): The (x, y) coordinates for the exit.
            output_file (str): Destination path for the generated text file.
            perfect (bool, optional): If True, creates a maze with a single
                valid path. Defaults to False.
            seed (int | None, optional): Random seed for reproducible
                generation. Defaults to None.
        """

        self.width = width
        self.height = height
        self.entry = entry_coord
        self.exit = exit_coord
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

        self.grid: List[List[Square]] = []
        self.pattern_42: Set[Tuple[int, int]] = set()
        self.shortest_path_coords: Set[Tuple[int, int]] = set()

    def export_to_hex(self) -> None:
        """Converts the internal grid state into hexadecimal string format.

        Appends the metadata block (entry, exit, shortest path) at the end
        of the output file.

        Raises:
            ValueError: If the current grid dimensions do not match the
                expected configuration.
            OSError: If the system fails to write or open the output file.
        """
        if (len(self.grid) != self.height or
           len(self.grid[0]) != self.width):
            raise ValueError("Grid dimensions do not match configuration. "
                             f"Expected {self.width}x"
                             f"{self.height}.")
        try:
            with open(self.output_file, 'w', encoding='utf-8') as output_file:
                for row in self.grid:
                    hex_row = ""
                    for cell in row:
                        hex_row += f"{cell.get_info('number'):x}"
                    output_file.write(hex_row + "\n")
                output_file.write("\n")
                output_file.write(f"{self.entry[0]},"
                                  f"{self.entry[1]}\n")
                output_file.write(f"{self.exit[0]},"
                                  f"{self.exit[1]}\n")
                output_file.write(f"{self.solve()}\n")
        except OSError as e:
            raise OSError("Failed to write output file "
                          f"'{self.output_file}': {e}")

    def generate(self) -> None:
        """Delegates the full generation process to the Grid class, absorbs
        the completely generated maze, and exports the final grid to disk.
        """
        maze_engine = Grid(self.width,
                           self.height,
                           self.entry,
                           self.exit,
                           self.perfect,
                           self.seed)
        maze_engine.run_maze()
        self.grid = maze_engine.get_maze()
        self.export_to_hex()

    def solve(self) -> str:
        """Calculates the shortest valid path from ENTRY to EXIT.

        Populates self.shortest_path_coords with all the (x, y) tuples that
        make up the path for UI rendering.

        Returns:
            str: A sequence of directional moves, e.g., "EESSWW".
        """
        path_str, path_coords = AStarSolver.solve(
            grid=self.grid,
            entry=self.entry,
            exit_coord=self.exit,
            width=self.width,
            height=self.height
        )
        self.shortest_path_coords = path_coords
        return path_str
