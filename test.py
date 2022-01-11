'''
simplified file for testing generative functions.
'''

# Imports
import time
from datetime import datetime as date

import tqdm # for progress bars...
from random import randint, choice

from ensembles.rando import new_random_composition
from ensembles.strqtet import strqtet
from ensembles.strqtet2 import strqtet2
from ensembles.strqtet3 import strqtet3
from ensembles.pnoduet import pnoduet
from ensembles.mixedqtet import mixedqtet
from ensembles.bloom import bloom
from ensembles.organ import organ

from utils.tools import scaletotempo
from utils.midi import save

from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition
from core.generate import Generate

#------------------------------------------------#

# start timer
start_time = time.time()

# new_random_composition()
# strqtet()     
# strqtet2()
# strqtet3()
# pnoduet()
# newcanon()
# mixedqtet()
# newpalindrome()
# bloom()
# organ()


# print("\nStarting coin toss test...")
# heads = 0
# tails = 0
# for i in tqdm.trange((100000), desc='Coin Flip Progress'):
#     toss = randint(0, 1)
#     if toss == 0:
#         heads += 1
#     else:
#         tails += 1
# print("\nHeads total:", heads)
# print("Tails total:", tails)

end_time = time.time()-start_time
print("\nruntime:", end_time, "seconds\n")