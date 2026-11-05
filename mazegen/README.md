# mazegen

mazegen is a small Python package that generates mazes and solves them. It started as part of the A-Maze-ing project, and everything you need is in one class called `MazeGenerator`.

## Installing

You need Python 3.14. Then install the wheel with pip:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

If you want to build the package yourself, run this from the root of the repository:

```bash
uv build --out-dir .
```

No uv? This works too, and puts the files in `dist/`:

```bash
pip install build
python -m build
```

## Basic example

```python
from mazegen.maze_generator import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry_coord=(0, 0),
    exit_coord=(19, 14),
    output_file="maze.txt",
)

maze.generate()
print(maze.solve())
```

`generate()` builds the maze and also writes it to `output_file`, so you don't need a separate save step.

## Custom parameters

These are the arguments you can pass to `MazeGenerator`:

- `width` and `height`: the size of the maze in cells.
- `entry_coord` and `exit_coord`: where the maze starts and ends, as `(x, y)`. `x` counts columns from the left and `y` counts rows from the top, both starting at 0.
- `output_file`: the file the maze gets written to.
- `perfect`: set this to `True` if you want exactly one path between any two cells. It defaults to `False`, which opens up dead ends and gives you a maze with loops.
- `seed`: use the same seed with the same settings and you get the same maze again. If you leave it out, you get a random maze each time.

Here is a perfect maze with a fixed seed:

```python
maze = MazeGenerator(
    width=30,
    height=20,
    entry_coord=(0, 0),
    exit_coord=(29, 19),
    output_file="perfect_maze.txt",
    perfect=True,
    seed=42,
)
maze.generate()
```

Mazes that are at least 10 cells wide and 8 cells tall get a "42" drawn in the middle out of fully closed cells. If your entry or exit lands on one of those cells, `generate()` raises a `ValueError`. Anything smaller than that is generated without the pattern, and you'll see an error message on the console telling you so.

## Accessing the maze

After `generate()` has run, the maze is in `maze.grid`. It's a list of rows, so you reach a cell with `maze.grid[y][x]`. Each cell is a `Square` object.

```python
cell = maze.grid[3][5]  # column 5, row 3

cell.is_wall_up("north")  # True if the north wall is closed
cell.get_info("number")   # all four walls stored as one number
```

The directions are `"north"`, `"east"`, `"south"` and `"west"`. Always use `is_wall_up()` to check for walls. `get_info("north")` looks like it should do the same thing, but it tells you something different.

## Accessing the solution

`solve()` returns the shortest path from the entry to the exit as a string of moves:

```python
path = maze.solve()
print(path)  # something like "EESSWW"
```

Each letter is one step: `N`, `E`, `S` or `W`. It also fills `maze.shortest_path_coords` with the `(x, y)` cells on that path, which is handy if you want to draw it:

```python
for x, y in maze.shortest_path_coords:
    print(x, y)
```

That's a set, so the cells aren't in walking order. Use the string from `solve()` if you need the actual route. If there's no way through, `solve()` returns an empty string.

Call `generate()` before `solve()`, because there's nothing to solve until the grid exists. The solver uses A*, so the path you get is always a shortest one.

## The output file

The format of the file is different from `maze.grid`. Each row of the maze is one line, with one hexadecimal digit per cell. To get the digit, add up the walls that are closed: north is 1, east is 2, south is 4 and west is 8.

After the rows there's an empty line, then the entry, the exit and the path, each on its own line. Here's a small 6 by 4 maze:

```text
bd5153
c53a96
93c6c3
ec5556

0,0
5,3
SEESENNEESWSES
```

The `b` (11) in the top left corner means north, east and west are closed and south is open, which is why the path starts with `S`.

## License

mazegen is released under the MIT license. See `LICENSE.md` for the full text.
