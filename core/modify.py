'''
module for modifying composition() objects and imported MIDI files.

   
TODO:

    Implement a method to repeat an entire section of music and append it to a given MIDI file

    Implement a method to take a given section of music and modify notes and rhythms at random (or
    with specified user input)

    Implement a method to add notes and rhythms to the end of the file. 

Other TODO's:

    basic scale or pitch class set(s) (can also accept arrays, i.e. groups of notes, which can be used as chords)

    order the notes will be played (allows free selection of any order of those notes, sequential or otherwise)

    basic rate at which this order is assessed, again, a list of values which define a 
    rhythm which itself can be further manipulated

    a separate rhythmically defined period of rests

    variable transposition, which can be defined rhythmically

    periodic permutation of things like note order (above), rest order, order of other functions in the program

    rhythmically defined retrograde/inversion functions of note order and other functions in the program

    rhythmic scaling of certain rhythmic functions (i.e. changing the rhythmic values in another function 
    by a certain factor, which can be constant or variably defined rhythmically)

    variable states of expansion (i.e. moving notes further apart from one another, pitch-wise)

    automatically generated chords based on defined pitch scale

    rhythmically defined variable selection of tension for chords in a progression

    ability to transpose a part to a new mode of a defined pitch scale

    variably defined root cycles for chords

    rhythmically controlled assignment of whatever note is being played to any number of instruments 
    (meaning if you want note 1 to be played by instrument 1 and note 2 and 3 to be played by 
    instrument 2 and so forth in that pattern)

'''

from random import(
    randint, 
    shuffle, 
    choice, 
    choices
)

import utils.midi as mid

from utils.tools import (
    tostr, 
    ispos, 
    oe, 
    scaletotempo
)

from containers.melody import Melody
from core.constants import(
    NOTES, 
    RHYTHMS, 
    PITCH_CLASSES, 
    DYNAMICS, 
    RANGE
)

class Modify:
    '''
    a class of modification methods that work with composition objects and
    imported MIDI files.
    '''
    def __init__(self) -> None:
        pass


    def transpose(self, pcs, dist, octeq=True):
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
        if type(dist)==int:
            for note in range(pcsl):
                pcs[note] += dist
        # modify with a list of intervals across all pitch-class integers. 
        # this allows for each pitch-class to be transposed by a unique
        # distance, allowing for rapid variation generation. 
        # it could also be a list of the same repeated value but that 
        # might be less efficient.
        elif type(dist)==list:
            for note in range(pcsl):
                pcs[note] += dist[note]
        else:
            raise TypeError("incorrect input type. must be single int or list of ints!")
        # keep resulting pcs values between 0 and 11 by default.
        if octeq:
            pcs = oe(pcs)
        return pcs


    def transpose_m(self, notes:list[int], dist:int):
        '''
        wrapper to use with melody() objects.
        returns a new note list[str]
        '''
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
        pcs = self.transpose(self.getindex(notes), t=dist, octeq=False)
        return tostr(pcs, octeq=False)


    def transpose_c(self, chords:list, dist:int):
        '''
        wrapper to use with chord() lists
        '''
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
        cl = len(chords)
        for c in range(cl):
            pcs = self.transpose(self.getindex(chords[c].notes), t=dist, octeq=False)
            chords[c].notes = tostr(pcs, octeq=False)
        return chords


    def getintervals(self, notes:list[str]):
        '''
        generates a list of intervals from a given melody.
        total intervals will be len(m.notes)-1.
        
        difference between index values with NOTES corresponds to distance
        in semi-tones!
        '''
        intrvls = []
        ind = self.getindex(notes)
        ind_len = len(ind)
        for n in range(1, ind_len):
            intrvls.append(ind[n]-ind[n-1])
        return intrvls


    def getindex(self, notes):
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
            notelen = len(notes)
            for n in range(notelen):
                indicies.append(NOTES.index(notes[n]))
            return indicies
        else:
            raise TypeError("notes must be a single str or list[str]! type is:", type(notes))


    def retrograde(self, m:Melody):
        '''
        reverses the elements in a melody object (notes, rhythms, dynamics)
        returns a duplicated melody() object
        '''
        retro = m
        retro.notes.reverse()
        retro.dynamics.reverse()
        retro.rhythms.reverse()
        return retro


    def invert(self, notes: list[str]):
        '''
        inverts a melody. returns a new note list[str]
        '''
        inverted = []                            # list of inverted intervals
        intr = self.getintervals(notes)          # get list of intervals and invert values
        il = len(intr)
        for i in range(il):
            if ispos(intr[i]):
                inverted.append(-abs(intr[i]))
            else:
                inverted.append(abs(intr[i]))
        mel = []                                 # get index of first note. we don't need them all.
        mel.append(self.getindex(notes))         # add first note index to new melody note list
        for i in range(il):                      # build new melody note list off this inverted interval list 
            mel.append(mel[i]+inverted[i])
        return tostr(mel, octeq=False)


    def retro_invert(self, m:Melody):
        '''
        applies both the retrograde and inversion operations.
        returns a separate Melody() object to be appended
        to the original, if needed.
        '''
        ret = self.retrograde(m)
        ret.notes = self.invert(ret.notes)
        return ret


    def frag(self, m:Melody):
        '''
        randomly picks a subset of notes, rhythms, and dynamics (all
        from the same position in the melody) from a given melody and 
        returns this subset as a melodic fragment in a new melody() object
        '''
        frag = Melody()
        # copy other info from supplied melody object 
        # to not miss anything important
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


    def mutate(self, m:Melody):
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


    def rotate(self, notes: list[str]):
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


    def changedynamics(self, dyn, diff):
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