'''
a module containing a variety of tools to analyze and manipulate melody() 
objects and chord() lists. these methods will likely be used in other large
classes in the analyze.py and modify.py files.
'''

# imports
from random import randint, shuffle, choice

from core.constants import NOTES, PITCH_CLASSES
from containers.melody import Melody


def tostr(pcs, octave=None, octeq=True):
    '''
    Converts a list of pitch class integers to note name strings, with or without 
    a supplied octave. Works within one octave or beyond one octave. 
    
    Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
    '''
    scale = []
    if octeq==True:
        # ensure oe is enforced in case octeq flag isn't 
        # set to False by mistake
        pcs = oe(pcs)
        if octave==None:
            for i in range(len(pcs)):
                scale.append(PITCH_CLASSES[pcs[i]])     
        elif type(octave)==int and octave > 1 and octave < 6:
            for i in range(len(pcs)):
                note = "{}{}".format(PITCH_CLASSES[pcs[i]], octave)
                scale.append(note)
        else:
            raise ValueError("octave must be within 2-5!")
    else:
        # this only uses pcs, even if an octave is supplied.
        # NOTES has note strings with assigned octaves. 
        for i in range(len(pcs)):
            scale.append(NOTES[pcs[i]])  
    return scale


def getpcs(notes):
    '''
    matches pitch strings to pitch class integers.
    
    returns the corresponding pcs list[int]. list is unsorted, that is,
    it's in the original order of the elements in the submitted notes list'''
    pcs = []
    if type(notes)==str:
        # check if there's an octave int present
        if notes.isalpha()==False:
            note = removeoct(notes)
            pcs.append(PITCH_CLASSES.index(note))
        else:
            pcs.append(PITCH_CLASSES.index(notes))
    elif type(notes)==list:
        for n in range(len(notes)):
            if notes[n].isalpha()==False:
                note = removeoct(notes[n])
                pcs.append(PITCH_CLASSES.index(note))
            else:
                pcs.append(PITCH_CLASSES.index(notes[n]))
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


def getindex(notes):
    '''
    gets the index or list of indicies of a given note or 
    list of notes in NOTES. 
    
    note name str must have an assigned octave between 0-8. 
    
    the returned list[int] should be used by transpose() with 
    octeq set to False. those resulting values should be mapped 
    back against NOTES to get octave-accurate transposed notes'''
    if type(notes)==str:
        return NOTES.index(notes)
    elif type(notes)==list:
        indicies = []
        for n in range(len(notes)):
            indicies.append(NOTES.index(notes[n]))
        return indicies


def getintervals(notes):
    '''
    generates a list of intervals from a given melody.
    total intervals will be len(m.notes)-1.
    
    difference between index values corresponds to distance
    in semi-tones!'''
    intr = []
    ind = getindex(notes)
    for n in range(len(ind)):
        try:
            intr.append(ind[n+1]-ind[n])
        # if this is the last element, then subtract randint(1,3)
        # from it??? i dont think this modifies the last element.
        except IndexError:
            break
    return intr


def ispos(num):
    '''
    helper method to tell if an int is positive or negative. 
    zero counts as positive here because reasons'''
    num = float(num)
    return True if num >= 0 else False


def transpose_m(notes, dist):
    '''
    wrapper to use with melody() objects.
    returns a new note list[str]
    '''
    if type(dist)!= int or dist > 11 or dist < 1:
        raise ValueError("distance must be an int: 1<=n<=11")
    pcs = transpose(getindex(notes), t=dist, octeq=False)
    return tostr(pcs, octeq=False)


def transpose_c(chords, dist):
    '''
    wrapper to use with chord() lists
    '''
    if type(chords)!=list or type(dist)!=int:
        raise TypeError("list must be chord object list, and distance must be an int")
    if type(dist)==int:
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
    for c in range(len(chords)):
        pcs = transpose(getindex(chords[c].notes), t=dist, octeq=False)
        chords[c].notes = tostr(pcs, octeq=False)
    return chords


def transpose(pcs, t, octeq=True):
    '''
    Transpose a pitch class or list of pitch classes (list[int]) 
    using a supplied interval i, or list of intervals i. 

    If octeq is set to False, then resulting values may be greater than
    11. This may work when working with a source scale (since it goes
    from octaves 2-5) as long as the resulting value n is n <= len(source)-1.
    
    Returns a modified pcs (list[int]) or modified pitch class (int).
    '''
    if type(pcs)!=list:
        raise TypeError("pcs must be a list[int]")
    # modify with a single interval across all pitch-classes
    if type(t)==int:
        for note in range(len(pcs)):
            pcs[note] += t
    # modify with a list of intervals across all pitch-classes. 
    # this allows for each pitch-class to be transposed by a unique
    # distance, allowing for rapid variation generation. 
    # it could also be a list of the same repeated value but that 
    # might be less efficient.
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
        raise ValueError("must be single int or list of ints!")
    return pitch


