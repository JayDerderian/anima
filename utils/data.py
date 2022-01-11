'''
This module auto-generates random source data for generative methods.

Outputs list of n length with one of the following data types: list[int], 
list[float], hex str, list[str]
'''

# Imports
from random import randint, choice
from random import uniform

from core.constants import ALPHABET

# Generate a list of 10 - 50 random numbers between 0-200
def new_ints(t=None):
    '''List of random integers between 0 and 500'''
    nums = []
    if t == None:
        total = randint(10, 50)
    else: 
        total = t
    for i in range(total):
        nums.append(randint(0, 500))
    return nums

# Generate a list of 10 - 50 random floating point numbers between 0 - 200
def new_floats():
    '''List of floats between 0.001 and 500.001'''
    floats = []
    total = randint(10, 50)
    for i in range(total):
        floats.append(uniform(0.001, 500.001))
    return floats

# Generates a random hex color number 0x000000 to 0xFFFFFF
def new_hex():
    '''Generates a random hex color number 0x000000 to 0xFFFFFF'''
    num = randint(0, 16777215)
    hexNum = format(num, 'x')
    hexNum = '0x' + hexNum
    return hexNum

# Generate a list of 10 - 50 random upper/lower-case characters
def new_chars():
    '''Generates a random list of 10-50 letters/chars'''
    chars = []
    total = randint(10, 50)
    for i in range(total):
        # Pick letter
        char = choice(ALPHABET)
        # Captitalize?
        if randint(1, 2) == 1:
            char = char.upper()
        chars.append(char)
    return chars

# Generate new data
def new_data(dataType):
    '''Select and generate some random data for input.
       Enter in 1-4 to choose (1 = int list, 2 = float list, 
       3 = char list, 4 = 0xXXXXXX hex number)'''
    # Generate ints
    if dataType == 1:
        data = new_ints()
    # Generate floats
    elif dataType == 2:
        data = new_floats()
    # Generate chars
    elif dataType == 3:
        data = new_chars()
    # Generate a new hex
    else:
        data = new_hex()
    return data
