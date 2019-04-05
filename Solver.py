"""
Katherine Miller
Last edited: 2019.04.04
Lazor Project Grid Solver

This code is the last step of the Lazor Grid Solver Project
It takes the output from the reader.py to construct all possible combinations
of the board, then checks if the board is a solution via the laser() function.
**WORK IN PROGRESS**
"""

from itertools import *
from sympy.utilities.iterables import multiset_permutations
                                                           
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
array_reset = array

#print to make sure it looks okay
for i in array_reset:
        print(i)
print()

#getting the length and width of the array makes indexing easier
length = len(array_reset)
width = len(array_reset[0])


whilecount = 0
forcount = 0



#for each permutation in the shortened list
for permutation in shortened:
        #these counts are just to keep track of what is getting looped when
        print('for ',forcount)
        forcount += 1
        innercount = 0
        
        #first reset the working array back to all 'o's
        workingarray = array_reset
        
        #then loop through the array replacing 'o's with the blocks
        for l in range(length):
                for w in range(width):
                        if workingarray[l][w] == 'o':
                                print('inner ',innercount)
                                innercount += 1
                                
                                workingarray[l][w] = permutation.pop(0)
for i in array:
        print(i)



####NOTES:
####Here the working array isn't resetting.
####What's worse, the original array is somehow getting written over




