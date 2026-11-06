import curses
from mazegen import MazeGenerator
from mazegen.square import Square


class CursesViewer:
    """Handles the interactive terminal visualization of the maze using curses.

    Attributes:
        maze (MazeGenerator): The maze generator containing the grid logic.
        show_path (bool): Flag determining if the solution path is rendered.
        color_idx (int): Current color palette index for rendering walls.
        WALL_N (int): Bitmask constant for the North wall (1).
        WALL_E (int): Bitmask constant for the East wall (2).
        WALL_S (int): Bitmask constant for the South wall (4).
        WALL_W (int): Bitmask constant for the West wall (8).
        COLOR_PATTERN (int): Color pair ID for the 42 pattern.
        COLOR_PATH (int): Color pair ID for the shortest path route.
        COLOR_WALL_1 (int): Color pair ID for the primary wall style.
        COLOR_WALL_2 (int): Color pair ID for the secondary wall style.
        COLOR_WALL_3 (int): Color pair ID for the tertiary wall style.
        COLOR_ENTRY (int): Color pair ID for the entry cell background.
        COLOR_EXIT (int): Color pair ID for the exit cell background.
    """

    WALL_N = 1
    WALL_E = 2
    WALL_S = 4
    WALL_W = 8

    COLOR_PATTERN = 1
    COLOR_PATH = 2
    COLOR_WALL_1 = 3
    COLOR_WALL_2 = 4
    COLOR_WALL_3 = 5
    COLOR_ENTRY = 6
    COLOR_EXIT = 7

    def __init__(self, maze_generator: MazeGenerator) -> None:
        """Initializes the CursesViewer with a generated maze.

        Args:
            maze_generator (MazeGenerator): An instance of the public
                maze generator.
        """
        self.maze = maze_generator
        self.show_path = True
        self.color_idx = 3

    def _get_cell_val(self, x: int, y: int) -> int:
        """Extracts integer wall bitmask directly from a Square object.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            int: Integer bitmask representation of cell walls.
        """
        square: Square = self.maze.grid[y][x]
        return square.get_info("number")

    def _get_pillar_char(self, pillar_x: int, pillar_y: int) -> str:
        """Calculates the precise Unicode character for a wall intersection.

        Inspects the logical walls of the surrounding cells to select the
        correct Unicode box-drawing character.

        Args:
            pillar_x (int): The x-coordinate (column) of the pillar.
            pillar_y (int): The y-coordinate (row) of the pillar.

        Returns:
            str: A single Unicode character representing the intersection.
        """
        width = self.maze.width
        height = self.maze.height

        up = down = left = right = False

        if pillar_y > 0:
            if pillar_x < width:
                up = bool(self._get_cell_val(pillar_x,
                                             pillar_y - 1) & self.WALL_W)
            else:
                up = bool(self._get_cell_val(pillar_x - 1,
                                             pillar_y - 1) & self.WALL_E)

        if pillar_y < height:
            if pillar_x < width:
                down = bool(self._get_cell_val(pillar_x,
                                               pillar_y) & self.WALL_W)
            else:
                down = bool(self._get_cell_val(pillar_x - 1,
                                               pillar_y) & self.WALL_E)

        if pillar_x > 0:
            if pillar_y < height:
                left = bool(self._get_cell_val(pillar_x - 1,
                                               pillar_y) & self.WALL_N)
            else:
                left = bool(self._get_cell_val(pillar_x - 1,
                                               pillar_y - 1) & self.WALL_S)

        if pillar_x < width:
            if pillar_y < height:
                right = bool(self._get_cell_val(pillar_x,
                                                pillar_y) & self.WALL_N)
            else:
                right = bool(self._get_cell_val(pillar_x,
                                                pillar_y - 1) & self.WALL_S)

        idx = ((1 if up else 0) + (2 if right else 0) +
               (4 if down else 0) + (8 if left else 0))

        UNICODE_PILLARS = (
            ' ', '╵', '╶', '└', '╷', '│', '┌', '├',
            '╴', '┘', '─', '┴', '┐', '┤', '┬', '┼'
        )
        return UNICODE_PILLARS[idx]

    def draw_ui(self, stdscr: 'curses.window') -> None:
        """Draws the expanded maze grid and the interactive menu.

        Args:
            stdscr (curses.window): The main curses window object.
        """
        stdscr.clear()

        for y, row in enumerate(self.maze.grid):
            for x, square_obj in enumerate(row):
                screen_y = y * 2
                screen_x = x * 4

                cell_val = square_obj.get_info("number")
                has_north = bool(cell_val & self.WALL_N)
                has_east = bool(cell_val & self.WALL_E)
                has_south = bool(cell_val & self.WALL_S)
                has_west = bool(cell_val & self.WALL_W)

                try:
                    wall_color = curses.color_pair(self.color_idx)
                    stdscr.addstr(screen_y, screen_x,
                                  self._get_pillar_char(x, y),
                                  wall_color)
                    stdscr.addstr(screen_y, screen_x + 4,
                                  self._get_pillar_char(x + 1, y),
                                  wall_color)
                    stdscr.addstr(screen_y + 2, screen_x,
                                  self._get_pillar_char(x, y + 1),
                                  wall_color)
                    stdscr.addstr(screen_y + 2, screen_x + 4,
                                  self._get_pillar_char(x + 1, y + 1),
                                  wall_color)
                    if has_north:
                        stdscr.addstr(screen_y, screen_x + 1, "───",
                                      wall_color)
                    if has_south:
                        stdscr.addstr(screen_y + 2, screen_x + 1, "───",
                                      wall_color)
                    if has_west:
                        stdscr.addstr(screen_y + 1, screen_x, "│", wall_color)
                    if has_east:
                        stdscr.addstr(screen_y + 1, screen_x + 4, "│",
                                      wall_color)

                    is_pattern = not square_obj.get_info("breakable")
                    is_path = (self.show_path and
                               (x, y) in self.maze.shortest_path_coords)
                    is_entry = ((x, y) == self.maze.entry)
                    is_exit = ((x, y) == self.maze.exit)

                    if is_entry:
                        stdscr.addstr(screen_y + 1, screen_x + 1, "   ",
                                      curses.color_pair(self.COLOR_ENTRY))
                    elif is_exit:
                        stdscr.addstr(screen_y + 1, screen_x + 1, "   ",
                                      curses.color_pair(self.COLOR_EXIT))
                    elif is_pattern:
                        stdscr.addstr(screen_y + 1, screen_x + 1, "   ",
                                      curses.color_pair(self.COLOR_PATTERN))
                    elif is_path:
                        stdscr.addstr(screen_y + 1, screen_x + 1, "   ",
                                      curses.color_pair(self.COLOR_PATH))
                except curses.error:
                    pass

        ui_y = (self.maze.height * 2) + 1
        path_status = 'Yes' if self.show_path else 'No'

        try:
            stdscr.addstr(ui_y, 0, "=== CONTROLS ===", curses.A_BOLD)
            stdscr.addstr(ui_y + 1, 0, f"Path visible: {path_status}")
            stdscr.addstr(ui_y + 2, 0,
                          "Controls: [R]egenerate  "
                          "|  [H]ide Path  |  [C]olor  |  [Q]uit")
        except curses.error:
            pass

        stdscr.refresh()

    def _interactive_loop(self, stdscr: 'curses.window') -> None:
        """Executes the main event loop for keyboard capture and UI updates.

        Args:
            stdscr (curses.window): The main curses window object.
        """
        curses.curs_set(0)
        stdscr.nodelay(False)

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.COLOR_PATTERN,
                         curses.COLOR_BLACK,
                         curses.COLOR_YELLOW)

        curses.init_pair(self.COLOR_PATH,
                         curses.COLOR_WHITE,
                         curses.COLOR_BLUE)

        curses.init_pair(self.COLOR_ENTRY,
                         curses.COLOR_WHITE,
                         curses.COLOR_MAGENTA)

        curses.init_pair(self.COLOR_EXIT,
                         curses.COLOR_WHITE,
                         curses.COLOR_RED)

        curses.init_pair(self.COLOR_WALL_1, curses.COLOR_WHITE, -1)
        curses.init_pair(self.COLOR_WALL_2, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_WALL_3, curses.COLOR_CYAN, -1)

        while True:
            self.draw_ui(stdscr)
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            elif key in (ord('h'), ord('H')):
                self.show_path = not self.show_path
            elif key in (ord('r'), ord('R')):
                self.maze.generate()
                pass
            elif key in (ord('c'), ord('C')):
                # Cycle through the wall IDs (3, 4, and 5)
                self.color_idx = (3 if self.color_idx == 5
                                  else self.color_idx + 1)

    def show(self) -> None:
        """Starts the curses application safely using the standard wrapper.

        Ensures the terminal is properly initialized and restored to its
        original state upon exit or failure.
        """
        curses.wrapper(self._interactive_loop)
