'''
Authors: Kuan-Lin Chen, Josh Cole, Katherine Miller, Yi Li
Project: Lazor app game solver
Due date: 11:59pm Apr 17th, 2019

Contains all code necessary for solving a Lazor puzzle containing reflect, opaque,
and reflect blocks.

**Functions**
    laser_board_reader
        reads .bff file
    pos_chk
        checks if a position is inside the board
    update_laser
        moves the laser one step forward
    laser_runner
        moves the laser through a whole board
    get_colors
        defines the colors for the output .png
    save_grid
        saves a .png of the solution if a solution is found
    *lazors_cheat*
        Goes through all possible solutions for a board until a correct one is found
        *The only function that needs to be called to solve a Lazor puzzle
        All other functions/classes are called by this function.*

**Classes**
    Block
'''
from PIL import Image
from itertools import *
from sympy.utilities.iterables import multiset_permutations
import copy
import os
import time

def laser_board_reader(filename):

    '''
    Reads in a file and that contains the following:
        comments started with #
        information on blocks required (A,B,C) followed by # of them (ex. A 2)
        information on laser's (intial x)(initial y)(slope x)(slope y) (ex. L 2 7 1 -1)
        required laser intersection points (ex. P 3 0)
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

    After reading in builds an array out of that information to represent a list,
    then compiles a list of blocks, a list of lasers, and a list of required
    intersection points

    **Parameters**

        filename: *str*
            The .bff file that contains all the Lazor information

    **Returns**

        grid: *list, list, str*
            A list X of lists Y containting strings. The lists Y contain values for
            the rows in the array and the list X contains each column.

        blocks_a_b_c: *list*
            A list of the number of each type of block in the order A, B, and C

        lasers: *list, list, tuple, int*
            A list containing lists of 2 sets of tuples that each contain 2 integers
            The first tuple is the laser's starting (x, y) coordinates
            The second tuple is the laser's initial direction

        intersects: *list, tuple, int*
            A list of tuples which each have two integers, which are a required
            intersections (x, y) coordinates
    '''
    print("Loading in board...")
    # Read in the file and then parse it:
    try:
        raw_file = open(filename, 'r').read()
    except IOError:
        print("ERROR: No such file exists. Check spelling.")
        exit()

    list_by_line = raw_file.strip().split('\n')

    # Cut out all the comments so you read through less text
    important_text = list()
    for l in list_by_line:
        if not "#" in l:
            important_text.append(l)

    # Select out the section of the file that represents what
    # the grid will look like, and then turn that into an array
    file_grid = list()
    if 'GRID STOP' in important_text:
        for i in range(0, len(important_text)):
            if important_text[i] == "GRID START":
                for j in range(1, len(important_text)-i):
                    if important_text[i + j] == "GRID STOP":
                        break
                    file_grid.append(important_text[i + j])
                    important_text[i + j] = '@'
                break

    # Generate the array version of the grid and write in
    # specifications from the .bff file
    for k in range(len(file_grid)):
        file_grid[k] = list(file_grid[k].strip().split())

    # Error check for if there is not a correctly writen grid in the .bff file,
    # and then if there is, create a generic grid of the correct size
    if len(file_grid) == 0:
        grid =[]
    else:
        grid_x_length = 2 * len(file_grid) + 1
        grid_y_length = 2 * len(file_grid[0]) + 1
        grid = [['x' for x in range(grid_x_length)] for y in range(grid_y_length)]

    # Fill in to the generic grid, the specifications from the .bff file on locked
    # block locations, open spaces, and no block allowed spaces
    for i in range(0, len(file_grid)):
        for j in range(0,len(file_grid[0])):
            grid[2 * j + 1][2 * i + 1] = file_grid[i][j]

    # Read out and turn into lists the number of blocks of each type, the lasers
    # and their position and initial slopes, and the intersection points
    blocks_a_b_c = list([0, 0, 0])
    lasers = list()
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
            lasers.append([(int(important_text[l][1]), int(important_text[l][2])), (int(important_text[l][3]),int(important_text[l][4]))])
        elif important_text[l][0] == 'P':
            intersects.append((int(important_text[l][1]), int(important_text[l][2])))

    # Generates error messages if something isn't contained in the file correctly,
    # and instructs on what proper format should look like.
    if len(grid) == 0:
        print('''ERROR: File contains no board in an appropriate format. Board must be in format:
            GRID START
            row
            row
            ...
            GRID STOP''')
        exit()
    elif blocks_a_b_c == [0, 0, 0]:
        print('''ERROR: File contains no blocks to place. Blocks must be written in as some combination of:
            A #
            B #
            C #''')
        exit()
    elif len(lasers) == 0:
        print('''ERROR: File contains no lasers to run board. Lasers must be written in the form:
            L # # # #''')
        exit()
    elif len(intersects) == 0:
        print('''ERROR: File contains no intersection points for required win condition. Points must be written in the form:
            P # #''')
        exit()
    else:
        print("Board loaded.")
    return grid, blocks_a_b_c, lasers, intersects


