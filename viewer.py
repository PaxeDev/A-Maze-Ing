import curses
from mazegen import MazeGenerator


class CursesViewer:
    """Handles the interactive terminal visualization of the maze using curses.

    Attributes:
        maze (MazeGenerator): The maze generator containing the grid logic.
        show_path (bool): Flag determining if the solution path is rendered.
        color_idx (int): Current color palette index for rendering walls.
        COLOR_PATTERN (int): Color pair ID for the 42 pattern.
        COLOR_PATH (int): Color pair ID for the shortest path route.
        COLOR_WALL_1 (int): Color pair ID for the primary wall style.
        COLOR_WALL_2 (int): Color pair ID for the secondary wall style.
        COLOR_WALL_3 (int): Color pair ID for the tertiary wall style.
        COLOR_ENTRY (int): Color pair ID for the entry cell background.
        COLOR_EXIT (int): Color pair ID for the exit cell background.
    """
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

    def _get_pillar_char(self, px: int, py: int) -> str:
        """Calculates the precise Unicode character for a wall intersection.

        Inspects the logical walls of the surrounding cells to select the
        correct Unicode box-drawing character.

        Args:
            px (int): The x-coordinate (column) of the pillar.
            py (int): The y-coordinate (row) of the pillar.

        Returns:
            str: A single Unicode character representing the intersection.
        """
        w = self.maze.width
        h = self.maze.height
        grid = self.maze.grid

        up = down = left = right = False

        # Check for a wall going UP from this pillar
        if py > 0:
            if px < w:
                up = bool(grid[py - 1][px] & 8)  # West wall of cell above
            else:
                up = bool(grid[py - 1][px - 1] & 2)  # E.wall cell left-above

        # Check for a wall going DOWN from this pillar
        if py < h:
            if px < w:
                down = bool(grid[py][px] & 8)  # West wall of current cell
            else:
                down = bool(grid[py][px - 1] & 2)  # East wall of cell left

        # Check for a wall going LEFT from this pillar
        if px > 0:
            if py < h:
                left = bool(grid[py][px - 1] & 1)  # North wall of cell left
            else:
                left = bool(grid[py - 1][px - 1] & 4)  # S.wall cell left-above

        # Check for a wall going RIGHT from this pillar
        if px < w:
            if py < h:
                right = bool(grid[py][px] & 1)  # North wall of current cell
            else:
                right = bool(grid[py - 1][px] & 4)  # South wall of cell above

        # Map the 4 boolean directions to an integer index (0-15)
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

        # Draw the expanded maze (scale: 2 rows x 4 columns per cell)
        for y, row in enumerate(self.maze.grid):
            for x, cell_value in enumerate(row):
                sy = y * 2
                sx = x * 3

                # Bitwise operators to decode the walls
                n = bool(cell_value & 1)
                e = bool(cell_value & 2)
                s = bool(cell_value & 4)
                w = bool(cell_value & 8)

                try:
                    # Get the currently selected color for the walls
                    wall_color = curses.color_pair(self.color_idx)

                    # Anchor pillar in the top-left corner
                    stdscr.addstr(sy, sx, self._get_pillar_char(x, y),
                                  wall_color)
                    # North Wall (3 characters wide)
                    if n:
                        stdscr.addstr(sy, sx + 1, "──", wall_color)

                    # West Wall (1 character high)
                    if w:
                        stdscr.addstr(sy + 1, sx, "│", wall_color)

                    # Closure of the outer east edge (only in the last column)
                    if x == self.maze.width - 1:
                        stdscr.addstr(sy, sx + 3,
                                      self._get_pillar_char(x + 1, y),
                                      wall_color)
                        if e:
                            stdscr.addstr(sy + 1, sx + 3, "│", wall_color)

                    # Closing the outer south edge (only in the last row)
                    if y == self.maze.height - 1:
                        stdscr.addstr(sy + 2, sx,
                                      self._get_pillar_char(x, y + 1),
                                      wall_color)
                        if s:
                            stdscr.addstr(sy + 2, sx + 1, "──", wall_color)
                        # Absolute bottom-right corner
                        if x == self.maze.width - 1:
                            stdscr.addstr(sy + 2, sx + 3,
                                          self._get_pillar_char(x + 1, y + 1),
                                          wall_color)
                    is_pattern = (hasattr(self.maze, 'pattern_42')
                                  and (x, y) in self.maze.pattern_42)
                    is_path = (self.show_path and
                               hasattr(self.maze, 'shortest_path_coords')
                               and (x, y) in self.maze.shortest_path_coords)
                    is_entry = ((hasattr(self.maze, 'entry') and
                                 (x, y) == self.maze.entry))
                    is_exit = ((hasattr(self.maze, 'exit') and
                                (x, y) == self.maze.exit))

                    # fill the hollow interior
                    # of the cell (the 3 central spaces)
                    # using a pair of colors
                    # (black text on a gold background)
                    if is_entry:
                        stdscr.addstr(sy + 1, sx + 1, "  ",
                                      curses.color_pair(self.COLOR_ENTRY))
                    elif is_exit:
                        stdscr.addstr(sy + 1, sx + 1, "  ",
                                      curses.color_pair(self.COLOR_EXIT))
                    elif is_pattern:
                        stdscr.addstr(sy + 1, sx + 1, "  ",
                                      curses.color_pair(self.COLOR_PATTERN))
                    elif is_path:
                        stdscr.addstr(sy + 1, sx + 1, "  ",
                                      curses.color_pair(self.COLOR_PATH))
                except curses.error:
                    pass

        # Menu start coordinates
        # Calculate the first available line below the maze
        ui_y = (self.maze.height * 2) + 1
        path_status = 'Yes' if self.show_path else 'No'

        try:
            stdscr.addstr(ui_y, 0, "=== CONTROLS ===", curses.A_BOLD)
            # Line 1: Current status
            stdscr.addstr(ui_y + 1, 0, f"Path visible: {path_status}")

            # Line 2: Controls in horizontal format to save vertical space
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
        # Enable the terminal color engine
        curses.curs_set(0)
        stdscr.nodelay(False)

        # 2. Register color pairs (ID, Foreground, Background)
        # Pattern 42: Black text on a yellow (gold) background
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.COLOR_PATTERN,
                         curses.COLOR_BLACK,
                         curses.COLOR_YELLOW)

        # Solution path: White text on a blue background
        curses.init_pair(self.COLOR_PATH,
                         curses.COLOR_WHITE,
                         curses.COLOR_BLUE)

        # Input: White text on a magenta (pink) background
        curses.init_pair(self.COLOR_ENTRY,
                         curses.COLOR_WHITE,
                         curses.COLOR_MAGENTA)

        # Output: White text on a red background
        curses.init_pair(self.COLOR_EXIT,
                         curses.COLOR_WHITE,
                         curses.COLOR_RED)

        # Rotating wall paddle (C key)
        # White on a transparent background
        curses.init_pair(self.COLOR_WALL_1, curses.COLOR_WHITE, -1)
        # Green Matrix
        curses.init_pair(self.COLOR_WALL_2, curses.COLOR_GREEN, -1)
        # Neon Cyan
        curses.init_pair(self.COLOR_WALL_3, curses.COLOR_CYAN, -1)

        while True:
            self.draw_ui(stdscr)
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            elif key in (ord('h'), ord('H')):
                self.show_path = not self.show_path
            elif key in (ord('r'), ord('R')):
                # self.maze.generate()
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
