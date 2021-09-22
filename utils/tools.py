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
        if o == None:
            for i in range(len(pcs)):
                note = "{}{}".format(NOTES[pcs[i]], o)
                scale.append(note)
        elif type(o) == int and o > 1 and o < 6:
            for i in range(len(pcs)):
                note = "{}{}".format(NOTES[pcs[i]], o)
                scale.append(NOTES[pcs[i]])
        else:
            raise ValueError
    return scale


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
def scaletotempo(tempo, rhythms):
    '''
    A rhythm converter function to translate durations in self.rhythms (list)
    or self.rhythm (float) to actual value in seconds for a specified tempo. 
    
    ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

    60/72 = .83 - The result becomes the converter value to multiply all supplied
    durations against to get the new tempo-accurate durations in seconds.

    NOTE: the round() method keeps the results within three decimal places  
    '''
    diff = 60/tempo
    # is this a single float?
    if type(rhythms) == float:
        rhythms *= diff
        rhythms = round(rhythms, 3)
    # or a list of floats?
    elif type(rhythms) == list:
        for i in range(len(rhythms)):
            rhythms[i] *= diff
            rhythms[i] = round(rhythms[i], 3)
    else:
        raise ValueError
    return rhythms    