from typing import cast, Set, Tuple
from mazegen.viewer import CursesViewer
from mazegen.core import BaseMazeGenerator


class DummyConfig:
    HEIGHT = 20
    WIDTH = 25

    ENTRY = (1, 1)
    EXIT = (19, 14)


class DummyMaze:
    config = DummyConfig()
    # 10 = Est/West, 15 = All close, 0 = all open, 5 = North/Sud
    # n = bool(cell_value & 1)
    # e = bool(cell_value & 2)
    # s = bool(cell_value & 4)
    # w = bool(cell_value & 8)
    # grid = [
    #     [13,  5,  5,  5,  5,  5,  5,  3],
    #     [11,  9,  5,  5,  5,  5,  3, 10],
    #     [10, 10,  9,  5,  5,  3, 10, 10],
    #     [10, 10, 10,  9,  3, 10, 10, 10],
    #     [10, 10, 10, 12,  6, 10, 10, 10],
    #     [10, 10, 12,  5,  5,  6, 10, 10],
    #     [10, 12,  5,  5,  5,  5,  6, 10],
    #     [12,  5,  5,  5,  5,  5,  5,  6]
    # ]
    hex_grid = [
            "9139551111555515515395153",
            "ac2a9102829113855692c3a92",
            "814402aac42ac2a9138452a86",
            "a8116aa8552812c0028138683",
            "868696845142a8386846c6942",
            "81294143943a8284529553812",
            "8446943a852c2c4512a95286a",
            "a951292c2f816fffaac296852",
            "8416c2852fc4157f829285452",
            "81453ac56fffafff86aa8153a",
            "84112813913fafd503c2ac102",
            "812a82ac6c2fafffac54692aa",
            "aaaaa8453943c111413956aaa",
            "8682c453c43c3c6c3a82916c2",
            "83ac111451692915286a86956",
            "82c386815416c4292a9685693",
            "829429681141138444294552a",
            "ac69443aa83aa841392c39382",
            "839453a82c46845682812aa82",
            "c44556c6c555455546c446c46"
        ]
    grid = [[int(char, 16) for char in row] for row in hex_grid]

    # pattern_42: Set[Tuple[int, int]] = {
    #     (3, 3), (4, 3), (3, 4), (4, 4)
    # }
    pattern_42: Set[Tuple[int, int]] = {
        (9, 7), (13, 7), (14, 7), (15, 7), (9, 8), (15, 8),
        (9, 9), (10, 9), (11, 9), (13, 9), (14, 9), (15, 9),
        (11, 10), (11, 11), (13, 10), (13, 11), (14, 11), (15, 11)
    }

    # shortest_path_coords: Set[Tuple[int, int]] = {
    #     (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
    #     (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
    #     (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
    #     (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 2)
    # }
    path_str = "ESEENEEESSSEESESSESESSSSEEEEEESES"
    shortest_path_coords: Set[Tuple[int, int]] = {config.ENTRY}
    cx, cy = config.ENTRY
    for move in path_str:
        if move == 'N':
            cy -= 1
        elif move == 'S':
            cy += 1
        elif move == 'E':
            cx += 1
        elif move == 'W':
            cx -= 1
        shortest_path_coords.add((cx, cy))


if __name__ == "__main__":
    maze = cast(BaseMazeGenerator, DummyMaze())
    viewer = CursesViewer(maze)
    viewer.show()
