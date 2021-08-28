'''
Simplified file for testing generative functions.
'''

# Imports
from random import sample
from random import randint
from modes.rando import newRandomComposition
from ensembles.strqtet import newStrQtet
from ensembles.pnoduet import pnoduet
from practice.practice import newArp, newProg, newcanon

from core.generate import Generate

# newRandomComposition()
# newStrQtet()
# pnoduet(instrument=None)
# newArpeggio()
# newProg()
# newcanon()


create = Generate()
for i in range(10):
    new_scale, pcs = create.newScale()
    print("\ntotal:", len(new_scale))
    print(new_scale)
    print(pcs)