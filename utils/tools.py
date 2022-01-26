'''
a module containing a variety of tools to analyze and manipulate melody() 
objects and chord() lists. these methods will likely be used in other large
classes in the analyze.py and modify.py files.

TODO: scale_limit()
      copy() should be used to copy melody() or chord() objects

      should also loot into __eq__ dunder method for classes. might 
      not need to make my own copy() method, but we'll see...

'''
from math import floor
from random import randint, shuffle
from core.constants import NOTES, PITCH_CLASSES
from containers.melody import Melody


def allsame(l):
    '''
    returns true if all elements in the list are the same'''
    return True if all(e == l[0] for e in l) else False


def tostr(pcs, octave=None, octeq=True):
    '''
    Converts a list of pitch class integers to note name strings, with or without 
    a supplied octave. Works within one octave or beyond one octave. 
    
    Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
    '''
    scale = []
    if octeq:
        pcs = oe(pcs)
        if octave==None:
            pcsl = len(pcs)
            for i in range(pcsl):
                scale.append(PITCH_CLASSES[pcs[i]])     
        elif type(octave)==int and octave > 1 and octave < 6:
            pcsl = len(pcs)
            for i in range(pcsl):
                note = f"{PITCH_CLASSES[pcs[i]]}{octave}"
                scale.append(note)
        else:
            raise ValueError("octave must be within 2-5!")
    else:
        # this only uses pcs, even if an octave is supplied.
        # NOTES has note strings with assigned octaves. 
        # assigning an octave value as an arg is redundant 
        # here since a list of any ints such that 
        # i < len(NOTES) will do.
        for i in range(len(pcs)):
            scale.append(NOTES[pcs[i]])  
    return scale


def removeoct(anote):
    '''
    removes octave integer from a note name string. 
    shouldn't be called directly.
    '''
    # split single note into two or three parts:
    # either name + oct or name + acc + oct. 
    n = [char for char in anote]
    if len(n)==3:
        return f"{n[0]}{n[1]}"
    elif len(n)==2 and n[1]=="b" or n[1]=="#":
        return f"{n[0]}{n[1]}"     
    else:
        return n[0]


def getpcs(notes):
    '''
    matches pitch strings to pitch class integers.
    
    returns the corresponding pcs list[int]. list is unsorted, that is,
    it's in the original order of the elements in the submitted notes list
    '''
    pcs = []
    if type(notes)==str:
        # check if there's an octave int present
        if notes.isalpha()==False:                
            note = removeoct(notes)
            pcs.append(PITCH_CLASSES.index(note))
        else:
            pcs.append(PITCH_CLASSES.index(notes))
    elif type(notes)==list:
        nl = len(notes)
        for n in range(nl):
            if notes[n].isalpha()==False:
                note = removeoct(notes[n])
                pcs.append(PITCH_CLASSES.index(note))
            else:
                pcs.append(PITCH_CLASSES.index(notes[n]))
    return pcs


def getindex(notes):
    '''
    gets the index or list of indicies of a given note or 
    list of notes in NOTES. 
    
    note name str must have an assigned octave between 0-8. 
    
    the returned list[int] should be used by transpose() with 
    octeq set to False. those resulting values should be mapped 
    back against NOTES to get octave-accurate transposed notes
    '''
    if type(notes)==str:
        return NOTES.index(notes)
    elif type(notes)==list:
        indicies = []
        l = len(notes)
        for n in range(l):
            indicies.append(NOTES.index(notes[n]))
        return indicies
    else:
        raise TypeError("notes must be a single str or list[str]! type is:", type(notes))


def getintervals(notes):
    '''
    generates a list of intervals from a given melody.
    total intervals will be len(m.notes)-1.
    
    difference between index values with NOTES corresponds to distance
    in semi-tones!
    '''
    intrvls = []
    ind = getindex(notes)
    ind_len = len(ind)
    for n in range(1, ind_len):
        intrvls.append(ind[n]-ind[n-1])
    return intrvls


def ispos(num):
    '''
    helper method to tell if an int is positive or negative. 
    zero counts as positive here because reasons
    '''
    num = float(num)
    return True if num >= 0 else False


