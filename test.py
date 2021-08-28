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

# newRandomComposition()
# newStrQtet()
# pnoduet(instrument=None)
# newArpeggio()
# newProg()
# newcanon()


'''
Trying to do a list comprehension version of the loop in newScale()...
'''
total = randint(5, 9)
pcs = []
pcs = sample(range(11), total)
pcs.sort()

print(pcs)