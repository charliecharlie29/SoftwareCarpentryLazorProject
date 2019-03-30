"""
This is a file for generation of the class of bolcks
With the example of grid boards
o   o   o   o
o   o   o   o
o   o   o   o
o   o   o   o
A 2
C 1
L 2 7 1 -1
P 3 0
P 4 3
P 2 5
P 4 7

"""
# Board and Grid Generation
# board[y][x]
x_of_grid = 4; y_of_grid = 4
board = [[0 for x in range(2*x_of_grid+1)] for y in range(2*y_of_grid+1)]
# grid = [[ for x in range(1,x_of_grid+1)] for y in range(1,y_of_grid+1)]
grid_list = []
for x in range(1,x_of_grid+1):
    for y in range(1,y_of_grid+1):
        grid_list.append((x,y))

# Informations
reflect_block = 2
opaque_block = 0
refract_block = 1
laser_start = (2,7)
laser_path = []
laser_direction = (1, -1)
targets = [(3, 0), (4, 3), (2, 5), (4, 7)]


class Opaque_Block:
    """
    An Opaque Block ends the path of the laser and does not return a new direction of the laser
    """
    def __init__(self,x,y):
        """
        Defines the position of the block on the board

        ** Parameters **
            x = the x position of the block on the grid
            y = the y position of the block on the grid

        ** Returns **
            x_range = a list containing the x positions of the block
            y_range = a list containing the y positions of the block
        """
        self.x_range = [x - 1 , x, x + 1 ]
        self.y_range = [y - 1 , y, y + 1 ]

    def lsr_dir(self,lsr_pos_x,lsr_pos_y,contact_x,contact_y):
        """
        Returns the contacting x and y as an opaque block blocks the laser path

        ** Parameters **
        lsr_pos_x = the x position of the incoming laser
        lsr_pos_y = the y position of the incoming laser
        contact_x = the x position of the contacting point
        contact_y = the y position of the contacting point

        ** Returns **
        contact_x = the x position of the contacting point
        contact_y = the y position of the contacting point
        """
        return (contact_x, contact_y)

class Reflect_Block:
    """
    A Reflect Block reflects the laser and thus returns a new laser direction
    """
    def __init__(self,x,y):
        """
        Defines the position of the block on the board

        ** Parameters **
            x = the x position of the block on the grid
            y = the y position of the block on the grid

        ** Returns **
            x_range = a list containing the x positions of the block
            y_range = a list containing the y positions of the block
        """
        self.x_range = [x - 1 , x, x + 1 ]
        self.y_range = [y - 1 , y, y + 1 ]

    def lsr_dir(self,lsr_pos_x,lsr_pos_y,contact_x,contact_y):
        """
        Returns the a tuple containing the new direction of the laser

        ** Parameters **
        lsr_pos_x = the x position of the incoming laser
        lsr_pos_y = the y position of the incoming laser
        contact_x = the x position of the contacting point
        contact_y = the y position of the contacting point

        ** Returns **
        new_x_dir = the x direction of the reflecting laser
        new_y_dir = the y direction of the reflecting laser
        """
        if contact_x == self.x_range[1]:
            # Means that it's reflecting on the y surface
            new_x_dir = lsr_pos_x - contact_x
            new_y_dir = contact_y - lsr_pos_y
        if contact_y == self.y_range[1]:
            # Means that it's reflecting on the x surface
            new_x_dir = contact_x - lsr_pos_x
            new_y_dir = lsr_pos_y - contact_y
        return (new_x_dir,new_y_dir)

class Refract_Block:
    """
    A Refract Block reflects the laser and enables the laser to penetrate the block thus returns two new direction and a new starting position
    """
    def __init__(self,x,y):
        """
        Defines the position of the block on the board

        ** Parameters **
            x = the x position of the block on the grid
            y = the y position of the block on the grid

        ** Returns **
            x_range = a list containing the x positions of the block
            y_range = a list containing the y positions of the block
        """
        self.x_range = [x - 1 , x, x + 1 ]
        self.y_range = [y - 1 , y, y + 1 ]

    def lsr_dir(self,lsr_pos_x,lsr_pos_y,contact_x,contact_y):
        """
        Returns the a tuple containing the new direction of the laser

        ** Parameters **
        lsr_pos_x = the x position of the incoming laser
        lsr_pos_y = the y position of the incoming laser
        contact_x = the x position of the contacting point
        contact_y = the y position of the contacting point

        ** Returns **
        new_x1_dir = the x direction of the reflecting laser
        new_y1_dir = the y direction of the reflecting laser
        new_x2_dir = the x direction of the penetrating laser
        new_y2_dir = the y direction of the penetrating laser
        new_x2_pos = the x position of the penetrating laser
        new_y2_pos = the y position of the penetrating laser
        """
        if contact_x == self.x_range[1]:
            # Means that it's reflecting on the y surface
            new_x_dir = lsr_pos_x - contact_x
            new_y_dir = contact_y - lsr_pos_y
        if contact_y == self.y_range[1]:
            # Means that it's reflecting on the x surface
            new_x_dir = contact_x - lsr_pos_x
            new_y_dir = lsr_pos_y - contact_y

        lsr_dir_x = contact_x - lsr_pos_x; lsr_dir_y = contact_y - lsr_pos_y
        contact_x += lsr_dir_x; contact_y += lsr_dir_y
        while contact_x != self.x_range[0] or contact_x != self.x_range[1] or contact_y != self.y_range[0] or contact_y != self.y_range[1]:
            contact_x += lsr_dir_x; contact_y += lsr_dir_y
        new_x2_dir = lsr_dir_x; new_y2_dir = lsr_dir_y
        new_x2_pos = contact_x; new_y2_pos = contact_y

        return (new_x1_dir,new_y1_dir,new_x2_dir,new_y2_dir,new_x2_pos,new_y2_pos)