def transpose_m(notes:list[int], dist:int):
    '''
    wrapper to use with melody() objects.
    returns a new note list[str]
    '''
    if dist > 11 or dist < 1:
        raise ValueError("distance must be an int: 1<=n<=11")
    pcs = transpose(getindex(notes), t=dist, octeq=False)
    return tostr(pcs, octeq=False)


def transpose_c(chords:list, dist:int):
    '''
    wrapper to use with chord() lists
    '''
    if dist > 11 or dist < 1:
        raise ValueError("distance must be an int: 1<=n<=11")
    cl = len(chords)
    for c in range(cl):
        pcs = transpose(getindex(chords[c].notes), t=dist, octeq=False)
        chords[c].notes = tostr(pcs, octeq=False)
    return chords


def transpose(pcs, t, octeq=True):
    '''
    transpose a pitch class (int) or list of pitch classes (list[int]) 
    using a supplied interval t (int), or list of intervals t (list[int]). 

    if octeq is set to False, then resulting values may be greater than
    11. This may work when working with a source scale (since it goes
    from octaves 2-5) as long as the resulting value n is n <= len(source)-1.

    use getindex() prior to calling transpose() when working with various 
    composition objects. indices in NOTES function as int representations
    of notes, provided they're within the range of NOTES.

    returns a modified pcs (list[int]) or modified pitch class (int).
    '''
    if type(pcs)!=list:
        raise TypeError("pcs must be a list[int]! pcs was type:", type(pcs))
    pcsl = len(pcs)
    # modify with a single interval across all pitch-class integers
    if type(t)==int:
        for note in range(pcsl):
            pcs[note] += t
    # modify with a list of intervals across all pitch-class integers. 
    # this allows for each pitch-class to be transposed by a unique
    # distance, allowing for rapid variation generation. 
    # it could also be a list of the same repeated value but that 
    # might be less efficient.
    elif type(t)==list:
        for note in range(pcsl):
            pcs[note] += t[note]
    else:
        raise TypeError("incorrect input type. must be single int or list of ints!")
    # keep resulting pcs values between 0 and 11 by default.
    if octeq:
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
        pl = len(pitch)
        for i in range(pl):
            if pitch[i] > 11 or pitch[i] < 0:
                pitch[i] %= 12
    else:
        raise ValueError("must be single int or list[int], supplied arg is type:", type(pitch))
    return pitch


def retrograde(m:Melody):
    '''
    reverses the elements in a melody object (notes, rhythms, dynamics)
    returns a duplicated melody() object
    '''
    retro = m
    retro.notes.reverse()
    retro.dynamics.reverse()
    retro.rhythms.reverse()
    return retro


def invert(notes: list[str]):
    '''
    inverts a melody. returns a new note list[str]
    '''
    inverted = []                       # list of inverted intervals
    intr = getintervals(notes)          # get list of intervals and invert values
    il = len(intr)
    for i in range(il):
        if ispos(intr[i]):
            inverted.append(-abs(intr[i]))
        else:
            inverted.append(abs(intr[i]))
    mel = []                            # get index of first note. we don't need them all.
    mel.append(getindex(notes))         # add first note index to new melody note list
    for i in range(il):                 # build new melody note list off this inverted interval list 
        mel.append(mel[i]+inverted[i])
    return tostr(mel, octeq=False)


def frag(m:Melody):
    '''
    randomly picks a subset of notes, rhythms, and dynamics (all
    from the same position in the melody) from a given melody and 
    returns this subset as a melodic fragment in a new melody() object'''
    frag = Melody()
    # copy other info from supplied melody object to not miss anything 
    # important
    data = m.get_meta_data()
    frag.info = data[0]
    frag.pcs = data[1]
    frag.source_data = data[2]
    frag.source_scale = data[3]
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


def mutate(m:Melody):
    '''
    randomly permutates the order of notes, rhythms, and dynamics
    in a given melody object. each list is permutated independently of 
    each other, meaning original associations aren't preserved! 

    returns a separate melody() object containing this permutation
    '''
    mutant = m
    shuffle(mutant.notes)
    shuffle(mutant.rhythms)
    shuffle(mutant.dynamics)
    return mutant


