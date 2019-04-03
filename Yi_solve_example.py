from Lazor_Solver import lazor_board_reader
from Yi_block import Block
from Yi_block import update_laser

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
        len_x, len_y = len(board), len(board[0])
        if (pos[0] == 0 or pos[0] == len_x - 1 or pos[1] == 0 or pos[1] == len_y - 1):
            return False
        return True

    # solve for the laser path
    success = False

    while not success:

        target_remain = targetPos[:]
        i = 0
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
                try:
                    if (positions[0] in target_remain):
                        target_remain.remove(positions[0])
                except IndexError:
                    pass
            # Check whether this block assignment has failed by checking
            # whether all lasers have reached boundaries
            if not (len(lasers[-1]) == 0):
                laser_alive += 1

        if (len(target_remain) == 0):
            success = True
            print('Solution found!')
            break

        # break the while loop if failed
        if (laser_alive == 0):
            break
