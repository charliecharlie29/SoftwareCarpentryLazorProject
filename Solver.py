"""
PYTHON 3.7.2

Katherine Miller
Last edited: 2019.04.04
Lazor Project Grid Solver

This code is the last step of the Lazor Grid Solver Project
It takes the output from the reader.py to construct all possible combinations
of the board, then checks if the board is a solution via the laser() function.
**WORK IN PROGRESS**
"""
import copy
from itertools import *
from sympy.utilities.iterables import multiset_permutations
                                                           
###############################
## From reader.py: 
[A,B,C] = [3,3,0]

# This is what the grid array looks like.
array = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
###############


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

#getting the length and width of the array makes indexing easier
length = len(array)
width = len(array[0])


#for each permutation in the shortened list
for p in permutations:
        #these counts are just to keep track of what is getting looped when
        
        workingarray = copy.deepcopy(array)
        #then loop through the array replacing 'o's with the blocks
        for l in range(length):
                for w in range(width):
                        if workingarray[l][w] == 'o':
                                workingarray[l][w] = p.pop(0)
        