def rotate(notes: list[str]):
    '''
    moves the first note of a given list of notes
    to the end of the list.
    
    use method in a loop to rotate n times (such that you don't 
    return to the original ordering) to generate a series
    of "modes."

    returns a list[str]
    '''
    notes.append(notes.pop(0))
    return notes


def scaletotempo(tempo, rhythms, revert=False):
    '''
    Converts a supplied float or list[float] of rhythmic values to
    actual value in seconds at a given tempo. can also convert back to base
    rhythmic values of revert is set to True.

    Returns either a single float or list[float]
    
    ex: [base] q = 60, quarter_note = 1 sec, 
        [new tempo] q = 72, quarter_note = 0.8333(...) sec

    60/72 = .83 - The result becomes the converter value to multiply or divide
    all supplied durations against to get the new tempo-accurate durations in seconds.

    NOTE: the round() method keeps the results within three decimal places to help 
          facilitate sheet music generation.  
    '''
    diff = 60/tempo
    if type(rhythms) == int:
        rhythms = float(rhythms)
    if type(rhythms)==float:
        if revert==False:
            rhythms *= diff
        else:
            rhythms /= diff
        rhythms = round(rhythms, 3)
    elif type(rhythms)==list:
        rl = len(rhythms)
        for i in range(rl):
            if revert==False:
                rhythms[i] *= diff
            else:
                rhythms[i] /= diff
            rhythms[i] = round(rhythms[i], 3)
    else:
        raise TypeError("incorrect input type. must be single float or list of floats!")
    return rhythms


def changedynamics(dyn, diff):
    '''
    makes a single or list of dynamics louder or softer 
    by a specified amount. returns a modified dynamics list[int]
    '''
    # needs to be an int that's a multiple of 4 and 
    # within the specified range! MIDI velocities start 
    # at 0 and increase by 4 until 127.
    if type(diff)!=int:
        raise TypeError("supplied value not an int!")
    else:
        if diff % 4 != 0:
            raise ValueError("supplied value not a multiple of four!")
    # main alteration section
    if type(dyn)==int:
        if dyn > 123:
            raise ValueError("supplied dynamic is too high")
        dyn += diff
    elif type(dyn)==list:
        # only modify dynamics that will be within proper
        # MIDI velocity range.
        dl = len(dyn)
        for d in range(dl):
            if dyn[d] < 123:
                dyn[d] += diff
            else:
                continue
    return dyn


def checkrange(notes:list[str], ran:list[str]):
    '''
    checks for and removes and removes any notes
    not within the range of a given instrument.

    returns a modified note list[str]
    '''
    diff = get_diff(notes, ran)
    if len(diff) > 0:
        difflen = len(diff)
        for note in range(difflen):
            notes.remove(diff[note])
    return notes

def get_diff(notes, ran):
    '''removes notes not in range of a given instrument with a provided range'''
    return [notes for notes in notes + ran if notes not in notes or notes not in ran]

def getrange(notes:list[str]):
    '''
    returns the lowest and highest note in a given set of notes
    in a tuple: (min, max)
    '''
    for note in notes:
        (min, max) = (10000, -1)
        n = NOTES.index(note)
        if n <  int(min):
            min = n
        elif n > int(max):
            max = n
    return (min, max)


def scale_limit(total:int):
    '''
    scales repetition limits according to total notes
    higher total == fewer reps, basically
    '''
    '''
    TODO: look at proportional scaling methods...
    '''
    if 1 <= total <= 10:
        total = randint(1, 3)
    elif 11 <= total <= 100:                        
        total = randint(1, int(total * 0.2))   
    elif 101 <= total <= 300:
        total = randint(1, int(total * 0.075)) 
    elif 301 <= total <= 500:
        total = randint(1, int(total * 0.05)) 
    elif 501 <= total <= 700:
        total = randint(1, int(total * 0.035)) 
    elif 701 <= total <= 1000:
        total = randint(1, int(total * 0.02))
    elif total > 1000:
        total = randint(1, int(total * 0.001)) 
    return total