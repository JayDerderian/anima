"""
module for modifying composition() objects and imported MIDI files.


TODO:

    Implement a method to repeat an entire section of music and append it to a given MIDI file

    Implement a method to take a given section of music and modify notes and rhythms at random (or
    with specified user input)

    Implement a method to add notes and rhythms to the end of the file.
"""

from random import (
    randint,
    shuffle,
    choice,
    choices
)

import utils.midi as mid

from utils.tools import (
    to_str,
    is_pos,
    oct_equiv,
    scale_to_tempo
)

from containers.melody import Melody
from core.constants import (
    NOTES,
    RHYTHMS,
    PITCH_CLASSES,
    DYNAMICS,
    RANGE
)


class Modify:
    """
    a class of modification methods that work with composition objects and
    imported MIDI files.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def transpose(pcs, dist, oct_eq=True):
        """
        transpose a list of pitch classes (list[int]) using a supplied interval t (int),
        or list of intervals t (list[int]).

        if oct_eq is set to False, then resulting values may be greater than
        11. This may work when working with a source scale (since it goes
        from octaves 2-5) as long as the resulting value n is n <= len(source)-1.

        use Modify.get_index() prior to calling Modify.transpose() when working with various
        composition objects. indices in NOTES function as int representations
        of notes.

        returns a modified pcs (list[int]) or modified pitch class (int).
        """
        pcs_len = len(pcs)
        # modify with a single interval across all pitch-class integers
        if type(dist) == int:
            for note in range(pcs_len):
                pcs[note] += dist
        # modify with a list of intervals across all pitch-class integers. 
        # this allows for each pitch-class to be transposed by a unique
        # distance, allowing for rapid variation generation. 
        # it could also be a list of the same repeated value but that 
        # might be less efficient.
        elif type(dist) == list:
            for note in range(pcs_len):
                pcs[note] += dist[note]
        else:
            raise TypeError("incorrect input type. must be single int or list of ints!")
        # keep resulting pcs values between 0 and 11 by default.
        if oct_eq:
            pcs = oct_equiv(pcs)
        return pcs

    def transpose_m(self, notes: list[int], dist: int):
        """
        wrapper to use with melody() objects.
        returns a new note list[str]
        """
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
        pcs = self.transpose(self.get_index(notes),
                             dist=dist, oct_eq=False)
        return to_str(pcs, oct_eq=False)

    def transpose_c(self, chords: list, dist: int) -> list:
        """
        wrapper to use with chord() lists
        """
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
        cl = len(chords)
        for c in range(cl):
            pcs = self.transpose(self.get_index(chords[c].notes),
                                 dist=dist, oct_eq=False)
            chords[c].notes = to_str(pcs, oct_eq=False)
        return chords

    def get_intervals(self, notes: list[str]) -> list[int]:
        """
        generates a list of intervals from a given melody.
        total intervals will be len(m.notes)-1.

        difference between index values with NOTES corresponds to distance
        in semi-tones!
        """
        intervals = []
        ind = self.get_index(notes)
        ind_len = len(ind)
        for n in range(1, ind_len):
            intervals.append(ind[n] - ind[n-1])
        return intervals

    @staticmethod
    def get_index(notes):
        """
        gets the index or list of indices of a given note or
        list of notes in NOTES.

        note name str must have an assigned octave between 0-8.

        the returned list[int] should be used by transpose() with
        oct_eq set to False. those resulting values should be mapped
        back against NOTES to get octave-accurate transposed notes
        """
        if type(notes) == str:
            return NOTES.index(notes)
        elif type(notes) == list:
            indices = []
            note_len = len(notes)
            for n in range(note_len):
                indices.append(NOTES.index(notes[n]))
            return indices
        else:
            raise TypeError("notes must be a single str or list[str]! type is:", type(notes))

    @staticmethod
    def retrograde(m: Melody) -> Melody:
        """
        reverses the elements in a melody object (notes, rhythms, dynamics)
        returns a duplicated melody() object
        """
        retro = m
        retro.notes.reverse()
        retro.dynamics.reverse()
        retro.rhythms.reverse()
        return retro

    def invert(self, notes: list[str]):
        """
        inverts a melody. returns a new note list[str]
        """
        # list of inverted intervals
        inverted = []
        # get list of intervals and invert values
        intervals = self.get_intervals(notes)
        interval_len = len(intervals)
        for i in range(interval_len):
            if is_pos(intervals[i]):
                inverted.append(-abs(intervals[i]))
            else:
                inverted.append(abs(intervals[i]))
        # get index of first note. we don't need them all.
        mel = []
        mel.append(self.get_index(notes))
        # build new melody note list off this inverted interval list
        for i in range(interval_len):
            mel.append(mel[i] + inverted[i])
        return to_str(mel, oct_eq=False)

    def retro_invert(self, m: Melody) -> Melody:
        """
        applies both the retrograde and inversion operations.
        returns a separate Melody() object to be appended
        to the original, if needed.
        """
        ret = self.retrograde(m)
        ret.notes = self.invert(ret.notes)
        return ret

    @staticmethod
    def frag(m: Melody) -> Melody:
        """
        randomly picks a subset of notes, rhythms, and dynamics (all
        from the same position in the melody) from a given melody and
        returns this subset as a melodic fragment in a new melody() object
        """
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
        frag_len = randint(3, len(m.notes) - 2)
        # pick starting index and build fragment from here
        strt = randint(0, len(m.notes) - frag_len)
        for stuff in range(frag_len):
            frag.notes.append(m.notes[strt])
            frag.rhythms.append(m.rhythms[strt])
            frag.dynamics.append(m.dynamics[strt])
            strt += 1
        return frag

    @staticmethod
    def mutate(m: Melody) -> Melody:
        """
        randomly permutates the order of notes, rhythms, and dynamics
        in a given melody object. each list is permutated independently of
        each other, meaning original associations aren't preserved!

        returns a separate melody() object containing this permutation
        """
        mutant = m
        shuffle(mutant.notes)
        shuffle(mutant.rhythms)
        shuffle(mutant.dynamics)
        return mutant

    @staticmethod
    def rotate(notes: list[str]) -> list[str]:
        """
        moves the first note of a given list of notes
        to the end of the list.

        use method in a loop to rotate n times (such that you don't
        return to the original ordering) to generate a series
        of "modes."

        returns a list[str]
        """
        notes.append(notes.pop(0))
        return notes

    @staticmethod
    def change_dynamics(dyn, diff):
        """
        makes a single or list of dynamics louder or softer
        by a specified amount. returns a modified dynamics list[int]
        """
        # needs to be an int that's a multiple of 4 and 
        # within the specified range! MIDI velocities start 
        # at 0 and increase by 4 until 127.
        if type(diff) != int:
            raise TypeError("supplied value not an int!")
        else:
            if diff % 4 != 0:
                raise ValueError("supplied value not a multiple of four!")
        # main alteration section
        if type(dyn) == int:
            if dyn > 123:
                raise ValueError("supplied dynamic is too high")
            dyn += diff
        elif type(dyn) == list:
            # only modify dynamics that will be within proper
            # MIDI velocity range.
            dl = len(dyn)
            for d in range(dl):
                if dyn[d] < 123:
                    dyn[d] += diff
                else:
                    continue
        return dyn
