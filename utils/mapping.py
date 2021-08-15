'''
This module handles mapping functions when converting raw data to index numbers,
which will be used to map against newNotes()'s generated source scale in newMelody()
'''

# Imports
import core.constants as c

# Converts an array of floats to an array of ints
def floatToInt(self, data):
    '''
    Converts an array of floats to an array of ints
    '''
    result = []
    for i in range(len(data)):
        result.append(int(data[i]))
    return result

# Scale individual data set integers such that i = i < len(dataSet) - 1
def scaleTheScale(data):
    '''
    Returns inputted integer array with any ints i > len(data) - 1 altered to 
    adhere to this limit. This will keep the newly inputted data array's 
    values within the bounds of the scale array. These values function as a 
    collection of index numbers to sequentially map to a new source
    scale to generate melodic ideas. 
    '''
    # scale it
    for i in range(len(data)):
        # Repeat this subtraction until we're under our threshold.
        while data[i] > len(data) - 1:
            data[i] -= 1
            # data[i] = math.floor(data[i] / len(data) - 1)
    return data

# Maps letters to index numbers
def lettersToNumbers(letters):
    '''
    Takes a string of any length as an argument, 
    then maps the letters to index numbers, which will then be 
    translated into notes (strings). Accounts for number chars 
    as well

    Thanks to Eric Dale for getting this method in better shape.
    '''
    # convert inputted str to list of str's
    letters = list(letters)
    # make all uppercase characters lowercase
    for i in range(len(letters) - 1):
        if letters[i].isupper() == True:
            letters[i] = letters[i].lower()
    numbers = []
    for char in letters:
        if char.isnumeric():
            # if it's already a number, add it's *index* since it might be out of range'
            # numbers.append(int(char))
            numbers.append(c.ALPHABET.index(char))
    return numbers

# Convert a hex number representing a color to an array of integers
def hexToIntList(hex):
    '''
    Converts a prefixed hex number to an array of integers.
    '''
    # convert to int
    hexStr = int(hex, 0)
    # convert to array of ints (ie. 132 -> [1, 3, 2])
    hexList = [int(x) for x in str(hexStr)]
    return hexList