"""
Katherine Miller
Last edited: 2019.04.02
Lazor Project Grid Solver
"""

from itertools import repeat

###############################
## From Josh: 
[A,B,C] = [3,3,0]

# This is what the grid array looks like.
array = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]

#[[(targetpoint-x,targetpoint-y),(slope,direction)]
## I'm assuming slope, direction means run,rise
laser = [[(4,9),(-1,-1)],[(6,9),(-1,-1)]]

# This is a list of the points that we have to intersect to complete the puzzle
targets = [(2,5),(5,0)]
################################

## Indexing the array: 
##    array[0] = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
##    array[0][0] = 'x'
##    array[y][x]


## Set the target points
## indicated with 't'
for point in targets:
	array[point[1]][point[0]] = 't'

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

    
        ## Push Block Centers
#to prevent an index error, count keeps track of how far we've gone
count = 0
if count < len(blockspots):
        for y in array:
                for x in y:
                        #replace only the block centers in the array
                        if x == 'o':
                                print(x)
                                x = blockspots[count]
                                print(x)
                                count += 1
                                print()
                                # from the print statements we can see that
                                # the blocks are getting assigned properly,
                                # but it is not reassigning to the original
                                # array for some reason

print(array)
    
    

