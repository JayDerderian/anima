'''
Simplified file for testing generative functions.
'''

# Imports
import core.constants as c
from core.generate import Generate
from modes.rando import newRandomComposition
from utils.data import newData


#***********************************************************************************************#
#-------------------------------------TEST STUFF HERE-------------------------------------------#
#***********************************************************************************************#

# create = Generate()

# # 12-tone matrix test
# row, pcs = create.newTwelveToneRow()
# print("\n\noriginal row:", pcs)
# # generate a list of 11, non-repeating random intervals
# intervals = sample(c.INTERVALS[1], len(c.INTERVALS[1]))
# print("\ninterval list:", intervals)
# # generate the matrix
# m = create.newMatrix(pcs, intervals)
# # print entire matrix
# print("\nfinal matrix:\n")
# create.printMatrix(m)