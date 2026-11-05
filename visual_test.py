from typing import cast
from viewer import CursesViewer
from mazegen import MazeGenerator
from mazegen.solver import AStarSolver
from mazegen.square import Square


def create_square(val: int) -> Square:
    square = Square()
    square.set_square(number=val)
    return square


class DummyMaze():
    width = 10
    height = 10
    entry = (1, 1)
    exit = (9, 9)
    # 10 = Est/West, 15 = All close, 0 = all open, 5 = North/Sud
    # n = bool(cell_value & 1)
    # e = bool(cell_value & 2)
    # s = bool(cell_value & 4)
    # w = bool(cell_value & 8)
    grid = [
        [create_square(11), create_square(9), create_square(3),
         create_square(13), create_square(5), create_square(5),
         create_square(5), create_square(5), create_square(1),
         create_square(7)],
        [create_square(12), create_square(6), create_square(12),
         create_square(5), create_square(5), create_square(5),
         create_square(5), create_square(3), create_square(12),
         create_square(3)],
        [create_square(11), create_square(9), create_square(5),
         create_square(1), create_square(3), create_square(9),
         create_square(5), create_square(6), create_square(9),
         create_square(2)],
        [create_square(10), create_square(10), create_square(9),
         create_square(6), create_square(10), create_square(10),
         create_square(9), create_square(5), create_square(6),
         create_square(10)],
        [create_square(8), create_square(6), create_square(10),
         create_square(9), create_square(6), create_square(12),
         create_square(6), create_square(9), create_square(5),
         create_square(6)],
        [create_square(12), create_square(3), create_square(10),
         create_square(12), create_square(3), create_square(13),
         create_square(3), create_square(12), create_square(3),
         create_square(11)],
        [create_square(11), create_square(10), create_square(12),
         create_square(3), create_square(8), create_square(5),
         create_square(4), create_square(7), create_square(10),
            create_square(10)],
        [create_square(10), create_square(12), create_square(3),
         create_square(10), create_square(14), create_square(9),
         create_square(5), create_square(3), create_square(12),
            create_square(2)],
        [create_square(8), create_square(5), create_square(6),
         create_square(12), create_square(3), create_square(12),
         create_square(3), create_square(12), create_square(5),
         create_square(6)],
        [create_square(12), create_square(5), create_square(5),
         create_square(7), create_square(12), create_square(5),
         create_square(4), create_square(5), create_square(5),
         create_square(7)]
    ]

    path_str, shortest_path_coords = AStarSolver.solve(
        grid=grid,
        entry=entry,
        exit_coord=exit,
        width=width,
        height=height,
    )

    def solve(self) -> str:
        return self.path_str


if __name__ == "__main__":
    maze = cast(MazeGenerator, DummyMaze())
    print(f"Rute: {DummyMaze.path_str}")
    print(f"Path len: {len(DummyMaze.shortest_path_coords)}")
    viewer = CursesViewer(maze)
    viewer.show()
