"""
this module handles the analysis of composition() objects and
MIDI files.

TODO:
    convert MIDI file data to composition() object, as best as possible.
    mainly need to retrieve MIDI note numbers, velocities, and start/end times
    possibly parse_midi other parts of MIDI file as I learn more about them...

    comp object analysis:

        - list source data

        - get all PC's from each part
        - count all PCS
        - find most common pitch classes
        - match PCS against sets, scales, intervals

        - convert given rhythms to base rhythms (RHYTHMS),
        and create a rhythm analysis.
        - count most common base rhythms (rhythm classes?)

TODO: generate spectrogram of a given audio file
"""

from utils.midi import (
    load_midi_file,
    save,
    parse_midi,
    tempo2bpm,
    MIDI_num_to_note_name
)

from utils.tools import (
    remove_oct,
    oct_equiv,
    scale_to_tempo,
    all_same,
    to_str
)

from core.constants import (
    NOTES,
    PITCH_CLASSES,
    RHYTHMS,
    BEATS,
    RANGE,
    SCALES,
    SETS
)
from core.modify import Modify


class Analyze:
    """
    class of analysis functions to be used with composition() and MidiFile()
    objects.
    """

    def __init__(self) -> None:
        self.going = True

    # ---------------------------------Pitch class retrieval-------------------------------#

    def get_pcs_from_comp(self, comp):
        """
        gets all pitch classes from each part in a composition() object

        param: Composition()
        return: list[int]

        NOTE: this doesn't account if there's more than one of the same instrument!
              the dictionary key is the current melody object instrument, for now...
        """
        pcs = {}
        if len(comp.melodies) > 0:
            ml = len(comp.melodies)
            for m in range(ml):
                pcs[comp.melodies[m].instrument] = self.get_pcs(comp.melodies[m].notes)
            return pcs
        if len(comp.chords) > 0:
            cl = len(comp.chords)
            for c in range(cl):
                chords = comp.chords[c]
                chrd_len = len(chords)
                for chrd in range(chrd_len):
                    pcs[chords[chrd].instrument] = self.get_pcs(chords[chrd].notes)
            return pcs
        if len(comp.melodi_chords) > 0:
            ml_len = len(comp.melodi_chords)
            for m in range(ml_len):
                pcs[comp.melodi_chords[m].instrument] = self.get_pcs(comp.melodi_chords[m].notes)
        return pcs

    @staticmethod
    def get_pcs(notes):
        """
        matches pitch strings to pitch class integers.

        returns the corresponding pcs list[int]. list is unsorted, that is,
        it's in the original order of the elements in the submitted notes list
        """
        if type(notes) == str:
            # check if there's an octave int present 
            if not notes.isalpha():
                note = remove_oct(notes)
                pcs = PITCH_CLASSES.index(note)
            else:
                pcs = PITCH_CLASSES.index(notes)
        elif type(notes) == list:
            pcs = []
            nl = len(notes)
            for n in range(nl):
                if not notes[n].isalpha():
                    note = remove_oct(notes[n])
                    pcs.append(PITCH_CLASSES.index(note))
                else:
                    pcs.append(PITCH_CLASSES.index(notes[n]))
        else:
            raise TypeError("notes must be a list[int] or single int! type is", type(notes))
        return pcs

    # TODO: TEST THIS
    def count_pcs(self, tracks):
        """
        takes a list tracks (ideally parsed with midi.parse_midi()), then
        counts the number of instances of each pitch class in each track

        returns:
            dict(key = pitch class integer, value = total appearances)
        """
        pc_totals = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                     6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
        for track in tracks:
            # convert all MIDI note numbers to 
            # note name strings, then pitch classes (obvs not ideal)
            notes = []
            for n in range(len(tracks.notes)):
                notes.append(self.get_pcs(
                    MIDI_num_to_note_name(track.notes[n])
                ))
            for key in pc_totals:
                pc_totals[key] += notes.count(key)
        return pc_totals

    @staticmethod
    def get_index(notes):
        """
        gets the index or list of indices of a given note or
        list of notes in NOTES.

        note name str must have an assigned octave between 0-8.

        the returned list[int] should be used by transpose() with
        octeq set to False. those resulting values should be mapped
        back against NOTES to get octave-accurate transposed notes
        """
        if type(notes) == str:
            return NOTES.index(notes)
        elif type(notes) == list:
            indices = []
            notes_len = len(notes)
            for n in range(notes_len):
                indices.append(
                    NOTES.index(notes[n])
                )
            return indices
        else:
            raise TypeError("notes must be a single str or list[str]! "
                            "\ntype is:", type(notes))

    def find_normal_order(self, notes):
        """
        NOTE: Not ready! maybe match against SETS to see if it's actually
              in normal order

        takes a list of note name strings, converts them to pitch class integers,
        and finds an ordering "most packed to the left"

        returns pcs (list[int]) in normal order.
        """
        pcs = self.get_pcs(notes)  # get pcs from a given set
        pcs.sort()  # sort in ascending order
        # rotate until smallest interval in the set is 
        # at the left, and range of set is the smallest possible
        while pcs[1] - pcs[0] >= 2:
            pc = pcs.pop(0)
            pcs.append(pc)
        return pcs

    # TODO:
    def find_set(self, notes):
        """
        Given a set of notes, find an associated Forte set

            Reduce all notes (removing duplicates in any octave)
            in a given melody to an unordered set.

                Iterate through list, keeping track of each note
                it comes across.

                If we haven't seen this before, add to
                list, otherwise skip

            for note in notes:
                # remove the octave and see if we've seen this note before
                if note in found_notes:
                    continue
                else:
                    found_notes.append(note)

            Convert to pitch class integers, then sort in ascending order

            Convert to normal order, then compare against SETS

            NOTE: will need to expand SETS to include all sets in the Forte collection,
                  not just 5-9 note sets
        """
        ...

    # ----------------------------------Intervals------------------------------------#

    def get_intervals(self, notes):
        """
        generates a list of intervals from a given melody.
        total intervals will be len(m.notes)-1.

        difference between index values with NOTES corresponds to distance
        in semi-tones!
        """
        intrvls = []
        ind = self.get_index(notes)
        ind_len = len(ind)
        for n in range(1, ind_len):
            intrvls.append(ind[n] - ind[n - 1])
        return intrvls

    # TODO: 
    def get_interval_vector(self, notes):
        """
        gets the interval vector of a given set of
        notes.

        returns a dict[interval : frequency]
        """
        ...

    def check_range(self, notes: list[str], ran: list[str]):
        """
        checks for and removes and removes any notes
        not within the range of a given instrument.

        returns a modified note list[str]
        """
        diff = self.get_diff(notes, ran)
        if len(diff) > 0:
            difflen = len(diff)
            for note in range(difflen):
                notes.remove(diff[note])
        return notes

    @staticmethod
    def get_diff(notes, ran):
        """removes notes not in range of a given instrument with a provided range"""
        return [notes for notes in notes + ran if notes not in notes or notes not in ran]

    @staticmethod
    def get_range(notes: list[str]):
        """
        returns the lowest and highest note in a given set of notes
        in a tuple: (min, max)
        """
        min, max = 0, 0
        for note in notes:
            (min, max) = (10000, -1)
            n = NOTES.index(note)
            if n < int(min):
                min = n
            elif n > int(max):
                max = n
        return min, max

    # ---------------------------------------12 tone-------------------------------------#

    # TODO:
    def get_12tone_matrix(self, row, intrvls):
        """
        NOTE: NOT READY

        Generates a 2-D array/12-tone matrix from a given pitch class set (pcs = list[int]).
        Requires a list of 11 positive intervals between 1-11 ([1, 4, 2, 6]) to iterate off of.

        The matrix is generating by appending a transposition
        of the original row to each subsequent index.
        All other information, such as retrogressions, inversions, and
        retrogressions + inversions can be found using some print tricks.

        Returns a 2-D matrix - 'm'

        ---------

        Print original row:
            print(m[0])

        Print each row retrograde:
            for i in range(len(m[i])):
                retro = m[i]
                retro.reverse()
                print(retro)

        Print each row inversions (matrix column, top to bottom):
            for i in range(len(m))
                inv = [row[i] for row in m]
                print(inv)

        Print each row retrograde inversions (matrix column, bottom to top):
            for i in range(len(m))
                ret_inv = [row[i] for row in m]
                ret_inv[i].reverse()
                print(ret_inv)

        --------
        NOTE: maybe there's a way to populate the matrix using syntax like this:
        arr = [[r]*cols]*rows, where r is a modified version (transposition) of the
        original row.

        rows and cols are declared as a tuple (rows, cols = (n, n)
        where n is some int)
        """
        m = [[]]
        mod = Modify()
        # add original row to first matrix row
        for i in range(len(intrvls)):
            r = mod.transpose(row, intrvls[i])
            print("\nadding P", intrvls[i], ":", r)
            m.insert(i, r)
        return m

    @staticmethod
    def print_matrix(matrix):
        """
        Display a twelve-tone matrix (2D list)
        """
        for x in matrix:
            for y in x:
                print(y, end=" ")
            print()

    # -----------------------------------MIDI analysis--------------------------------------#

    def parse_MIDI(self, file_name: str):
        """
        analyzes a given MIDI file with a given file_name (str)

        returns a dictionary with nested dictionaries containing
        information about pitch class content, tempo, and velocities
        for each track

        TODO: still need to figure out rhythms...
              extract start/end times for each note, subtract end
              from start, then store?
        """
        vels = {}
        pcints = {}
        res = {
            "Tempo": 0,
            "Pitch Classes": {},
            "Rhythms": {},
            "Dynamics": {}
        }
        # get MidiTrack() dict and Messages() list
        tracks, msgs = parse_midi(file_name)
        # get global tempo
        res["Tempo"] = tempo2bpm(msgs[0].tempo)
        # get pitch class integers and velocities from each track
        for t in range(len(tracks)):
            pcs = []
            vel = []
            track = tracks[f"track {str(t)}"]
            for i in range(len(track)):
                if hasattr(track[i], "velocity"):
                    # skip any silent notes (rests)
                    if track[i].velocity == 0:
                        continue
                    # translate to note name...
                    note = MIDI_num_to_note_name(track[i].note)
                    # ...then to PC integer because reasons
                    pcs.append(self.get_pcs(note))
                    vel.append(track[i].velocity)
            pcints[f"track {str(t)}"] = pcs
            vels[f"track {str(t)}"] = vel

        res["Pitch Classes"].update(pcints)
        res["Dynamics"].update(vels)

        return res


""""
some additional methods for handling meter. these are mainly used 
sporadically and didn't really warrant being part of the larger analyze method class,
at least for now...
"""


def is_simple(meter):
    """returns True if meter is a simple meter"""
    return is_valid(meter)


def is_compound(meter):
    """returns True if meter is a compound meter"""
    return is_valid(meter) and meter[0] % 3 == 0 and 6 <= meter[0]


def is_valid(meter):
    """returns True if meter is valid (rational)"""
    return meter[0] > 0 and valid_beat_duration(meter)


def valid_beat_duration(meter):
    """returns True if meter denominator is a valid beat duration"""
    return True if meter[1] in BEATS else False
