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

from utils.tools import (tostr, 
                         getpcs,
                         getindex, 
                         changedynamic, 
                         transpose, 
                         transpose_m)

from core.generate import Generate
from core.constants import NOTES


#------------------------------------------------#


# start timer
start_time = time.time()

# transpose a melody by n semi-tones
create = Generate()
m = create.newMelody()
print("\noriginal notes:", m.notes)
dist = randint(1, 11)
print("\ntransposing", dist, "semi-tones...")
m.notes = transpose_m(m.notes, dist)
print("\ntransposed notes:", m.notes)

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