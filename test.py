'''
Simplified file for testing generative functions.
'''

# Imports
from modes.rando import newRandomComposition


#***********************************************************************************************#
#-------------------------------------TEST STUFF HERE-------------------------------------------#
#***********************************************************************************************#

if newRandomComposition() == -1:
    print("\nfurther testing is needed...\n")
else:
    print("\nhooray!")
