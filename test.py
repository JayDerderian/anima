'''
Simplified file for testing generative functions.
'''

# Imports
import time
from random import randint, choice

from modes.rando import newRandomComposition
from ensembles.strqtet import newStrQtet
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet
from practice.practice import newArp, newProg, newcanon

from core.generate import Generate

# start timer
start_time = time.time()

# newRandomComposition()
newStrQtet()
# pnoduet()
# newArp()
# newProg()
# newcanon()
# mixedqtet()

end_time = time.time()-start_time
print("\nruntime:", end_time, "seconds\n")