def retrograde(m):
    '''
    reverses the elements in a melody object (notes, rhythms, dynamics)
    returns a duplicated melody() object'''
    retro = m
    retro.notes.reverse()
    retro.dynamics.reverse()
    retro.rhythms.reverse()
    return retro


def invert(notes):
    '''
    inverts a melody. returns a new note list[str]'''
    
    # list of inverted intervals
    inverted = []
    # get list of intervals and invert values
    intr = getintervals(notes)
    for i in range(len(intr)):
        if ispos(intr[i])==True:
            inverted.append(-abs(intr[i]))
        else:
            inverted.append(abs(intr[i]))
    # get index of first note. we don't need them all.
    # add first note index to new melody note list
    mel = []
    mel.append(getindex(notes[0]))
    # build new melody note list off this inverted interval list 
    for i in range(len(intr)):
        mel.append(mel[i]+inverted[i])
    # translate to note name strings and return
    return tostr(mel, octeq=False)


def frag(m):
    '''
    randomly picks a subset of notes, rhythms, and dynamics (all
    from the same position in the melody) from a given melody and 
    returns this subset as a melodic fragment in a new melody() object'''
    frag = Melody()
    # copy other info from supplied melody object to not miss anything 
    # important
    data = m.getMetaData()
    frag.info = data[0]
    frag.pcs = data[1]
    frag.sourceData = data[2]
    frag.sourceScale = data[3]
    frag.tempo = m.tempo
    frag.instrument = m.instrument
    # generate fragment. any subset will necessarily
    # be at least one element less than the original set.
    frag_len = randint(3, len(m.notes)-2)
    # pick starting index and build fragment from here
    strt = randint(0, len(m.notes)-frag_len)
    for stuff in range(frag_len):
        frag.notes.append(m.notes[strt])
        frag.rhythms.append(m.rhythms[strt])
        frag.dynamics.append(m.dynamics[strt])
        strt+=1
    return frag


def mutate(m):
    '''
    randomly permutates the order of notes, rhythms, and dynamics
    in a given melody object. each list is permutated independtly of the
    other, meaning original associations aren't preserved! 

    returns a separate melody() object containing this permutation'''
    mutant = m
    shuffle(mutant.notes)
    shuffle(mutant.rhythms)
    shuffle(mutant.dynamics)
    return mutant


def rotate(notes):
    '''
    moves the first note of a given list of notes
    to the end of the list.
    
    use method in a loop to rotate n times (such that you don't 
    return to the original ordering) to generate a series
    of "modes."

    returns a list[str]'''
    note = notes[0]
    notes.remove(note)
    notes.append(note)
    return notes


def scaletotempo(tempo, rhythms, revert=False):
    '''
    Converts a supplied float or list[float] of rhythmic values to
    actual value in seconds at a given tempo. can also convert back to base
    rhythmic values of revert is set to True.
    
    ex: [base] q = 60, quarterNote = 1 sec, 
        [new tempo] q = 72, quarterNote = 0.8333(...) sec

    60/72 = .83 - The result becomes the converter value to multiply or divide
    all supplied durations against to get the new tempo-accurate durations in seconds.

    NOTE: the round() method keeps the results within three decimal places to help 
          facilitate sheet music generation.  
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


def changedynamics(dyn, diff):
    '''
    makes a single or list of dynamics louder or softer 
    by a specified amount. returns a modified dynamics list[int]'''
    # needs to be an int that's a multiple of 4 and 
    # within the specified range! MIDI velocities start 
    # at 0 and increase by 4 until 127.
    if type(diff)!=int:
        raise TypeError("supplied value not an int!")
    if type(diff)==int and diff % 4 != 0:
        raise ValueError("supplied value not a multiple of four!")
    if type(dyn)==int and dyn > 123:
        raise ValueError("supplied dynamic is too high")
    # main alteration section
    if type(dyn)==int:
        dyn += diff
    elif type(dyn)==list:
        # only modify dynamics that will be within proper
        # MIDI velocity range.
        for d in range(len(dyn)):
            if dyn[d] < 123:
                dyn[d] += diff
            else:
                continue
    return dyn