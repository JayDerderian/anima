'''
Simplified file for testing generative functions.
'''


# Imports
from random import randint
from random import uniform
from generate import generate


#-----------------------------------------test data generation------------------------------------------#


# Generate a list of 10 - 50 random numbers between 0-200
def newInts():
    '''List of random integers between 0 and 200'''
    nums = []
    total = randint(10, 50)
    for i in range(total):
        nums.append(randint(0, 200))
    return nums

# Generate a list of 10 - 50 random floating point numbers between 0 - 200
def newFloats():
    '''List of floats between 0.001 and 200.001'''
    floats = []
    total = randint(10, 50)
    for i in range(total):
        floats.append(uniform(0.001, 200.001))
    return floats

# Generates a random hex color number 0x000000 to 0xFFFFFF
def newHex():
    '''Generates a random hex color number 0x000000 to 0xFFFFFF'''
    num = randint(0, 16777215)
    hexNum = format(num, 'x')
    hexNum = '0x' + hexNum
    return hexNum

# Generate a list of 10 - 50 random upper/lower-case characters
def newChars():
    '''Generates a random list of 10-50 letters/chars'''
    chars = []
    total = randint(10, 50)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    for i in range(total):
        # Pick letter
        char = alphabet[randint(0, 25)]
        # Captitalize? 1 = yes, 2 = no
        if(randint(1, 2) == 1):
            char = char.upper()
        chars.append(char)
    return chars

# Generate new data
def newData(dataType):
    '''Select and generate some random data for input.
       Enter in 1-4 to chose (1 = int list, 2 = float list, 
       3 = char list, 4 =  0xXXXXXX hex number)'''
    # Generate ints
    if(dataType == 1):
        print("\ninputting ints...")
        data = newInts()
    # Generate floats
    elif(dataType == 2):
        print("\ninputting floats...")
        data = newFloats()
    # Generate chars
    elif(dataType == 3):
        print("\ninputting letters...")
        data = newChars()
    # Generate a new hex
    else:
        print("\ninputting hex number...")
        data = newHex()
    print("\ntotal elements:", len(data))
    return data

#-------------------------------------------------------------------------------------#
'''Test random stuff here'''

test_scale, method, data = generate().newSourceScale(total=randint(7, 40))

print("\nfinal total:", len(test_scale))
print("\ntest scale:", test_scale)
print("\ngen method:", method)
print("\nmeta-data:", data, "\n")