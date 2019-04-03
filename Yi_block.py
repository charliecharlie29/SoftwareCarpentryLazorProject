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
    board = [['','','','','','',''], ['','o','','o','','o',''], ['','','','','','',''], ['','o','','o','','o',''], ['','','','','','',''], ['','a','','o','','o',''], ['','','','','','','']]
    pos = (5, 2)
    dir = (1, -1)
    new_pos = update_laser(board, pos, dir)
    print(new_pos)
