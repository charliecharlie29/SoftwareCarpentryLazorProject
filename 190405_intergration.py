from PIL import Image
from itertools import *
from sympy.utilities.iterables import multiset_permutations
import copy

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
    if 'GRID STOP' in important_text:
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
    if len(file_grid) == 0:
        grid =[]
    else:
        grid_x_length = 2 * len(file_grid) + 1
        grid_y_length = 2 * len(file_grid[0]) + 1
        grid = [['x' for x in range(grid_x_length)] for y in range(grid_y_length)]

    for i in range(0, len(file_grid)):
        for j in range(0,len(file_grid[0])):
            grid[2 * j + 1][2 * i + 1] = file_grid[i][j]

    # Read out and turn into lists the number of blocks of each type, the lazers and their position and initial slopes, and the intersection points
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
    if len(grid) == 0:
        print '''ERROR: File contains no board in an appropriate format. Board must be in format:
            GRID START
            row
            row
            ...
            GRID STOP'''
    elif blocks_a_b_c == [0, 0, 0]:
        print '''ERROR: File contains no blocks to place. Blocks must be written in as some combination of:
            A #
            B #
            C #'''
    elif len(lazers) == 0:
        print '''ERROR: File contains no lasers to run board. Lasers must be written in the form:
            L # # # #'''
    elif len(intersects) == 0:
        print '''ERROR: File contains no intersection points for required win condition. Points must be written in the form:
            P # #'''
    return grid, blocks_a_b_c, lazers, intersects

class Block:
    '''
    This is an object that defines a block in the grid
    The block can be empty: either 'o' or 'x'
    Or the block can be one of three types:
        'A'--reflect
        'B'--opaque
        'C'--refract
    '''
    def __init__(self, block_coordinates, type):
        '''
        This function initilizes the block object
        **Parameters**:
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
            print('Incorrect type input for block!')
            exit()

    def laser(self, pos, dir):
        '''
        This function update the new direction of the laser depending on which
        type of block interacts with the laser
        **Parameters**:
        self: *object*
            This block object instance
        pos: *tuple of 2 int*
            The coordinates of laser in the grid
        dir: *tuple of 2 int*
            The direction in which laser is currently going
            4 possible directions:
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        return: *list*
            a list of new directions of the laser after interacting with block
            The list has 0 element is laser is absorbed
            The list has 1 element if laser interacts with a reflect block
            The list has 2 elements if laser interacts with refract block
        '''

        # block is at the top or bottom of laser position if x is an odd number
        if (pos[0] % 2 == 1):
            if (self.type == 'a'):
                new_dir = [(dir[0], dir[1] * -1)]
            elif (self.type == 'b'):
                new_dir = []
            else:
                new_dir1 = dir
                new_dir2 = (dir[0], dir[1] * -1)
                new_dir = [new_dir1, new_dir2]
        # block is at the top or bottom of laser position if x is an odd number
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


'''
        relative_pos: *tuple of 2 int*
            The relative position of block to the laser position
            top: (0, -1)
            down: (0, 1)
            left: (-1, 0)
            right: (1, 0)
