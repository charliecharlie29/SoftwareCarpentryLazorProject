from PIL import Image


def get_colors():
    '''
    Modified from the get_colors function that was provided in the Software
    Carpentry maze lab.

    Color map that the grid will use:
        x = no block allowed
        o = blocks allowed
        A = fixed reflect block
        B = fixed opaque block
        C = fixed refract block

    **Returns**

        color_map: *dict, str, tuple*
            A dictionary that will correlate the str key to
            a color.
    '''
    return {
        'x': (20, 20, 20),
        'A': (255, 255, 255),
        'o': (50, 50, 50),
        'B': (0, 0, 0),
        'C': (150, 150, 150),}


def save_grid(grid, name="grid"):
    '''
    This will save a grid object to a file. This function was modified from the save_maze
    fucntion that was provided in the Software Carpentry maze lab.

    **Parameters**

        grid: *list, list, str*
            A list of lists, holding strings specifying the different aspects
            of the grid:
                0 - Black - A wall
                1 - White - A space to travel in the grid
                2 - Green - A valid solution of the grid
                3 - Red - A backtracked position during grid solving
                4 - Blue - Start and Endpoints of the grid
        name: *str, optional*
            The name of the grid.png file to save.

    **Returns**
        None
    '''
    # Define the grid image, blockSize1 is the border areas, and blockSize2
    # is the size of the various blocks.
    blockSize1 = 5
    blockSize2 = 30
    nBlocksx = len(grid)
    nBlocksy = len(grid[0])

    dimx = ((nBlocksx - 1) / 2 * (blockSize1 + blockSize2)) + blockSize1
    dimy = ((nBlocksy - 1) / 2 * (blockSize1 + blockSize2)) + blockSize1
    colors = get_colors()

    # Verify that all values in the grid are valid colors.
    ERR_MSG = "Error, invalid grid value found!"
    assert all([x in colors.keys() for row in grid for x in row]), ERR_MSG
    img = Image.new("RGB", (dimx, dimy), color=0)



    # Parse "grid" into pixels, making the border areas thinner than the main
    # block areas. Then assigning the appropriate colors to those areas.
    for jy in range(nBlocksy):
        for jx in range(nBlocksx):
            if jy % 2 == 0:
                y = (jy / 2) * (blockSize2 + blockSize1)
                yran = blockSize1
                if jx % 2 == 0:
                    x = (jx / 2) * (blockSize2 + blockSize1)
                    xran = blockSize1
                else:
                    x = ((jx + 1) / 2) * (blockSize2 + blockSize1) - blockSize2
                    xran = blockSize2
            else:
                y = ((jy + 1) / 2) * (blockSize2 + blockSize1) - blockSize2
                yran = blockSize2
                if jx % 2 == 0:
                    x = (jx / 2) * (blockSize2 + blockSize1)
                    xran = blockSize1
                else:
                    x = ((jx + 1) / 2) * (blockSize2 + blockSize1) - blockSize2
                    xran = blockSize2
            for i in range(xran):
                for j in range(yran):
                    img.putpixel((x + i, y + j), colors[grid[jx][jy]])

    if not name.endswith(".png"):
        name += "_solution.png"
    img.save("%s" % name)



if __name__ == '__main__':
    grid = list(['x'])
    save_grid(grid)
