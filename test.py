'''
Simplified file for testing stuff
'''

# Imports
import time
from random import randint, choice

from ensembles.rando import newRandomComposition
from ensembles.strqtet import strqtet
from ensembles.strqtet2 import strqtet2
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet

from practice.practice import (newArp, 
                               newProg, 
                               newcanon, 
                               newpalindrome)

from utils.tools import (getpcs, 
                         changedynamic, 
                         transpose)

from core.generate import Generate


#------------------------------------------------#


# start timer
start_time = time.time()

create = Generate()
scale = create.newScale(octave=randint(3,5))
print("\nnew scale:", scale[0])
print("original pcs:", scale[1])
pcs = getpcs(scale[0])
print("\nretrieved pcs:", pcs)

# newRandomComposition()
# strqtet()
# strqtet2()
# pnoduet()
# newArp()
# newProg()
# newcanon()
# mixedqtet()
# newpalindrome()

end_time = time.time()-start_time
print("\nruntime:", end_time, "seconds\n")