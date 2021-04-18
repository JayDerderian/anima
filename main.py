#*******************************************************************************************#
#~~~~~~~~~~This is the main driver program for generating RNG-Based Compositions~~~~~~~~~~~~#
#*******************************************************************************************#

'''
Notes:

    TODO: CREATE TEST PROGRAM FOR ALL GENERATIVE AND DECISION FUNCTIONS.

    This file is mainly for testing functions and stuff right now. 
    Hopelly this is where the bulk of the GUI work will end up. Maybe.

'''


#-----------------------------------------------------------------------------#
#--------------------GENERATIVE FUNCTION TESTING ZONE!!!!!--------------------#
#-----------------------------------------------------------------------------#


# Imports
from create import generate

# Objects
create = generate()

# Testing melody generation
if(create.newMelody() != -1):
    print("\n...Done!\n")

# Testing UI stuff.

print("\n")
	