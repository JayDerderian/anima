"""
module for modifying composition() objects and imported MIDI files.


TODO:

    Implement a method to repeat an entire section of music and append it to a given MIDI file

    Implement a method to take a given section of music and modify notes and rhythms at random (or
    with specified user input)

    Implement a method to add notes and rhythms to the end of the file.
"""

from __future__ import annotations

from random import randint, shuffle

from utils.tools import to_str, is_pos, oct_equiv, scale_to_tempo
from containers.melody import Melody
from core.constants import NOTES


class Modify:
    """
    a class of modification methods that work with composition objects and
    imported MIDI files.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def transpose(
        pcs: list[int], dist: int | list[int], oct_eq: bool = True
    ) -> list[int]:
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
            for i in range(pcs_len):
                pcs[i] += dist
        # modify with a list of intervals across all pitch-class integers.
        # this allows for each pitch-class to be transposed by a unique
        # distance, allowing for rapid variation generation.
        # it could also be a list of the same repeated value but that
        # might be less efficient.
        elif type(dist) == list:
            for i in range(pcs_len):
                pcs[i] += dist[i]
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
        pcs = self.transpose(self.get_index(notes), dist=dist, oct_eq=False)
        return to_str(pcs, oct_eq=False)

    def transpose_c(self, chords: list, dist: int) -> list:
        """
        wrapper to use with chord() lists
        """
        if dist > 11 or dist < 1:
            raise ValueError("distance must be an int: 1<=n<=11")
        total_chords = len(chords)
        for c in range(total_chords):
            pcs = self.transpose(
                self.get_index(chords[c].notes), dist=dist, oct_eq=False
            )
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
        index_list = self.get_index(notes)
        ind_len = len(index_list)
        for n in range(1, ind_len):
            intervals.append(index_list[n] - index_list[n - 1])
        return intervals

    @staticmethod
    def get_index(notes: str | list[str]) -> int | list[int]:
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
            raise TypeError(
                "notes must be a single str or list[str]! type is:", type(notes)
            )

    @staticmethod
    def retrograde(melody: Melody) -> Melody:
        """
        reverses the elements in a melody object (notes, rhythms, dynamics)
        returns a duplicated melody() object
        """
        retro = melody
        retro.notes.reverse()
        retro.dynamics.reverse()
        retro.rhythms.reverse()
        return retro

    def invert(self, notes: list[str]) -> list[str | list[str]]:
        """
        inverts a melody. returns a new note list[str]
        """

        inverted = []  # list of inverted intervals
        intervals = self.get_intervals(notes)  # get list of intervals and invert values
        total_intervals = len(intervals)
        for i in range(total_intervals):
            if is_pos(intervals[i]):
                inverted.append(-abs(intervals[i]))
            else:
                inverted.append(abs(intervals[i]))

        # get index of first note. we don't need them all.
        mel = []
        mel.append(self.get_index(notes))

        # build new melody note list off this inverted interval list
        for i in range(total_intervals):
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
    def fragment(orig_melody: Melody) -> Melody:
        """
        randomly picks a subset of notes, rhythms, and dynamics (all
        from the same position in the melody) from a given melody and
        returns this subset as a melodic fragment in a new melody() object
        """
        # copy other info from supplied melody object
        # to not miss anything important. remove initial
        # notes ect so we can reuse the lists.
        frag = orig_melody
        frag.notes = []
        frag.rhythms = []
        frag.dynamics = []

        # generate fragment size. any subset will necessarily
        # be at least one element less than the original set.
        frag_len = randint(3, len(orig_melody.notes) - 2)

        # pick starting index and build fragment from here
        strt = randint(0, len(orig_melody.notes) - frag_len)
        for _ in range(frag_len):
            frag.notes.append(orig_melody.notes[strt])
            frag.rhythms.append(orig_melody.rhythms[strt])
            frag.dynamics.append(orig_melody.dynamics[strt])
            strt += 1

        return frag

    @staticmethod
    def mutate(melody: Melody) -> Melody:
        """
        randomly permutates the order of notes, rhythms, and dynamics
        in a given melody object. each list is permutated independently of
        each other, meaning original associations aren't preserved!

        returns a new Melody() object containing this permutation
        """
        mutant = melody
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
    def change_dynamics(dyn: int | list, diff: int) -> int | list:
        """
        makes a single or list of dynamics louder or softer
        by a specified amount. returns a modified dynamics list[int]

        needs to be an int that's a multiple of 4 and
        within the specified range! MIDI velocities start
        at 0 and increase by 4 until 127.
        """
        if type(dyn) == int:
            if dyn > 123:
                raise ValueError(
                    "supplied dynamic is too high. " f"max is 123. dyn supplied: {dyn}"
                )
            dyn += diff
        elif type(dyn) == list:
            total_dynamics = len(dyn)
            for d in range(total_dynamics):
                if dyn[d] < 123:
                    dyn[d] += diff

        return dyn

    @staticmethod
    def change_duration(rhythm: float, val: float) -> float:
        """
        Augment or diminish a single rhythmic duration.
        """
        rhythm += val
        return rhythm

    def change_durations(self, rhythms: list[float], val: float | list[float]) -> list:
        """
        Augment or diminish a Melody or Chord() object's rhythms by a specified amount.
        If a list of augmentation values are provided, they must be of equal length
        of the
        """
        if type(val) == float:
            for i in range(len(rhythms)):
                rhythms[i] += val

        elif type(val) == list:
            if len(val) != len(rhythms):
                raise ValueError(
                    f"augmentation value list must be same length as rhythms list"
                    f"vals: {len(val)}\nrhythms: {len(rhythms)}"
                )
            for i in range(len(rhythms)):
                rhythms[i] += val[i]
        else:
            raise TypeError(
                "augmentation values must be either type float or list[float]"
            )

        return rhythms
