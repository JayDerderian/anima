'''
This module handles mapping functions when converting raw data to index numbers,
which will be used to map against newNotes()'s generated source scale in newMelody()
'''

from core.constants import ALPHABET

# Converts an array of floats to an array of ints
def float_to_int(data):
    '''
    Converts an array of floats to an array of ints
    '''
    result = []
    for i in range(len(data)):
        result.append(int(data[i]))
    return result


# Scale individual data set integers such that i = i < len(dataSet) - 1
def scale_the_scale(data):
    '''
    Returns inputted list[int] with any ints i > len(data) 1 altered to 
    adhere to this limit. This will keep the newly inputted data array's 
    values within the bounds of the scale array. These values function 
    as a collection of index numbers to sequentially map to a new source
    scale to generate melodic ideas.
 
    '''
    for i in range(len(data)):
        if data[i] > len(data)-1:
            data[i] %= len(data)-1
    return data


# Maps letters to index numbers
def letters_to_numbers(letters):
    '''
    Takes a string of any length as an argument, 
    then maps the letters to index numbers, which will then be 
    translated into notes (strings). Accounts for number chars 
    as well
    '''
    # convert inputted str to list of str's
    letters = list(letters)
    numbers = []
    for i in range(len(letters)):
        # make all uppercase characters lowercase
        if letters[i].isupper() == True:
            letters[i] = letters[i].lower()
        if letters[i] in ALPHABET:
            numbers.append(ALPHABET.index(letters[i]))
        # is this str a str of an int???
        elif letters[i].isnumeric():
            # convert to int, keep within bounds of len(letters)-1,
            # then add to list.
            num = int(letters[i])
            if num > len(ALPHABET)-1:
                num %= len(ALPHABET)-1
            numbers.append(num)
    return numbers


# Convert a hex number representing a color to an array of integers
def hex_to_int_list(hex):
    '''
    Converts a prefixed hex number to an array of integers.
    '''
    # convert to int
    hexint = int(hex, 0)
    # then convert to list of ints (ie. 132 -> [1, 3, 2])
    # hexlist = [int(x) for x in str(hexint)]
    return [int(x) for x in str(hexint)]


# Call appropriate mapping method and return modified data
def map_data(mel, data, dt):
    '''
    Wrapper method to map data used by newMelody()
    
    Returns modified data and modified melody() object, or -1 
    on failure. melody() object has original source data saved.
    '''
    # If ints, scale as necessary
    if dt == 1:
        # Save original source data
        mel.source_data = data
        data = scale_the_scale(data)

    # If floats then convert to ints and scale
    elif dt == 2:
        # Save original source data
        mel.source_data = data
        data = float_to_int(data)
        data = scale_the_scale(data)

    # If name or other multi-word input then matches letters to their corresponding index numbers.
    elif dt == 3:
        # Save original source data
        mel.source_data = data
        data = letters_to_numbers(data)

    # If hex convert to array of ints and scale
    elif dt == 4:
        # Converts hex number to string, then saves
        # that as the first item of a list. It's silly, I know.
        # Save original source data
        mel.source_data.append(str(data))
        data = hex_to_int_list(data)
    else:
        raise ValueError("dt value out of range! 1-4")
    return data, mel