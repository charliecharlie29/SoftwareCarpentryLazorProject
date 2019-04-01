import time
import random
from PIL import Image


def get_colors():
    '''
    Colors map that the maze will use:
        0 - Black - A wall
        1 - White - A space to travel in the maze
        2 - Green - A valid solution of the maze
        3 - Red - A backtracked position during maze solving
        4 - Blue - Start and Endpoints of the maze

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        'x': (20, 20, 20),
        'A': (255, 255, 255),
        'o': (0, 255, 0),
        'B': (255, 0, 0),
        'C': (100, 100, 100),
    }


def save_maze(maze, name="maze"):
    '''
    This will save a maze object to a file.

    **Parameters**

        maze: *list, int, str*
            A list of lists, holding integers specifying the different aspects
            of the maze:
                0 - Black - A wall
                1 - White - A space to travel in the maze
                2 - Green - A valid solution of the maze
                3 - Red - A backtracked position during maze solving
                4 - Blue - Start and Endpoints of the maze
        blockSize: *int, optional*
            How many pixels each block is comprised of.
        name: *str, optional*
            The name of the maze.png file to save.

    **Returns**

        None
    '''

    blockSize1 = 5
    blockSize2 = 30
    nBlocksx = len(maze)
    nBlocksy = len(maze[0])

    dimx = ((nBlocksx - 1) / 2 * (blockSize1 + blockSize2)) + blockSize1
    dimy = ((nBlocksy - 1) / 2 * (blockSize1 + blockSize2)) + blockSize1
    colors = get_colors()

    # Verify that all values in the maze are valid colors.
    ERR_MSG = "Error, invalid maze value found!"
    assert all([x in colors.keys() for row in maze for x in row]), ERR_MSG
    img = Image.new("RGB", (dimx, dimy), color=0)



    # Parse "maze" into pixels
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
                    img.putpixel((x + i, y + j), colors[maze[jx][jy]])

    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)



if __name__ == '__main__':
    line1 = ['x','x','x','x','x','x','x','x','x']
    line2 = ['x','o','x','A','x','o','x','o','x']
    maze = [line1,line2,line1,line2,line1,line2,line1]
    save_maze(maze)