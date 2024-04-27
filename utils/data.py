"""
Generate random source data for generative methods.

Outputs list of n length with one of the following data types: list[int],
list[float], hex str, list[str]
"""

from random import seed, uniform, randint, choice
from core.constants import ALPHABET

seed()


def new_ints() -> list[int]:
    """Generate a list of 10 - 50 random numbers between 0-500"""
    total = randint(10, 50)
    return [randint(0, 500) for i in range(total)]


def new_floats() -> list[float]:
    """Generate a list of 10 - 50 random floating point numbers between 0 - 200"""
    total = randint(10, 50)
    return [uniform(0.001, 500.001) for i in range(total)]


def new_hex() -> str:
    """Generates a random hex color number 0x000000 to 0xFFFFFF as a string"""
    num = randint(0, 16777215)
    hex_num = format(num, "x")
    hex_num = "0x" + hex_num
    return hex_num


def new_chars() -> list[str]:
    """Generate a list of 10 - 50 random upper/lower-case characters"""
    chars = []
    total = randint(10, 50)
    for i in range(total):
        char = choice(ALPHABET)
        # Capitalize?
        if randint(0, 1) == 1:
            char = char.upper()
        chars.append(char)
    return chars


DATA_MAP = {
    "ints": new_ints(),
    "floats": new_floats(),
    "chars": new_chars(),
    "hex_num": new_hex(),
}


def new_data(data_type: str):
    """
    Select and generate some random data for input.

    """
    if data_type not in list(DATA_MAP.keys()):
        raise ValueError(
            f"{data_type} is not a valid data type! "
            f"available data types: {list(DATA_MAP.keys())}"
        )
    return DATA_MAP[data_type]
