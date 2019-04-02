'''
Josh Cole. Reading in the board file (.bff) to extract and compile
all the important information from it.
'''
from PIL import Image

def lazor_board_reader(filename):
    '''
    Reads in a file and that contains:
        comments started with #
        information on blocks required (A,B,C) followed by # of them (ex. A 2)
        information on lazers (intial x)(initial y)(slope x)(slope y) (ex. L 2 7 1 -1)
        required lazer intersection points (ex. P 3 0)
        a Lazor Grid (in the below style)

            GRID START
            grid representation
            GRID STOP

            Where symbols are:
                x = no block allowed
                o = blocks allowed
                A = fixed reflect block
                B = fixed opaque block
                C = fixed refract block
    and builds an array out of that information to represent a list, then compiles
    a list of blocks, a list of lazers, and a list of required intersection points

    **Parameters**
        filename: *str*
            The .bff file that contains all the Lazor information
    
    **Returns**
        grid: *list, list, str*
            A list X of lists Y containting strings. The lists Y contain values for
            the rows in the array and the list X contains each column.
        
        blocks_a_b_c: *list*
            A list of the number of each type of block in the order A, B, and C
        
        lazers: *list, list, tuple, int*
            A list containing lists of 2 sets of tuples that each contain 2 integers
            The first tuple is the lazer's starting (x, y) coordinates
            The second tuple is the lazer's initial direction

        intersects: *list, tuple, int*
            A list of tuples which each have two integers, which are a required
            intersections (x, y) coordinates
    '''

    raw_file = open(filename, 'r').read()
    list_by_line = raw_file.strip().split('\n')

    # Cut out all the comments so you read through less text
    important_text = list()
    for l in list_by_line:
        if not "#" in l:
            important_text.append(l)

    # Select out the section of the file that represents what
    # the grid will look like, and then turn that into an array
    file_grid = list()
    for i in range(0, len(important_text)):
        if important_text[i] == "GRID START":
            for j in range(1, len(important_text)-i):
                if important_text[i + j] == "GRID STOP":
                    break
                file_grid.append(important_text[i + j])
                important_text[i + j] = '@'
            break
    for k in range(len(file_grid)):
        file_grid[k] = list(file_grid[k].strip().split())
    
    # Generate the array version of the grid and write in 
    # specifications from the .bff file
    grid_x_length = 2 * len(file_grid) + 1
    grid_y_length = 2 * len(file_grid[0]) + 1
    grid = [['x' for x in range(grid_x_length)] for y in range(grid_y_length)]

    for i in range(0, len(file_grid)):
        for j in range(0,len(file_grid[0])):
            grid[2 * j + 1][2 * i + 1] = file_grid[i][j]

    # Read out and turn into lists the number of blocks of each type, the lazers
    # and their position and initial slopes, and the intersection points
    blocks_a_b_c = list([0, 0, 0])
    lazers = list()
    intersects = list()
    for l in range(0, len(important_text)):
        important_text[l] = list(important_text[l].split())
        if len(important_text[l]) == 0:
            continue
        elif important_text[l][0] == 'A':
            blocks_a_b_c[0] = int(important_text[l][1])
        elif important_text[l][0] == 'B':
            blocks_a_b_c[1] = int(important_text[l][1])
        elif important_text[l][0] == 'C':
            blocks_a_b_c[2] = int(important_text[l][1])
        elif important_text[l][0] == 'L':
            lazers.append([(int(important_text[l][1]), int(important_text[l][2])), (int(important_text[l][3]),int(important_text[l][4]))])
        elif important_text[l][0] == 'P':
            intersects.append((int(important_text[l][1]), int(important_text[l][2])))

    return grid, blocks_a_b_c, lazers, intersects


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

def lazor_solver(filename):
    '''
    The contains it all part of the code. Using various functions, it takes an input
    .bff file and creates a .png file that shows the solution to the Lazor file.

    **Parameters**
        filename: *str*
            The name of the .bff file to be read in that contains the Lazor board
            to be solved
    **Returns**
        None
    
    '''
    if ".bff" in filename:
        filename = filename.split(".bff")[0]
    a = lazor_board_reader(filename=filename + '.bff')
    save_grid(a[0], name="%s_solution.png" % filename)

if __name__ == '__main__':
    a = lazor_solver('mad_1.bff')
    b = lazor_solver('numbered_6')