def get_colors():
    '''
    Modified from the get_colors function that was provided in the Software
    Carpentry maze lab. This function defines what each block will look like
    when printed into a .png file.

    Color map that the grid will use:
        x = no block allowed
        o = blocks allowed
        A = fixed reflect block
        B = fixed opaque block
        C = fixed refract block

    **Parameters**
        None

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
        'C': (192, 192, 192),}

def save_grid(grid, name="grid"):
    '''
    This will save a grid object to a file as a legible board with blocks as larger
    spaces and the boundaries as thin lines. This function was modified from the
    save_maze function that was provided in the Software Carpentry maze lab.

    **Parameters**

        grid: *list, list, str*
            A list of lists, holding strings specifying the different aspects
            of the grid:
                'o' - Medium Grey - An open space
                'x' - Dark Grey - A space that blocks can't be (includes boundaries)
                'A' - White - A reflect block
                'B' - Black - An opaque block
                'C' - Silver/Light Grey - A refract block

        name: *str, optional*
            The name of the grid.png file to save.

    **Returns**
        None
    '''

    # Define the grid image, blockSize1 is the border areas, and blockSize2
    # is the size of the various blocks.
    blockSize1 = 10
    blockSize2 = 60
    nBlocksx = len(grid)
    nBlocksy = len(grid[0])

    dimx = ((nBlocksx - 1) // 2 * (blockSize1 + blockSize2)) + blockSize1
    dimy = ((nBlocksy - 1) // 2 * (blockSize1 + blockSize2)) + blockSize1
    colors = get_colors()



    # Verify that all values in the grid are valid colors.
    ERR_MSG = "ERROR: invalid grid value found!"
    assert all([x in colors.keys() for row in grid for x in row]), ERR_MSG
    img = Image.new("RGB", (dimx, dimy), color=0)

    # Parse "grid" into pixels, making the border areas thinner than the main
    # block areas. Then assigning the appropriate colors to those areas.
    for jy in range(nBlocksy):
        for jx in range(nBlocksx):

            if jy % 2 == 0:
                y = (jy // 2) * (blockSize2 + blockSize1)
                yran = blockSize1

                if jx % 2 == 0:
                    x = (jx // 2) * (blockSize2 + blockSize1)
                    xran = blockSize1
                else:
                    x = ((jx + 1) // 2) * (blockSize2 + blockSize1) - blockSize2
                    xran = blockSize2

            else:
                y = ((jy + 1) // 2) * (blockSize2 + blockSize1) - blockSize2
                yran = blockSize2

                if jx % 2 == 0:
                    x = (jx // 2) * (blockSize2 + blockSize1)
                    xran = blockSize1
                else:
                    x = ((jx + 1) // 2) * (blockSize2 + blockSize1) - blockSize2
                    xran = blockSize2

            for i in range(xran):
                for j in range(yran):
                    img.putpixel((x + i, y + j), colors[grid[jx][jy]])

    if not name.endswith(".png"):
        name += "_solution.png"
    img.save("%s" % name)
    print("Solution saved in current folder as %s" % name)

class Block:
    '''
    This is an object that defines a block in the grid
    The block can be empty: either 'o' or 'x' or one of three types:

        'A'--reflect
        'B'--opaque
        'C'--refract
    '''
    def __init__(self, block_coordinates, type):
        '''
        This function initilizes the block object

        **Parameters**

            x: *int*
                The x-coordinate of the block on board

            y: *int*
                The y-coordinate of the block on board

            type: *string*
                The type of the block
        '''
        self.coordinates = block_coordinates
        self.type = type.lower()

        #Print error message and quit if invalid type given
        if not (type.lower() in ['o', 'x', 'a', 'b', 'c']):
            print('ERROR: Incorrect type input for block! Must be o, x, A, B, or C')
            exit()

    def laser(self, pos, dir):
        '''
        This function update the new direction of the laser depending on which
        type of block interacts with the laser

        **Parameters**

            self: *object*
                This block object instance

            pos: *tuple of 2 int*
                The coordinates of laser in the grid

            dir: *tuple of 2 int*
                The direction in which laser is currently going
                4 possible directions:
                (1, 1), (1, -1), (-1, 1), (-1, -1)

        **Returns**

            new_dir: *list*
                a list of new directions of the laser after interacting with block
                The list has 0 element is laser is absorbed
                The list has 1 element if laser interacts with a reflect block
                The list has 2 elements if laser interacts with refract block
        '''

        # block is above or below the laser position if x is an odd number
        if (pos[0] % 2 == 1):
            if (self.type == 'a'):
                new_dir = [(dir[0], dir[1] * -1)]
            elif (self.type == 'b'):
                new_dir = []
            else:
                new_dir1 = dir
                new_dir2 = (dir[0], dir[1] * -1)
                new_dir = [new_dir1, new_dir2]

        # block is at the left or right of laser position if x is an even number
        else:
            if (self.type == 'a'):
                new_dir = [(dir[0] * -1, dir[1])]
            elif (self.type == 'b'):
                new_dir = []
            else:
                new_dir1 = dir
                new_dir2 = (dir[0] * -1, dir[1])
                new_dir = [new_dir1, new_dir2]

        return new_dir


def update_laser(board, pos, dirc):
    '''
    If the laser is not currently at the boundary, this function will check
    whether laser interacts with a block and return the new direction of laser

    **Parameters**

        board: *list, list, string*
            A list of list holds all elements on board

        pos: *tuple of 2 int*
            The current position of laser

        dirc: *tuple of 2 int*
            The current direction laser is going

    **Return**
        new_dir: *list*
            a list that hold new directions laser will be going
    '''
    x, y = pos[0], pos[1]
    new_dir = []

    # Check laser position and if it hits a block, then change direction
    # appropriately, otherwise continue on in the same direction

    # Check above and below laser position if x is an odd number
    if (x % 2 == 1):
        if (board[x][y + dirc[1]].lower() == 'a') or \
        (board[x][y + dirc[1]].lower() == 'b') or \
        (board[x][y + dirc[1]].lower() == 'c'):
            block = Block((x, y + dirc[1]), board[x][y + dirc[1]])
            new_dir = block.laser(pos, dirc)
        else:
            new_dir = copy.deepcopy([dirc])


    # Check left and right of laser position if x is an evem number
    else:
        if (board[x + dirc[0]][y].lower() == 'a') or \
        (board[x + dirc[0]][y].lower() == 'b') or \
        (board[x + dirc[0]][y].lower() == 'c'):

            block = Block((x + dirc[0], y), board[x + dirc[0]][y])
            new_dir = block.laser(pos, dirc)
        else:
            new_dir = copy.deepcopy([dirc])

    return new_dir

def pos_chk(board, pos):
    """
    This function checks whether a given laser position is at the boundary of
    the board.

    **Parameters**

        board: *list, list, string*
            contains list of x coordinates, in which list is a list of y coordinates
            containing a string representing the type of block on the board

        pos: *tuple*
            the current (x,y) position of the laser

    **Return**

        *boolean*
            True if not on boundary and False if on boundary
    """

    len_x, len_y = len(board), len(board[0])

    if (pos[0] <= 0 or pos[0] >= len_x - 1 or pos[1] <= 0 or pos[1] >= len_y - 1):
        return False
    else:
        return True

def laser_runner(board, laser_origin, targetPos):
    '''
    Takes a board and runs lasers from given start positions and directions through
    the Lazor board and blocks, tracking each laser's position as it goes and
    checking if all required target positions have been intersected by a laser.

    **Parameters**
        board: *list, list, string*
            contains list of x coordinates, in which list is a list of y coordinates
            containing a string representing the type of block on the board

        laser_origin: *list, list, tuple, int*
            A list containing lists of 2 sets of tuples that each contain 2 integers
            The first tuple is the laser's starting (x, y) coordinates
            The second tuple is the laser's initial direction

        targetPos: **list, tuple, int*
            A list of tuples which each have two integers, which are a required
            intersections (x, y) coordinates

    **Returns**
        *boolean*
            True if not on all positions are interesected by the laser(s)
            and False if not all target positions have been hit
    '''

    MAXITER = 1000
    ITER = 0

    # Initialize the list that stores all laser positions and create a list that
    # holds targets required for the lasers to hit
    laserList = []
    target_remain = copy.deepcopy(targetPos)
    for pos in laser_origin:
        laserList.append([pos])

    # Solving for the laser's pathway through a given board
    success = False

    # Keep iterating the laser until success or all lasers out of boundary or absorbed
    while not success:
        ITER += 1
        for i in range (len(laserList)):

            # Get current position of this laser if the last position in this
            # laser list is not empty. If it is empty, just continue
            if (len(laserList[i][-1]) == 0):
                continue
            pos, dirc = laserList[i][-1][0], laserList[i][-1][1]

            # Check whether the laser is at the boundary of the board.
            # If so, append an empty list to this list in laserList and skip to
            # the next laser
            if (pos_chk(board, pos) == False) and (ITER > 1):
                laserList[i].append([])
                continue

            # move laser one step forward
            next_dir = update_laser(board, pos, dirc)

            # If laser did not interact with a refract block
            if len(next_dir) == 1:
                dirc = next_dir[0]
                pos = tuple(map(sum, zip(pos, dirc)))
                laserList[i].append([pos, dirc])

            # If laser interacted with a refract block and created a new laser
            elif len(next_dir) == 2:
                dir1, dir2 = next_dir[0], next_dir[1]
                pos1 = tuple(map(sum, zip(pos, dir1)))
                pos2 = tuple(map(sum, zip(pos, dir2)))

                # Append new position and direction of the first and second
                # lasers to the their respective laserList (an old and new one)
                # first list in laserList
                laserList[i].append([pos1, dir1])
                laserList.append([[pos2, dir2]])
            else:
                laserList[i].append([])

        # Go throught the current laserList and see whehther all target
        # points are in the laserList
        laser_alive = 0

        # Check whether this block assignment has failed by checking
        # whether all lasers have reached boundaries
        for lasers in laserList:
            if not (len(lasers[-1]) == 0):
                laser_alive += 1

        # break the while loop if lasers cannot go anywhere else or if the
        # max iterations have been reached
        if (laser_alive == 0) or (ITER == MAXITER):
            break

    for lasers in laserList:
        for positions in lasers:

            # Remove targets being hit by lasers from the target_remain list
            try:
                if (positions[0] in target_remain):
                    target_remain.remove(positions[0])
            except IndexError:
                pass

    # Solution is correct (True) if all targets get hit by lasers, otherwise if not
    # all targets are hit then this is not the correct solution (False)
    if (len(target_remain) == 0):
        return True
    else:
        return False

def lazors_cheat(filename):
    """
    Takes a .bff file for a Lazor puzzle (containing only block types reflect,
    opaque, and refract) and solves it. Then creates a .png solution that shows
    where to put each block

    **Parameters**
        filename: *string*
            The .bff file that contains all the Lazor information.
            Can contain .bff or not

    **Returns**
        None
    """

    # filename = raw_input("What is the filename?\n")


    # Checks for if the file name contains '.bff'' or not
    if ".bff" in filename:
        filename = filename.split(".bff")[0]

    # Read the .bff file and extract the information
    information = laser_board_reader(filename=filename + '.bff')
    grid = information[0]
    [A, B, C] = information[1]
    laser_origin = information[2]
    targetPos = information[3]


    # Seting up block locations

    # 1. Pull out block locations from grid
    blockspots = []
    for y in grid:
        for x in y:
            if x is 'o':
                blockspots.append(x)

    # 2. Assign types of block to list of grid locations
    for i in range(A):
        blockspots[i] = 'A'
    for i in range(A,(A+B)):
        blockspots[i] = 'B'
    for i in range((A+B),(A+B+C)):
        blockspots[i] = 'C'

    # 3. Get all permutations of block locations for a given grid and number of each
    # type of block
    permutations = list(multiset_permutations(blockspots))
    length = len(grid); width = len(grid[0])


    # Algorithm for solving: Create a list of all possible combinations of the
    # lists containging possible block positions and run them individually until
    # finding a solution
    print("%i possible solutions." % len(permutations))
    print("Solving...")
    SOLUTION_FOUND = False
    for possibility in permutations:

        # Create a working grid that reads the information of the block location
        # inside each possibility of the permutations by looping through the array
        # replacing 'o's with the blocks
        workinggrid = copy.deepcopy(grid)
        for l in range(length):
            for w in range(width):
                if workinggrid[l][w] == 'o':
                    workinggrid[l][w] = possibility.pop(0)

        if laser_runner(workinggrid,laser_origin,targetPos) == True:
            print("Solution found!")
            save_grid(workinggrid, name="%s_solution.png" % filename)
            SOLUTION_FOUND = True
            break
    if SOLUTION_FOUND == False:
        print('''Solution not found.
        Please double check .bff file is correct''')



if __name__ == "__main__":

    time_start = time.time()
    lazors_cheat("dark_1.bff")
    time_end = time.time()
    print('run time: %f seconds' %(time_end - time_start))
