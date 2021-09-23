'''
a module for general note/rhythm/dynamic-related modification
'''

# imports
from core.constants import NOTES


def toStr(pcs, octave=None):
    '''
    Converts a list of pitch class integers to note name strings, with or without 
    a supplied octave. 
    
    Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
    '''
    scale = []
    if octave==None:
        for i in range(len(pcs)):
            scale.append(NOTES[pcs[i]])
    elif type(octave)==int and octave > 1 and octave < 6:
        for i in range(len(pcs)):
            note = "{}{}".format(NOTES[pcs[i]], octave)
            scale.append(note)
    else:
        raise ValueError("octave must be within 2-5!")
    return scale


def getpcs(notes):
    '''
    matches pitch strings to pitch class integers. modifies supplied
    note list!
    
    returns the corresponding pcs list[int]. list is unsorted, that is,
    it's in the original order of the elements in the submitted notes list'''
    pcs = []
    if type(notes)==str:
        # check if there's an octave int present
        if notes.isalpha()==False:
            note = removeoct(notes)
            # now check NOTES and return index of note str
            if note in NOTES:
                pcs.append(NOTES.index(note))
        else:
            if notes in NOTES:
                pcs.append(NOTES.index(notes))
    elif type(notes)==list:
        for note in range(len(notes)):
            # check if there's an octave in present
            if notes[note].isalpha()==False:
                anote = removeoct(notes[note])
            # now check NOTES and return index of note str
            if anote in NOTES:
                pcs.append(NOTES.index(anote))
    return pcs


def removeoct(anote):
    '''
    removes octave integer from a note name string. 
    shouldn't be called directly.'''
    # split single note into two or three parts:
    # either name + oct or name + acc + oct. 
    n = [char for char in anote]
    if len(n)==3:
        note = "{}{}".format(n[0], n[1])
        return note
    elif len(n)==2 and n[1]=="b" or n[1]=="#":
        note = "{}{}".format(n[0], n[1])
        return note     
    else:
        return n[0]


def transpose(pcs, t, octeq=True):
    '''
    Transpose a pitch class or list of pitch classes (list[int]) 
    using a supplied interval i, or list of intervals i. 

    If octeq is set to False, then resulting values may be greater than
    11. This may work when working with a source scale (since it goes
    from octaves 2-5) as long as the resulting value n is n <= len(source)-1.
    
    Returns a modified pcs (list[int]) or modified pitch class (int).
    '''
    # modify with a single interval across all pitch-classes
    if type(t)==int:
        for note in range(len(pcs)):
            pcs[note] += t
    # modify with a list of intervals across all pitch-classes. 
    # this allows for each pitch-class to be transposed by a unique
    # distance, allowing for rapid variation generation. can also
    # be a list of the same repeated value but that might be less
    # efficient.
    elif type(t)==list:
        for note in range(len(pcs)):
            pcs[note] += t[note]
    else:
        raise ValueError("incorrect input type. must be single int or list of ints!")
    # keep resulting pcs values between 0 and 11 by default.
    if octeq==True:
        pcs = oe(pcs)
    return pcs


def oe(pitch):
    '''
    Octave equivalance. Handles either a single int or list[int].
    Keeps a single pitch class integer within span of an octave (0 - 11). 

    Returns either a modified int or list[int]
    '''
    if type(pitch)==int:
        pitch %= 12
    elif type(pitch)==list:
        for i in range(len(pitch)):
            if pitch[i] > 11 or pitch[i] < 0:
                pitch[i] %= 12
    else:
        raise ValueError("incorrect input type. must be single int or list of ints!")
    return pitch


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
    if type(rhythms)==float:
        if revert==False:
            rhythms *= diff
        else:
            rhythms /= diff
        rhythms = round(rhythms, 3)
    elif type(rhythms)==list:
        for i in range(len(rhythms)):
            if revert==False:
                rhythms[i] *= diff
            else:
                rhythms[i] /= diff
            rhythms[i] = round(rhythms[i], 3)
    else:
        raise ValueError("incorrect input type. must be float or list of floats!")
    return rhythms


def changedynamic(dyn, diff):
    '''
    makes a single or list of dynamics louder or softer 
    by a specified amount'''
    # needs to be an int that's a multiple of 4 and 
    # within the specified range! MIDI velocities start 
    # at 0 and increase by 4 until 127.
    if type(diff)!=int:
        raise TypeError("supplied value not an int!")
    elif type(diff)==int and diff % 4 != 0:
        raise ValueError("supplied value not a multiple of four!")
    if type(dyn)==int:
        dyn += diff
    elif type(dyn)==list:
        # only modify dynamics that will be within proper
        # MIDI velocity range
        for d in range(len(dyn)):
            if dyn[d] < 123:
                dyn[d] += diff
            else:
                continue
    return dyn