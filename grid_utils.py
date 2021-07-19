import colors
import grid_square


def load_grid(columns, rows, WIDTH, PAD):
    grid = []

    xnum = columns
    ynum = rows

    # columns is outer array and rows are the nested array
    # grid[2][3] accesses the 2nd column (x-axis) and the 3rd row (y-axis)
    for row in range(ynum):
        grid.append([])
        for column in range(xnum):
            x = column
            y = row

            square = grid_square.GridSquare(x, y, WIDTH, PAD)

            # if it is the outer squares in the grid, turn the squares into "wall" state
            # we are going to be ignoring these squares when doing the path-finding algorithms
            if square.x == 0 or square.y == 0 or square.x == xnum - 1 or square.y == ynum - 1:
                square.turn_to_wall()
                square.border = True

            grid[row].append(square)

    return grid


# ignores walls, start, and end grid squares so you can click another path-finding algorithm and
# keep the same start, end and wall squares to compare the algorithms
def clean_grid(grid):
    for column in grid:
        for square in column:
            if square.border or square.state == "wall" or square.state == "start_pos" or square.state == "end_pos":
                continue

            square.turn_to_free()
            square.is_visited = False
            square.back_trace = False

    return grid


# unlike clean_grid, clear_grid frees every grid square except the walls on the outside of the grid
def clear_grid(grid):
    for column in grid:
        for square in column:
            if square.border:
                continue

            square.turn_to_free()
            square.is_visited = False
            square.back_trace = False

    return grid
