"""
Generate random source data for generative methods.

Outputs list of n length with one of the following data types: list[int],
list[float], hex str, list[str]
"""

from random import (
    uniform, randint, choice
)
from core.constants import ALPHABET


def new_ints(t=None):
    """Generate a list of 10 - 50 random numbers between 0-500"""
    total = randint(10, 50)
    return [randint(0, 500) for i in range(total)]


def new_floats():
    """ Generate a list of 10 - 50 random floating point numbers between 0 - 200"""
    total = randint(10, 50)
    return [uniform(0.001, 500.001) for i in range(total)]


def new_hex():
    """Generates a random hex color number 0x000000 to 0xFFFFFF"""
    num = randint(0, 16777215)
    hex_num = format(num, 'x')
    hex_num = '0x' + hex_num
    return hex_num


def new_chars():
    """Generate a list of 10 - 50 random upper/lower-case characters"""
    chars = []
    total = randint(10, 50)
    for i in range(total):
        char = choice(ALPHABET)
        # Capitalize?
        if randint(1, 2) == 1:
            char = char.upper()
        chars.append(char)
    return chars

def new_data(data_type):
    """
    Select and generate some random data for input.
    Enter in 1-4 to choose (1 = int list, 2 = float list,
    3 = char list, 4 = 0xXXXXXX hex number)
    """
    # Generate ints
    if data_type == 1:
        return new_ints()
    # Generate floats
    elif data_type == 2:
        return new_floats()
    # Generate chars
    elif data_type == 3:
        return new_chars()
    # Generate a new hex
    elif data_type == 4:
        return new_hex()
    else:
        raise ValueError("must be int between 1 and 4")
