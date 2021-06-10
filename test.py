'''
---------------------------------------------------------------------------------------------------------
                                            TESTING SUITE
---------------------------------------------------------------------------------------------------------
'''
# Imports
from random import uniform
from random import randint
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
    result = generate().scaleTheScale(test)
    for i in range(len(result)):
        if(result[i] > limit):
            print("...result out of bounds!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()
    print("ok!")


#----------------------------------------------low-level tests-------------------------------------------#


# test tempo generation
def testNewTempo():
    '''
    tests tempo generation. Ensures return value is a float within an acceptible range.
    '''
    print("\ntesting tempo generation...")
    t = generate().newTempo()
    # type check
    if(type(t) != float):
        print("...tempo generation failed!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # bounds check
    if(t > generate().tempos[len(generate().tempos) - 1] or t < generate().tempos[0]):
        print("...tempo generated out of range!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    print("ok!")

# tests instrument selection
def testNewInstrument():
    '''
    tests instrument selection. also generates a list and checks to make sure
    those instruments are on the original list
    '''
    print("\ntesting instrument selection...")
    # single instrument
    inst = generate().newInstrument()
    # did we get a string back?
    if(type(inst) != str):
        print("...wrong data type returned!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # was this on the list?
    found = False
    for i in range(len(generate().instruments)):
        if(generate().instruments[i] == inst):
            found = True
            break
    if(found == False):
        print("...output not on original instrument list!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # instrument list
    instruments = generate().newInstruments(randint(2, 10))
    # did we get a list back?
    if(type(instruments) != list):
        print("...wrong data type returned!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # is there anything in it?
    if(len(instruments) == 0):
        print("...no instruments in list!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # are the elements strings?
    for i in range(len(instruments)):
        if(type(instruments[i]) != str):
            print("...wrong data type in list!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()
    # and are they in the original list?
    found = False
    for i in range(len(instruments)):
        if(instruments[i] == generate().instruments[i]):
            found = True
            break
    if(found == False):
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

# test single-rhythm generation
def testNewRhythm():
    '''
    tests single-rhythm generation
    '''
    print("\ntesting single-rhythm generation...")
    r = generate().newRhythm()
    # make sure it's the right data type
    if(type(r) != float):
        print("...wrong data type generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # make sure it's one from our list
    found = False
    for i in range(len(generate().rhythms)):
        if(r == generate().rhythms[i]):
            found = True
            break
    if(found == False):
        print("...no rhythm generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()

    print("ok!")

# test single-dynamic generation
def testNewDynamic():    
    '''
    tests single-dynamic generation
    '''
    print("\ntesting single-rhythm generation...")
    d = generate().newDynamic()
    # make sure it's the right data type
    if(type(d) != int):
        print("...wrong data type!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # make sure it's one of the ones we'd want...
    found = False
    for i in range(len(generate().dynamics)):
        if(d == generate().dynamics[i]):
            found = True
            break
    if(found == False):
        print("...no dynamic generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()

    print("ok!") 

# test single-chord generation
def testNewChord():
    '''
    tests chord generation with and without input
    '''
    print("\ntesting single-chord generation...")
    # without input
    c = generate().newChord()
    # did we get all required data?
    if(c.hasData() == False):
        print("...insufficient chord info!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # did we get a list back?
    if(type(c.notes) != list):
        print("...wrong data type generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # is there anything in it?
    if(len(c.notes) == 0):
        print("...no chord object returned!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # is this a list of strings?
    for i in range(len(c.notes)):
        if(type(c.notes[i]) != str):
            print("...wrong data type!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()

    # with input
    tempo = 60.0
    testScale = ["C#4, D#4, E4, F#4, G#4, A4, B4"]
    c = generate().newChord(tempo, testScale)
    # did we get all required data?
    if(c.hasData() == False):
        print("...insufficient chord info!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # did we get a list back?
    if(type(c.notes) != list):
        print("...wrong data type generated!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # is there anything in it?
    if(len(c.notes) == 0):
        print("...no chord object returned!")
        print("***Test failed!***\n")
        print("\nexiting...\n")
        exit()
    # is this a list of strings?
    for i in range(len(c.notes)):
        if(type(c.notes[i]) != str):
            print("...wrong data type!")
            print("***Test failed!***\n")
            print("\nexiting...\n")
            exit()

    print("ok!")

#----------------------------------------------mid-level tests-------------------------------------------#


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
    if(generate().newNotes(t) != -1):
        print("...failed to catch bad data type (single int)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    t = "test string"
    if(generate().newNotes(t) != -1):
        print("...failed to catch bad data type (single string)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    t = ['t','e','s','t']
    if(generate().newNotes(t) != -1):
        print("...failed to catch bad data type (list of strings)!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # with supplied (and converted) data
    s = []
    data = newInts()
    s = generate().newNotes(data)
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
    s = generate().newScale()
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

# test new rhythms list generation
def testNewRhythms():
    '''
    tests rhythms list generation with and without a supplied total
    '''
    print("\ntesting rhythms list generation...")

    # without total
    r = []
    r = generate().newRhythms()
    # did the method fail?
    if(r == -1):
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get a list back?
    if(type(r) != list):
        print("...did not return a list!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get anything?
    elif(len(r) == 0):
        print("...nothing returned!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # is this a list of floats?
    for i in range(len(r)):
        if(type(r[i]) != float):
            msg = "...incorrect type generated! r = "
            msg = "{}{}".format(msg, r[i])
            print(msg)
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()

    # with total
    r = []
    r = generate().newRhythms(randint(2, 20))
    # did the method fail?
    if(r == -1):
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get a list back?
    if(type(r) != list):
        print("...did not return a list!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get anything?
    elif(len(r) == 0):
        print("...nothing returned!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # is this a list of floats?
    # for i in range(len(r)):
    #     if(type(r[i] != float)):
    #         print("...incorrect type generated!")
    #         print("***Test failed!***")
    #         print("\nexiting...\n")
    #         exit()

    print("ok!")

# test new dynamics list generation
def testNewDynamics():
    '''
    tests dynamics list generation with and without a supplied total
    '''
    print("\ntesting dynamics list generation...")
    # without total
    d = []
    d = generate().newDynamics()
    # did the method fail?
    if(d == -1):
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get a list back?
    if(type(d) != list):
        print("...did not return a list!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get anything?
    elif(len(d) == 0):
        print("...nothing returned!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # is this a list of ints and are they in the correct range?
    for i in range(len(d)):
        # right type?
        if(type(d[i]) != int):
            print("...incorrect type generated!")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()
        # in range?
        if(d[i] > 127 or d[i] < 0):
            print("...output out of range! d = {d[i]}")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()

    # with total
    d = []
    d = generate().newDynamics(randint(2, 20))
    # did the method fail?
    if(d == -1):
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # did we get anything?
    elif(len(d) == 0):
        print("...nothing returned!")
        print("***Test failed!***")
        print("\nexiting...\n")
        exit()
    # is this a list of ints and are they in the correct range?
    for i in range(len(d)):
        # right type?
        if(type(d[i]) != int):
            print("...incorrect type generated!")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()
        # in range?
        if(d[i] > 127 or d[i] < 0):
            print("...output out of range! d = {d[i]}")
            print("***Test failed!***")
            print("\nexiting...\n")
            exit()

    print("ok!")


#---------------------------------------------high-level tests-------------------------------------------#




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#----------------------------------------------DRIVER CODE-----------------------------------------------#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


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
    # lets gooooooooo
    print("\n\n~~~~~~~~~~~~~STARTING ALL TESTS~~~~~~~~~~~~~~")
    
    # conversion tests
    print("\n\n****running conversion tests***")
    testFloats()
    testCharToInt()
    testHexToInt()
    testScaleTheScale()

    # low-level tests
    print("\n\n***running low-level tests***")
    testNewTempo()
    testNewInstrument()
    testNewNote()
    testNewRhythm()
    testNewDynamic()
    testNewChord()

    # mid-level tests
    print("\n\n***running mid-level tests***")
    testNewNotes()
    testNewScale()
    testNewRhythms()
    testNewDynamics()

    # high-level tests
    # print("\n\n***running high-level tests***\n")


    # we did it! hooray!
    testsPassed()

# run it 
runAllTests()