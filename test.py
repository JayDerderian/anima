'''
Simplified file for testing generative functions.
'''

# Imports

from core.constants import TEMPOS
import time
from random import randint, choice

from ensembles.rando import newRandomComposition
from ensembles.strqtet import strqtet
from ensembles.strqtet2 import strqtet2
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet

from utils.data import newData, newInts
from utils.mapping import mapData, scaleTheScale

from practice.practice import (newArp, 
                               newProg, 
                               newcanon, 
                               newpalindrome)

from core.generate import Generate
from containers.melody import Melody

#------------------------------------------------#

# start timer
start_time = time.time()

create = Generate()
m = create.newMelody()

d = randint(1,4)
data=newData(d)

print("\noriginal data:", m.sourceData)
print("\ntotal:", len(m.sourceData))
data = mapData(m, data=data, dataType=d)
print("\nresult:", data)

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