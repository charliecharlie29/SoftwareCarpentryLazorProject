'''
This is what my file reader function will return: grid, number of blocks in order A B C, lazers info, intersection info
Note, this is what the returns will look like for the file numbered_6.bff
'''
# This is what the grid array looks like.
[['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', 'o', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
# in non list form it is like this I made the spaces around the center of the blocks 
# x's because how we are writing blocks in we can't have blocks in the intermediate spaces
#
# x  x  x  x  x  x  x
# x  o  x  o  x  o  x
# x  x  x  x  x  x  x
# x  o  x  x  x  x  x
# x  x  x  x  x  x  x
# x  o  x  o  x  o  x
# x  x  x  x  x  x  x
# x  o  x  x  x  o  x
# x  x  x  x  x  x  x
# x  o  x  o  x  o  x
# x  x  x  x  x  x  x

# This is a list of the number of blocks A, B, and C respectively that we have to use
[3, 3, 0]

# This is a list of lists. Each inner list item contains two tuples, one for the
# lazers initial point and the second for the lazers initial travel slope/direction
[[(4, 9), (-1, -1)], [(6, 9), (-1, -1)]]

# This is a list of the points that we have to intersect to complete the puzzle
[(2, 5), (5, 0)]