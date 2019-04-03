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
    if len(file_grid) == 0:
        grid =[]
    else:
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


if __name__ == '__main__':
    a = lazor_board_reader('mad_1.bff')
    grid = a[0]
    
