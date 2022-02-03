'''
a module containing a variety of tools to analyze and manipulate melody() 
objects and chord() lists. these methods will likely be used in other large
classes in the analyze.py and modify.py files.

TODO: scale_limit()
      copy() should be used to copy melody() or chord() objects

      should also loot into __eq__ dunder method for classes. might 
      not need to make my own copy() method, but we'll see...

'''
from random import randint
from core.constants import NOTES, PITCH_CLASSES


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
            raise ValueError("octave must be within 2-6!")
    else:
        # this only uses pcs, even if an octave is supplied.
        # NOTES has note strings with assigned octaves. 
        # assigning an octave value as an arg is redundant 
        # here since a list of any ints such that 
        # i < len(NOTES) will do.
        for i in range(len(pcs)):
            scale.append(NOTES[pcs[i]])  
    return scale


def normalize_str(name):
    '''
    removes all non-alphanumeric characters from a string and converts
    it to lowercase.
    '''
    return ''.join(ch for ch in name if ch.isalnum()).lower()


def ispos(num):
    '''
    helper method to tell if an int is positive or negative. 
    zero counts as positive here because reasons
    '''
    num = float(num)
    return True if num >= 0 else False


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


def tempo2bpm(tempo):
    '''
    converts a MIDI file tempo to tempo in BPM. 
    can also take a BPM and return a MIDI file tempo

    - 250000 => 240
    - 500000 => 120
    - 1000000 => 60
    '''
    return int(round((60 * 1000000) / tempo))


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