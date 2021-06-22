import colors
import grid_square


def load_grid(columns, rows, WIDTH, PAD):
    grid = []

    xnum = columns
    ynum = rows

    for row in range(ynum):
        grid.append([])
        for column in range(xnum):
            x = column
            y = row

            square = grid_square.GridSquare(x,y,WIDTH, PAD)

            # if square.x==0 or square.y==0 or square.x==xnum-1 or square.y==ynum-1:
            #     square.turn_to_wall()
            #     square.border = True
            if square.x==0 or square.y==0 or square.x==xnum-1 or square.y==ynum-1:
                square.turn_to_wall()
                square.border = True

            grid[row].append(square)

    return grid


def clear_grid(grid, columns, rows):
    for column in grid:
        for square in column:
            if square.border == True:
                continue

            square.turn_to_free()

    return grid

