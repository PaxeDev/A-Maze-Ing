from mazegen.grid import Grid


if __name__ == "__main__":
    # width = int(input("width? "))
    # height = int(input("height? "))
    grid = Grid(10, 10, (5, 5), (8, 5), True, 85)
    maze = grid.get_maze()
    grid.run_maze()