'''

def update_laser(board, pos, dir):
    '''
    If the laser is not currently at the boundary, this function will check
    whether laser interacts with a block and return the new direction of laser
    **Parameters**:
    board: *list, list, string*
        A list of list holds all elements on board
    pos: *tuple of 2 int*
        The current position of laser
    dir: *tuple of 2 int*
        The current direction laser is going
    **Return**:
        a list that hold new directions laser will be going
    '''
    x, y = pos[0], pos[1]
    new_dir = []

    # check top and bottom of laser position if x is an odd number
    if (x % 2 == 1):
        if not (board[x][y + dir[1]] == 'o') or (board[x][y + dir[1]] == 'x'):
            block = Block((x, y + dir[1]), board[x][y + dir[1]])
            new_dir = block.laser(pos, dir)
        else:
            new_dir = [dir]
    # check left and right of laser position if x is an odd number
    else:
        if not (board[x + dir[0]][y] == 'o') or (board[x + dir[0]][y] == 'x'):
            block = Block((x + dir[0], y), board[x + dir[0]][y])
            new_dir = block.laser(pos, dir)
        else:
            new_dir = [dir]

    return new_dir

if __name__ == '__main__':

    # Obtain the input info from lazor_board_reader function
    input = lazor_board_reader('mad_1.bff')
    board = input[0]
    blocks = input[1]
    laser_origin = input[2]
    # Initialize the list that stores all laser positions
    laserList = [laser_origin]
    targetPos = input[3]

    # Assume we have the solution of correct board placement
    board[5][1] = 'C'
    board[7][3] = 'A'
    board[1][5] = 'A'

    def pos_chk(board, pos):
    '''
    This function checks whether a given laser position is at the boundary of
    the board.
    **Parameters**
        board: *list, list, string*
            contains list of x coordinates, in which list is a list of y
            coordinates containing a string representing the type of block on
            the board
        pos: *tuple*
            the current (x,y) position of the laser
    **Return**
        *boolean*
            True if not on boundary and False if on boundary
    '''
        len_x, len_y = len(board), len(board[0])
        if (pos[0] == 0 or pos[0] == len_x - 1 or pos[1] == 0 or pos[1] == len_y - 1):
            return False
        return True

    # solve for the laser path
    success = False

    # Keep iterating the laser until success or all lasers out of boundary or
    # absorbed
    while not success:
        # A list that holds targets not hit by lasers yet
        target_remain = targetPos[:]
        for i in range (len(laserList)):
            # Get current position of this laser if the last position in this
            # laser list is not empty
            if (len(laserList[i][-1]) == 0):
                continue
            pos, dir = laserList[i][-1][0], laserList[i][-1][1]

            # Check whether the laser is at the boundary of the board
            # If so, append a empty list to this list in laserList and skip to
            # the next laser
            if not pos_chk(board, pos):
                laserList[i].append([])
                continue

            # move laser one step forward
            next_dir = update_laser(board, pos, dir)

            # If laser did not interact with a refract block
            if len(next_dir) == 1:
                dir = next_dir[0]
                pos = tuple(map(sum, zip(pos, dir)))
                laserList[i].append([pos, dir])
            # If laser interacted with a refract block and created a new laser
            elif len(next_dir) == 2:
                dir1, dir2 = next_dir[0], next_dir[1]
                pos1 = tuple(map(sum, zip(pos, dir1)))
                pos2 = tuple(map(sum, zip(pos, dir2)))
                # Append new position and direction of the first laser to the
                # first list in laserList
                laserList[i].append([pos1, dir1])
                # Append new position and direction of the second laser to a new
                # list in laserList
                laserList.append([[pos2, dir2]])
            else:
                laserList[i].append([])

            ### DEBUG:
            print(laserList)

        # Go throught the current laserList and see whehther all target
        # laser points are in the laserList
        laser_alive = 0
        for lasers in laserList:
            for positions in lasers:
                # Remove targets being hit by lasers in the target_remain
                try:
                    if (positions[0] in target_remain):
                        target_remain.remove(positions[0])
                except IndexError:
                    pass
            # Check whether this block assignment has failed by checking
            # whether all lasers have reached boundaries
            if not (len(lasers[-1]) == 0):
                laser_alive += 1

        # solution is correct if all targets get hit by lasers
        if (len(target_remain) == 0):
            success = True
            print('Solution found!')
            break

        # break the while loop if failed
        if (laser_alive == 0):
            break

###############################
## From reader.py:
[A,B,C] = [3,3,0]

# This is what the grid array looks like.
array = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]

#[[(targetpoint-x,targetpoint-y),(slope,direction)]
## I'm assuming slope, direction means run,rise
laser = [[(4,9),(-1,-1)],[(6,9),(-1,-1)]]

## This is a list of the points that we have to intersect to complete the puzzle
targets = [(2,5),(5,0)]
################################

## Indexing the array:
##    array[0] = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
##    array[0][0] = 'x'
##    array[y][x]


## Set the target points
## indicated with 't'
# for point in targets:
#     array[point[1]][point[0]] = 't'

## Set block locations
## Pull out block centers
blockspots = []
for y in array:
    for x in y:
        if x is 'o':
            blockspots.append(x)

## Assign block centers
for i in range(A):
        blockspots[i] = 'A'
for i in range(A,(A+B)):
        blockspots[i] = 'B'
for i in range((A+B),(A+B+C)):
        blockspots[i] = 'C'

## Get all permutations of block locations
permutations = list(multiset_permutations(blockspots))

#use a shorter list to test
shortened = []
for i in range(3):
        shortened.append(permutations[i])


###THIS PUTS THE BLOCKS IN THE RIGHT SPOT
###IT DOESN'T INCORPERATE PERMUTATIONS
###IT ACTS AS A FAILSAFE IN CASE I MESS IT UP DOWNSTREAM
#### Put blocks back into board
##for l in range(length):
##        for w in range(width):
##                if array[l][w] == 'o':
##                        item = blockspots.pop(0)
##                        array[l][w] = item



#####WORKING VERSION

#make a separate variable so not to mess up original
array_reset = copy.deepcopy(array)

#print to make sure it looks okay
# for i in array_reset:
#         print(i)
# print()

#getting the length and width of the array makes indexing easier
length = len(array_reset)
width = len(array_reset[0])

#for each permutation in the shortened list
for permutation in permutations:
        #these counts are just to keep track of what is getting looped when
        # print('for ',forcount)
        # forcount += 1
        # innercount = 0

        #first reset the working array back to all 'o's
        workingarray = copy.deepcopy(array_reset)

        #then loop through the array replacing 'o's with the blocks
        for l in range(length):
                for w in range(width):
                        if workingarray[l][w] == 'o':
                                # print('inner ',innercount)
                                # innercount += 1
                                workingarray[l][w] = permutation.pop(0)
# for i in array:
#         print(i)
