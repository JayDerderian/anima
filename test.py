'''
Simplified file for testing generative functions.
'''

# Imports
import time
from random import randint, choice

from modes.rando import newRandomComposition
from ensembles.strqtet import strqtet
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet
from practice.practice import (newArp, 
                               newProg, 
                               newcanon, 
                               newpalindrome)

from core.generate import Generate

# start timer
start_time = time.time()

# newRandomComposition()
# strqtet()
# pnoduet()
# newArp()
# newProg()
# newcanon()
# mixedqtet()
# newpalindrome()

end_time = time.time()-start_time
print("\nruntime:", end_time, "seconds\n")