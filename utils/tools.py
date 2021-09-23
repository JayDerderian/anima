'''
a module for general note/rhythm/dynamic-related modification
'''

# imports
from core.constants import NOTES


# Converts a list of pitch class integers to note strings (with or without an octave)
def toStr(pcs, o=None, oe=True):
    '''
    Converts a list of pitch class integers to note name strings, with or without 
    a supplied octave. 
    
    Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
    '''
    scale = []
    if oe==True:
        if o==None:
            for i in range(len(pcs)):
                scale.append(NOTES[pcs[i]])
        elif type(o) == int and o > 1 and o < 6:
            for i in range(len(pcs)):
                note = "{}{}".format(NOTES[pcs[i]], o)
                scale.append(note)
        else:
            raise ValueError
    return scale


# matches pitch strings to pitch class integers. 
def getpcs(notes):
    '''
    matches pitch strings to pitch class integers. modifies supplied
    note list!
    
    returns the corresponding pcs list[int]. list is unsorted, that is,
    it's in the original order of the elements in the submitted notes list'''
    
    # parse note list for pcs ints
    pcs = []
    if type(notes) == str:
        print("\nchecking string...")
        # check if there's an octave int present
        if notes.isalpha()==False:
            print("...octave num found!")
            note = removeoct(notes)
        # now check NOTES and return index of note str
        print("\nchecking against NOTES...")
        if note in NOTES:
            pcs = NOTES.index(note)
            print("...found:", pcs)
    elif type(notes) == list:
        # copy the list since we'll have to modify it to check for 
        # octave values and remove them, if found.
        print("\nchecking list...")
        for note in range(len(notes)):
            # check if there's an octave
            if notes[note].isalpha()==False:
                print("...there's numbers here!")
                notes[note] = removeoct(notes[note])
            print("\nchecking againts NOTES...")
            if notes[note] in NOTES:
                pc = NOTES.index(notes[note])
                print("...found:", pc)
                pcs.append(pc)
                # pcs.append(NOTES.index(notes[note]))
    return pcs


# remove octave numbers from singe-note strings
def removeoct(notes):
    # remove from single note and append octave to list
    print("\nremoving octave...")
    # split single note into two or three parts:
    # either name+oct, name+acc+oct, or name+acc
    n = [char for char in notes]
    print("...split note into short list:", n)
    # account if there's an accidental!!!!
    if len(n)==3:
        note = "{}{}".format(n[0], n[1])
        print("...returning", note)
        return note
    # account for a len(n)==2 and an accidental!!!
    elif len(n)==2 and n[1]=="b" or n[1]=="#":
        note = "{}{}".format(n[0], n[1])
        print("...returning", note)
        return note     
    else:
        print("...returning", n[0])
        return n[0]


# Transpose
def transpose(pcs, t, oe=True):
    '''
    Transpose a pitch class or list of pitch classes (list[int]) 
    using a supplied interval i, or list of intervals i. 
    
    Returns a modified pcs (list[int]) or modified pitch class (int),
    depending on input.
    '''
    # modify with a single interval across all pitch-classes
    if type(t) == int:
        for note in range(len(pcs)):
            pcs[note] += t
    # modify with a list of intervals across all pitch-classes. 
    # this allows for each pitch-class to be transposed by a unique
    # distance, allowing for rapid variation generation.
    elif type(t) == list:
        for note in range(len(pcs)):
            pcs[note] += t[note]
    else:
        raise ValueError
    # keep resulting pcs values between 0 and 11, if desired.
    if oe==True:
        pcs = oe(pcs)
    return pcs


# Keeps a single pitch within span of an octave (0 - 11)
def oe(pitch):
    '''
    Octave equivalance. Handles either a single int or list[int].
    Keeps a single pitch class integer within span of an octave (0 - 11). 

    Returns either a modified int or list[int]
    '''
    # check a single pitch
    if type(pitch) == int:
        pitch %= 12
    # check a whole list of pcs integers
    elif type(pitch) == list:
        for i in range(len(pitch)):
            if pitch[i] > 11 or pitch[i] < 0:
                pitch[i] %= 12
    else:
        raise ValueError
    return pitch


# Convert base rhythms to values in a specified tempo
def scaletotempo(tempo, rhythms, revert=False):
    '''
    Converts a supplied float or list[float] of rhythmic values to
    actual value in seconds at a given tempo. can also convert back to base
    rhythmic values of revert is set to True.
    
    ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

    60/72 = .83 - The result becomes the converter value to multiply all supplied
    durations against to get the new tempo-accurate durations in seconds.

    NOTE: the round() method keeps the results within three decimal places  
    '''
    diff = 60/tempo
    # is this a single float?
    if type(rhythms) == float:
        if revert == False:
            rhythms *= diff
        else:
            rhythms /= diff
        rhythms = round(rhythms, 3)
    # or a list of floats?
    elif type(rhythms) == list:
        for i in range(len(rhythms)):
            if revert==False:
                rhythms[i] *= diff
            else:
                rhythms[i] /= diff
            rhythms[i] = round(rhythms[i], 3)
    else:
        raise ValueError
    return rhythms 