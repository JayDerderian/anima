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
                         transpose)

from core.generate import Generate


#------------------------------------------------#


# start timer
start_time = time.time()

# create = Generate()
# m = create.newMelody()
# print("\noriginal notes:", m.notes)
# indicies = getindex(m.notes)
# dist = randint(1, 11)
# print("\ntransposing", dist, "semi-tones...")
# pcs = transpose(indicies, t=dist, octeq=False)
# m.notes = tostr(pcs, octeq=False)
# print("\ntransposed notes:", m.notes)

pcs = []
total = randint(3, 20)
for i in range(total):
    pcs.append(randint(0, 75))
print("\nrandom non-oe pcs list:", pcs)
notes = tostr(pcs)
print("\nnotes:", notes)

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