'''
Simplified file for testing generative functions.
'''

# Imports
import time
from random import randint

from modes.rando import newRandomComposition

from ensembles.strqtet import newStrQtet
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet
from utils import data
from practice.practice import newArp, newProg, newcanon

from core.generate import Generate


start_time = time.time()

# newRandomComposition()
# newStrQtet()
# pnoduet()
# newArp()
# newProg()
# newcanon()
# mixedqtet()

create = Generate()
notes, info, source = create.newNotes()
print("\nnew notes:", notes)

end_time = time.time()-start_time
print("\nruntime:", end_time, "\n")