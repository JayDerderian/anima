'''
Simplified file for testing generative functions.
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

from utils.tools import getpcs

from core.generate import Generate

#------------------------------------------------#

# start timer
start_time = time.time()

create = Generate()
notes = create.newScale()
print("\nnew notes:", notes[0])
pcs = getpcs(notes[0])
print("\nfinal pcs:", pcs)


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