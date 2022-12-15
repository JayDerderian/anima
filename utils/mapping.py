"""
This module handles mapping functions when converting raw data to index numbers,
which will be used to map against newNotes()'s generated source scale in newMelody()
"""
from containers.melody import Melody
from core.constants import ALPHABET


def float_to_int(data):
    """
    Converts an array of floats to an array of ints
    """
    result = []
    for i in range(len(data)):
        result.append(int(data[i]))
    return result


def scale_the_scale(data):
    """
    Scales individual data set integers such that data[i] <= len(data)-1

    Returns inputted list[int] with any ints i > len(data) 1 altered to
    adhere to this limit. This will keep the newly inputted data array's
    values within the bounds of the scale array. These values function
    as a collection of index numbers to sequentially map to a new source
    scale to generate melodic ideas.

    """
    for i in range(len(data)):
        if data[i] > len(data)-1:
            data[i] %= len(data)-1
    return data


def letters_to_numbers(letters: str) -> list[int]:
    """
    Takes a string of any length as an argument,
    then maps the letters to index numbers, which will then be
    translated into notes (strings). Accounts for number chars
    as well
    """
    # convert inputted str to list of str's
    letters_list = list(letters)
    numbers = []
    for i in range(len(letters_list)):
        # make all uppercase characters lowercase
        if letters_list[i].isupper():
            letters_list[i] = letters_list[i].lower()
        if letters_list[i] in ALPHABET:
            numbers.append(
                ALPHABET.index(letters_list[i])
            )
        # is this str a str of an int???
        elif letters_list[i].isnumeric():
            # convert to int, keep within bounds of len(letters)-1,
            # then add to list.
            num = int(letters[i])
            if num > len(ALPHABET)-1:
                num %= len(ALPHABET)-1
            numbers.append(num)
    return numbers


def hex_to_int_list(hex) -> list[int]:
    """
    Converts a prefixed hex number to an array of integers.
    """
    hex_int = int(hex, 0)
    return [int(x) for x in str(hex_int)]


def map_data(mel: Melody, data, dt: int):
    """
    Wrapper method to map data used by newMelody()

    Returns modified data and modified melody() object, or -1
    on failure. melody() object has original source data saved.
    """
    # Save original source data
    mel.source_data = data
    # If ints, scale as necessary
    if dt == 1:
        data_scaled = scale_the_scale(data)
    # If floats then convert to ints and scale
    elif dt == 2:
        data_scaled = scale_the_scale(
            float_to_int(data)
        )
    # If name or other multi-word input then matches letters to their corresponding index numbers.
    elif dt == 3:
        data_scaled = letters_to_numbers(data)
    # If hex convert to array of ints and scale
    elif dt == 4:
        data_scaled = hex_to_int_list(data)
    else:
        raise ValueError("dt value out of range! 1-4")
    return data_scaled, mel
