from abc import ABC, abstractmethod
from typing import List, Set, Tuple
from config import MazeConfig


class BaseMazeGenerator(ABC):
    """
    Abstract base class for all maze generation algorithms.
    Enforces a strict contract: any child class MUST implement
    the abstract methods defined here.
    """

    def __init__(self, config: MazeConfig) -> None:
        """
        Initializes the generator with a fully validated configuration.

        Args:
            config (MazeConfig): The Pydantic validated configuration object.
        """
        self.config = config
        self.grid = self._initialize_grid()
        self.pattern_42: Set[Tuple[int, int]] = set()
        self.shortest_path_coords: Set[Tuple[int, int]] = set()

    def _initialize_grid(self) -> List[List[int]]:
        """
        Creates the empty maze grid based on the configuration dimensions.
        Using a bitwise system where a closed wall sets the bit to 1:
        North=1, East=2, South=4, West=8.

        A cell with all walls closed is 15 (1+2+4+8).

        Returns:
            List[List[int]]: A 2D matrix filled with solid blocks (15).
        """
        return [[15 for _ in range(self.config.WIDTH)]
                for _ in range(self.config.HEIGHT)]

    @abstractmethod
    def generate(self) -> None:
        """
        Core algorithm logic to carve paths from ENTRY to EXIT.
        This method modifies self.grid using bitwise subtraction.

        If the maze dimensions meet the minimum requirements,
        the implementation MUST populate self.pattern_42 with
        the (x, y) coordinates of the pattern.
        """
        pass

    @abstractmethod
    def solve(self) -> str:
        """
        Calculates the shortest valid path from ENTRY to EXIT.

        The implementation MUST populate self.shortest_path_coords with all
        the (x, y) tuples that make up the path for UI rendering.

        Returns:
            str: A sequence of directional moves, e.g., "EESSWW".
        """
        pass

    def export_to_hex(self) -> None:
        """
        Converts the internal grid state into the hexadecimal string format,
        appending the metadata block (entry, exit, shortest path) at the end.
        """
        if (len(self.grid) != self.config.HEIGHT or
           len(self.grid[0]) != self.config.WIDTH):
            raise ValueError("Grid dimensions do not match configuration. "
                             f"Expected {self.config.WIDTH}x"
                             f"{self.config.HEIGHT}.")
        try:
            with (open(self.config.OUTPUT_FILE, 'w', encoding='utf-8')
                  as output_file):
                for row in self.grid:
                    hex_row = "".join(f"{cell:x}" for cell in row)
                    output_file.write(hex_row + "\n")
                output_file.write("\n")
                output_file.write(f"{self.config.ENTRY[0]},"
                                  f"{self.config.ENTRY[1]}\t# entry (x,y)\n")
                output_file.write(f"{self.config.EXIT[0]},"
                                  f"{self.config.EXIT[1]}\t# exit (x,y)\n")
                output_file.write(f"{self.solve()}\n")
        except OSError as e:
            raise OSError("Failed to write output file "
                          f"'{self.config.OUTPUT_FILE}': {e}")
