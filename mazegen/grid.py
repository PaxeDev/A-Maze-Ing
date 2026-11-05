from .square import Square, Direction
import random


class Grid:
    """Hold the maze and keep track of its state during generation."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
    ) -> None:
        """Set up a new grid, ready for a maze to be generated.

        This builds the grid of squares and starts the current position
        at the top-left corner (0, 0). The lists of potential splits and
        dead ends start empty.

        Args:
            width: How many squares wide the maze is.
            height: How many squares tall the maze is.
            perfect: True for a perfect maze with exactly one path between
                the entry and the exit, or False for a Pac-Man-style board
                with loops.
            seed: The seed for the random generator. Using the same seed
                with the same settings gives the same maze. Leave it as
                None to pick one at random.
        """
        self.__width: int = width
        self.__height: int = height
        self.__maze: list[list[Square]] = self.initialize_grid(width, height)
        self.__current_x: int = 0
        self.__current_y: int = 0
        self.__entry: tuple[int, int] = entry
        self.__exit: tuple[int, int] = exit
        self.__potential_splits: list[tuple[int, int]] = list()
        self.__dead_ends: list[tuple[int, int]] = list()
        self.__perfect: bool = perfect
        self.__seed: int = (
            seed if seed is not None else random.randrange(2 ** 32)
        )
        self.__random: random.Random = random.Random(self.__seed)

    PATTERN_42: tuple[tuple[int, int], ...] = (
        (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
        (1, -2), (2, -2), (3, -2), (3, -1), (3, 0), (2, 0), (1, 0),
        (1, 1), (1, 2), (2, 2), (3, 2),
    )

    def get_maze(self) -> list[list[Square]]:
        """Give back the grid of squares that makes up the maze.

        This returns the maze itself, not a copy, so any changes you make
        to it also change the grid.

        Returns:
            The squares in the maze, stored as a list of lists.
        """
        return self.__maze

    def initialize_grid(
        self,
        width: int,
        height: int,
    ) -> list[list[Square]]:
        """Build a new grid where every square starts fully closed.

        Each square starts with all four walls up, ready for the generator
        to carve paths through it. The grid is stored row by row, so you
        can reach a square with maze[y][x].

        Args:
            width: How many squares to put in each row.
            height: How many rows to create.

        Returns:
            The new grid of squares, stored as a list of rows.
        """
        return [[Square() for _ in range(width)]
                for _ in range(height)]

    def set_bounds(self, x: int, y: int, square: Square) -> None:
        """Mark which directions lead to another square.

        Squares along the edge of the maze have fewer neighbours, so this
        marks only the directions that stay inside the maze as True. For
        example, the top-left square gets east and south. Directions that
        lead outside the maze aren't changed.

        Args:
            x: The square's row, counted from the top.
            y: The square's column, counted from the left.
            square: The square to update.
        """
        width = self.__width - 1
        height = self.__height - 1
        if x == 0:
            if y == 0:
                square.set_square(east=True, south=True)
            elif y == width:
                square.set_square(west=True, south=True)
            else:
                square.set_square(west=True, east=True, south=True)
        elif x == height:
            if y == 0:
                square.set_square(east=True, north=True)
            elif y == width:
                square.set_square(west=True, north=True)
            else:
                square.set_square(west=True, east=True, north=True)
        else:
            if y == 0:
                square.set_square(east=True, north=True, south=True)
            elif y == width:
                square.set_square(west=True, north=True, south=True)
            else:
                square.set_square(
                    west=True,
                    east=True,
                    north=True,
                    south=True,
                )

    def get_42_squares(self) -> set[tuple[int, int]]:
        """Work out which squares the "42" pattern covers.

        Returns:
            The (x, y) position of every square in the pattern.
        """
        middle_x = self.__width // 2
        middle_y = self.__height // 2
        return {(middle_x + dx, middle_y + dy) for dx, dy in self.PATTERN_42}

    def add_42_pattern(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Reserve the squares that draw "42" in the middle of the maze.

        If the maze is too small, this prints a message and leaves the
        pattern out.

        Args:
            entry: The (x, y) position of the entry.
            exit_: The (x, y) position of the exit.

        Raises:
            ValueError: If the entry or exit is on the pattern.
        """
        if self.__width < 10 or self.__height < 8:
            print("Error: the maze is too small for the 42 pattern.")
            return
        squares = self.get_42_squares()
        if entry in squares or exit_ in squares:
            raise ValueError("ENTRY and EXIT can't be on the 42 pattern.")
        for x, y in squares:
            self.__maze[y][x].set_square(breakable=False, visited=True)

    def prepare_maze(self) -> None:
        for x, row in enumerate(self.__maze):
            for y, square in enumerate(row):
                self.set_bounds(x, y, square)
        if self.__height >= 8 and self.__width >= 10:
            self.add_42_pattern(self.__entry, self.__exit)

    def in_bounds_check(self, x: int, y: int) -> bool:
        """Check whether a position is inside the maze.

        Args:
            x: The row to check, counted from the top.
            y: The column to check, counted from the left.

        Returns:
            True if the position is inside the maze, or False if it's
            outside.
        """
        height = self.__height - 1
        width = self.__width - 1
        if x >= 0 and x <= height and y >= 0 and y <= width:
            return True
        return False

    def check_neighbors(
        self,
        x: int,
        y: int,
        check_visited: bool,
    ) -> list[Direction]:
        """Find which neighbouring squares can be moved into.

        This looks at the squares to the north, east, south and west. It
        skips any that are outside the maze or marked as unbreakable, such
        as the squares in the "42" pattern.

        Args:
            x: The row of the current square, counted from the top.
            y: The column of the current square, counted from the left.
            check_visited: True to also skip squares that have already
                been visited, or False to allow them.

        Returns:
            The directions of the usable neighbours, which may be empty.
        """
        offsets: list[tuple[Direction, int, int]] = [
            ("north", x - 1, y),
            ("east", x, y + 1),
            ("south", x + 1, y),
            ("west", x, y - 1),
        ]

        directions: list[Direction] = []

        for name, nx, ny in offsets:
            if self.in_bounds_check(nx, ny):
                cell = self.__maze[nx][ny]
                if not check_visited:
                    if cell.get_info("breakable"):
                        directions.append(name)
                else:
                    if cell.get_info("breakable"):
                        if not cell.get_info("visited"):
                            directions.append(name)

        return directions

    def choose_direction(
        self,
        possible_directions: list[Direction],
    ) -> Direction | None:
        """Pick one direction at random from the available options.

        Args:
            possible_directions: The directions to choose from.

        Returns:
            The chosen direction, or None if the list is empty.
        """
        if not possible_directions:
            return None
        return self.__random.choice(possible_directions)

    def go_back_one_step(self) -> None:
        """Move back to the most recently saved position.

        The saved position is removed from the list of potential splits
        and becomes the current position. This lets the generator go back
        and try another route after it reaches a dead end.
        """
        last_point: tuple[int, int] = self.__potential_splits.pop()
        self.__current_x = last_point[0]
        self.__current_y = last_point[1]

    def move_on_grid(
        self,
        direction: Direction,
    ) -> None:
        """Move the current position one square in the given direction.

        Going north or south changes the row, while going east or west
        changes the column. This doesn't check whether the move stays
        inside the maze, so check the direction first.

        Args:
            direction: The direction to move. This can be "north", "east",
                "south" or "west".
        """
        match direction:
            case "north":
                self.__current_x = self.__current_x - 1
            case "east":
                self.__current_y = self.__current_y + 1
            case "south":
                self.__current_x = self.__current_x + 1
            case "west":
                self.__current_y = self.__current_y - 1
            case _:
                pass

    def braid_maze(self) -> None:
        """Open up dead ends so the maze has loops.

        This goes through the saved dead ends and removes one random wall
        from each, updating both squares that share it. Only walls facing
        a breakable neighbour inside the maze can be removed. A square that
        is no longer a dead end gets skipped, and so does a dead end with
        no wall that can be removed, so a few dead ends may remain.

        Because this adds loops, it should only run on non-perfect mazes.
        """
        all_directions: list[Direction] = ["north", "east", "south", "west"]

        while self.__dead_ends:
            x, y = self.__dead_ends.pop()
            square = self.__maze[x][y]

            # count every closed wall, including outer walls
            # and walls facing the 42
            closed_walls: list[Direction] = [
                direction for direction in all_directions
                if square.is_wall_up(direction)
            ]

            # skip false dead ends and cells already opened by an earlier break
            if len(closed_walls) != 3:
                continue

            # only walls facing an in-bounds, breakable neighbour
            neighbors: list[Direction] = self.check_neighbors(
                x, y, check_visited=False
            )
            breakable_walls: list[Direction] = [
                direction for direction in neighbors
                if square.is_wall_up(direction)
            ]

            if not breakable_walls:
                continue

            chosen_wall = self.__random.choice(breakable_walls)

            match chosen_wall:
                case "north":
                    self.__maze[x][y].change_number("north")
                    self.__maze[x - 1][y].change_number("south")
                case "east":
                    self.__maze[x][y].change_number("east")
                    self.__maze[x][y + 1].change_number("west")
                case "south":
                    self.__maze[x][y].change_number("south")
                    self.__maze[x + 1][y].change_number("north")
                case "west":
                    self.__maze[x][y].change_number("west")
                    self.__maze[x][y - 1].change_number("east")

    def run_maze(self) -> None:
        self.prepare_maze()
        try:
            while (True):
                self.__maze[self.__current_x][self.__current_y].set_square(
                    visited=True
                )
                possible_directions = self.check_neighbors(
                    self.__current_x, self.__current_y, check_visited=True
                )
                if len(possible_directions) > 1:
                    self.__potential_splits.append((
                        self.__current_x, self.__current_y))
                direction = self.choose_direction(possible_directions)
                if not direction:
                    self.__dead_ends.append((
                        self.__current_x, self.__current_y))
                    if not self.__potential_splits:
                        if not self.__perfect:
                            self.braid_maze()
                        return
                    self.go_back_one_step()
                    continue
                if not self.in_bounds_check(self.__current_x,
                                            self.__current_y):
                    break
                match direction:
                    case "north":
                        self.__maze[self.__current_x][
                            self.__current_y
                        ].change_number("north")
                        self.__maze[self.__current_x - 1][
                            self.__current_y
                        ].change_number("south")
                        self.move_on_grid("north")
                    case "east":
                        self.__maze[self.__current_x][
                            self.__current_y
                        ].change_number("east")
                        self.__maze[self.__current_x][
                            self.__current_y + 1
                        ].change_number("west")
                        self.move_on_grid("east")
                    case "south":
                        self.__maze[self.__current_x][
                            self.__current_y
                        ].change_number("south")
                        self.__maze[self.__current_x + 1][
                            self.__current_y
                        ].change_number("north")
                        self.move_on_grid("south")
                    case "west":
                        self.__maze[self.__current_x][
                            self.__current_y
                        ].change_number("west")
                        self.__maze[self.__current_x][
                            self.__current_y - 1
                        ].change_number("east")
                        self.move_on_grid("west")
                    case _:
                        pass
        except KeyboardInterrupt as error:
            print(f"{error}")
