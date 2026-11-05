import heapq
from typing import List, Tuple, Dict, Set
from mazegen.square import Square


class AStarSolver:
    """A* Pathfinding algorithm implementation for 2D maze grids.

    Attributes:
        WALL_N (int): Bitmask constant for North wall (1).
        WALL_E (int): Bitmask constant for East wall (2).
        WALL_S (int): Bitmask constant for South wall (4).
        WALL_W (int): Bitmask constant for West wall (8).
        DIRECTIONS (List[Tuple[int, int, int, str]]): List of movement vectors
            defined as (delta_x, delta_y, wall_bit_mask, direction_char).
    """

    WALL_N = 1
    WALL_E = 2
    WALL_S = 4
    WALL_W = 8

    DIRECTIONS: List[Tuple[int, int, int, str]] = [
        (0, -1, WALL_N, 'N'),
        (1, 0, WALL_E, 'E'),
        (0, 1, WALL_S, 'S'),
        (-1, 0, WALL_W, 'W')
    ]

    @staticmethod
    def _manhattan_distance(
        start_coord: Tuple[int, int],
        target_coord: Tuple[int, int]
    ) -> int:
        """Calculates the Manhattan distance between two 2D coordinates.

        Args:
            start_coord (Tuple[int, int]): Starting (x, y) coordinates.
            target_coord (Tuple[int, int]): Target (x, y) coordinates.

        Returns:
            int: Calculated Manhattan distance.
        """
        return (abs(start_coord[0] - target_coord[0]) +
                abs(start_coord[1] - target_coord[1]))

    @classmethod
    def solve(
        cls,
        grid: List[List[Square]],
        entry: Tuple[int, int],
        exit_coord: Tuple[int, int],
        width: int,
        height: int
    ) -> Tuple[str, Set[Tuple[int, int]]]:
        """Finds the shortest path from entry to exit using the A* algorithm.

        Args:
            grid (List[List[Square]]): 2D matrix holding Square objects.
            entry (Tuple[int, int]): Entry (x, y) coordinates.
            exit_coord (Tuple[int, int]): Destination (x, y) coordinates.
            width (int): Width of the grid in cells.
            height (int): Height of the grid in cells.

        Returns:
            Tuple[str, Set[Tuple[int, int]]]: A tuple containing:
                - Directional movement string (e.g., "EESSNW").
                - Set of (x, y) coordinates representing the solution path.
        """
        # Priority queue storing nodes to evaluate: (f_score, pos_x, pos_y)
        open_set: List[Tuple[int, int, int]] = []
        initial_f_score = cls._manhattan_distance(entry, exit_coord)
        heapq.heappush(open_set, (initial_f_score, entry[0], entry[1]))

        # Exact cost from entry coordinate to each evaluated point
        g_cost: Dict[Tuple[int, int], int] = {entry: 0}

        # Maps child_coord -> (parent_coord, move_direction)
        came_from: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

        while open_set:
            _, current_x, current_y = heapq.heappop(open_set)
            current_coord = (current_x, current_y)

            # Reconstruct route if destination is reached
            if current_coord == exit_coord:
                return cls._reconstruct_path(came_from, current_coord)

            # 1. Retrieve current cell value
            current_square = grid[current_y][current_x]
            cell_val = current_square.get_info("number")

            # 2. Iterate through all 4 possible movement directions
            for (
                delta_x,
                delta_y,
                wall_mask,
                direction_char,
            ) in cls.DIRECTIONS:
                # 3. Skip direction if a wall
                # blocks the path in the current cell
                if (cell_val & wall_mask) != 0:
                    continue

                # Calculate neighbor coordinates
                neighbor_x = current_x + delta_x
                neighbor_y = current_y + delta_y

                # Ensure neighbor is within grid bounds
                if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                    neighbor_coord = (neighbor_x, neighbor_y)
                    tentative_g_cost = g_cost[current_coord] + 1

                    if (neighbor_coord not in g_cost
                       or tentative_g_cost < g_cost[neighbor_coord]):

                        g_cost[neighbor_coord] = tentative_g_cost
                        came_from[neighbor_coord] = (current_coord,
                                                     direction_char)

                        f_score = tentative_g_cost + cls._manhattan_distance(
                            neighbor_coord, exit_coord)
                        heapq.heappush(
                            open_set,
                            (f_score, neighbor_x, neighbor_y))

        return "", set()

    @classmethod
    def _reconstruct_path(
        cls,
        came_from: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]],
        current_coord: Tuple[int, int]
    ) -> Tuple[str, Set[Tuple[int, int]]]:
        """Reconstructs movement string and set of path coordinates.

        Args:
            came_from (Dict[Tuple[int, int], Tuple[Tuple[int, int], str]]):
                Mapping from child coordinate to (parent_coord, move_direction)
            current_coord (Tuple[int, int]): Reached exit coordinate.

        Returns:
            Tuple[str, Set[Tuple[int, int]]]: A tuple containing:
                - Directional movement string ordered from entry to exit.
                - Set of (x, y) coordinates along the solution path.
        """
        path_coords: Set[Tuple[int, int]] = {current_coord}
        directional_moves: List[str] = []

        node_pointer = current_coord
        while node_pointer in came_from:
            parent_coord, move_direction = came_from[node_pointer]
            directional_moves.append(move_direction)
            path_coords.add(parent_coord)
            node_pointer = parent_coord

        directional_moves.reverse()
        return "".join(directional_moves), path_coords
