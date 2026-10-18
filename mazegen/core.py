from abc import ABC, abstractmethod
from typing import List, Set, Tuple


class BaseMazeGenerator(ABC):
    """Abstract base class for all maze generation algorithms.

    Enforces a strict contract: any child class MUST implement
    the abstract methods defined here.

    Attributes:
        width (int): The width of the maze measured in cells.
        height (int): The height of the maze measured in cells.
        entry (Tuple[int, int]): The (x, y) coordinates of the entry cell.
        exit (Tuple[int, int]): The (x, y) coordinates of the exit cell.
        output_file (str): The path where the maze will be exported.
        perfect (bool): Determines if the maze should be perfect (no loops).
        seed (int | None): The random seed used for maze generation.
        grid (List[List[int]]): The 2D matrix holding the bitwise wall logic.
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

        self.grid = self._initialize_grid()
        self.pattern_42: Set[Tuple[int, int]] = set()
        self.shortest_path_coords: Set[Tuple[int, int]] = set()

    def _initialize_grid(self) -> List[List[int]]:
        """Creates the empty maze grid based on the configuration dimensions.

        Uses a bitwise system where a closed wall sets the bit to 1:
        North=1, East=2, South=4, West=8. A fully closed cell is 15.

        Returns:
            List[List[int]]: A 2D matrix filled with solid blocks (15).
        """
        return [[15 for _ in range(self.width)]
                for _ in range(self.height)]

    @abstractmethod
    def generate(self) -> None:
        """Core algorithm logic to carve paths from ENTRY to EXIT.

        This method must modify self.grid using bitwise subtraction.
        It must also populate self.pattern_42 with the (x, y) coordinates
        of the pattern if dimensions allow it.
        """
        pass

    @abstractmethod
    def solve(self) -> str:
        """Calculates the shortest valid path from ENTRY to EXIT.

        The implementation must populate self.shortest_path_coords with all
        the (x, y) tuples that make up the path for UI rendering.

        Returns:
            str: A sequence of directional moves, e.g., "EESSWW".
        """
        pass

    def export_to_hex(self) -> None:
        """Converts the internal grid state into the hexadecimal string format.

        Appends the metadata block (entry, exit, shortest path) at the end
        of the file.

        Raises:
            ValueError: If the current grid dimensions do not match the
            expected config.
            OSError: If the system fails to write or open the output file.
        """
        if (len(self.grid) != self.height or
           len(self.grid[0]) != self.width):
            raise ValueError("Grid dimensions do not match configuration. "
                             f"Expected {self.width}x"
                             f"{self.height}.")
        try:
            with (open(self.output_file, 'w', encoding='utf-8')
                  as output_file):
                for row in self.grid:
                    hex_row = "".join(f"{cell:x}" for cell in row)
                    output_file.write(hex_row + "\n")
                output_file.write("\n")
                output_file.write(f"{self.entry[0]},"
                                  f"{self.entry[1]}\t# entry (x,y)\n")
                output_file.write(f"{self.exit[0]},"
                                  f"{self.exit[1]}\t# exit (x,y)\n")
                output_file.write(f"{self.solve()}\n")
        except OSError as e:
            raise OSError("Failed to write output file "
                          f"'{self.output_file}': {e}")


class MazeGenerator(BaseMazeGenerator):
    """Concrete implementation of the maze generation algorithms."""
    def generate(self) -> None:
        """Executes the path carving algorithm to build the maze."""
        # TODO: Implement the actual carving algorithm
        pass

    def solve(self) -> str:
        """Finds the shortest path through the generated maze.

        Returns:
            str: Sequence of directional movements.
        """
        # TODO: Implement the actual pathfinding algorithm
        return "N"  # Dummy return to satisfy the signature
