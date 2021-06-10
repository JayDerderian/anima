'''
---------------------------------------------------------------------------------------------------------
                                            TESTING SUITE
---------------------------------------------------------------------------------------------------------
'''
# Imports
from random import uniform
from random import randint
from generate import generate


#---------------------------test data generation------------------------------#

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


#---------------------------------------------conversion tests-------------------------------------------#

# test float to int
def testFloats():
    '''
    tests float array to int array conversion
    '''
    print("\ntesting float conversion...")
    create = generate()
    result = create.floatToInt(newFloats())
    # see if we got any data at all
    if(len(result) == 0):
        print("...no conversion created!")
        print("***Test failed!***\n")
        exit()
    # check to make sure they're all ints
    for i in range(len(result) - 1):
        if(type(result[i]) != int):
            print("...int conversion failed!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()
    print("ok!")
    
# test str to int list conversion
def testCharToInt():
    '''
    tests char str to int array conversion
    '''
    print("\ntesting string to int list conversion...")
    test = "test input"
    result = generate().mapLettersToNumbers(test)
    # ensure the list isn't empty
    if(len(result) == 0):
        print("...no conversion! test failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # ensure a list of ints was returned
    for i in range(len(result)):
        if(type(result[i]) != int):
            print("...str to int list test failed!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit() 
    print("ok!")

# test hex char (str) to int list conversion
def testHexToInt():
    '''
    tests hex num (in str form) to int array conversion
    '''
    print("\ntesting hext to int array conversion...")
    result = generate().hexToIntArray(newHex())
    # did anything return?
    if(len(result) == 0):
        print("...no conversion created!")
        print("\nexiting...\n")
        exit()
    # is it the correct type?
    for i in range(len(result)):
        if(type(result[i]) != int):
            print("...wrong type created!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()
    print("ok!")

# test scaling method
def testScaleTheScale():
    '''
    tests integer array scaling method
    '''
    print("\ntesting integer array scaling method...")
    test = newInts()
    limit = len(test) - 1
    result = generate.scaleTheScale(test)
    for i in range(len(result)):
        if(result[i] > limit):
            print("...result out of bounds!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()

#----------------------------------------------low-level tests-------------------------------------------#

# test tempo generation
def testNewTempo():
    '''
    tests tempo generation. Ensures return value is a float within an acceptible range.
    '''
    print("\ntesting tempo generation...")
    create = generate()
    t = create.newTempo()
    # type check
    if(type(t) != float):
        print("...tempo generation failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # bounds check
    if(t > create.tempos[38] or t < create.tempos[0]):
        print("...tempo generated out of range!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    print("ok!")

# test single-note generation
def testNewNote():
    '''
    tests single-note generation.
    '''
    print("\ntesting pitch generation...")
    # Create new instance
    create = generate()
    # random note
    p = ''
    p = create.newNote()
    if(p == ''):
        print("...random note test failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # test bounds check
    if(create.newNote(-1, 10) != -1):
        print("...bounds check failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # test specified note
    p = ''
    p = create.newNote(randint(0, 11), randint(2, 5))
    if(p == ''):
        print("...specified note test failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    print("ok!")

# test rhythm generation
def testNewRhythm():
    '''
    tests single-rhythm generation
    '''
    print("\ntesting single-rhythm generation...")
    r = create.newRhythm()
    # make sure it's the right data type
    if(type(r) != float):
        print("...wrong data type!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # make sure it's one of the ones we'd want...
    found = False
    for i in range(len(create.rhythms)):
        if(r == create.rhythms[i]):
            found == True
            break
    if(found == False):
        print("...no rhythm generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()

    print("ok!")

#----------------------------------------------Mid-level tests-------------------------------------------#

# test source-scale generation
def testNewNotes():
    '''
    tests source scale generation. attempts random scale, sends bad data,
    then sends a list of ints
    '''
    print("\ntesting source scale generation...")
    s = []
    # random source scale
    s = generate().newNotes()
    if(len(s) == 0):
        print("...random source scale test failed!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # with bad data
    t = 10
    if(generate.newNotes(t) != -1):
        print("...failed to catch bad data type (single int)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    t = "test string"
    if(generate.newNotes(t) != -1):
        print("...failed to catch bad data type (single string)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    t = ['t','e','s','t']
    if(generate.newNotes(t) != -1):
        print("...failed to catch bad data type (list of strings)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # with supplied (and converted) data
    s = []
    data = newInts()
    s = generate.newNotes(data)
    for i in range(len(s)):
        # make sure it's a list of str's
        if(type(s[i]) != str):
            print("...")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()
    print("ok!")

# test new random scale generation
def testNewScale():
    '''
    tests random scale generation. 
    NOTE: figure out a way to test for dataType value! 
          must be within 0-127 according to mido!
    '''
    print("\ntesting random scale generation...")
    s = []
    s = generate.newScale()
    # did we get anything?
    if(len(s) == 0):
        print("...no scale generated!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # is this a list of strings?
    for i in range(len(s)):
        if(type(s[i]) != str):
            print("...wrong data type generated!")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()
    print("ok!")



#---------------------------------------------High-level tests-------------------------------------------#




#--------------------------------------------------------------------------------------------------------#

# we did it, hooray!
def testsPassed():
    print("                      ")
    print("----------------------")
    print("***ALL TESTS PASSED***")
    print("----------------------")
    print("                      ")

# quick test
def quickTest():
    print("\n***quick test***\n")
    print("\nrandomly picking data type and data, then sending to newComposition()...")
    d = randint(1, 4)
    data = newData(d)
    print("\ninputting:", data)
    # Create new instance
    create = generate()
    result, abc = create.newComposition(data, d)
    if(result != -1):
        print("new piece:", result)
        return result
    else:
        print("ERROR")
        return "ERROR"


# RUN ALL TESTS
def runAllTests():
    print("\n***STARTING ALL TESTS***\n")
    
    # conversion tests
    print("\n****running conversion tests***\n")
    testFloats()
    testCharToInt()
    testHexToInt()
    testScaleTheScale()

    # low-level tests
    print("\n***running low-level tests***\n")
    testNewTempo()
    testNewNote()
    testNewRhythm()

    # mid-level tests
    print("\n***running mid-level tests***\n")
    testNewNotes()
    testNewScale()

    # high-level tests
    print("\n***running high-level tests***\n")


    # we did it! hooray!
    testsPassed()
