"""
This module handles all generative methods.
"""

import urllib.request
from math import floor
from names import get_full_name
from datetime import datetime as date
from random import seed, randint, sample, choice

from utils.mapping import map_data
from utils.txtfile import gen_info_doc
from utils.midi import export_midi
from utils.tools import to_str, oct_equiv, scale_to_tempo, scale_limit

from core.constants import (
    NOTES,
    CHROMATIC_SCALE,
    PITCH_CLASSES,
    RHYTHMS,
    REST,
    DYNAMICS,
    TEMPOS,
    INSTRUMENTS,
    SCALES,
    ARPEGGIOS,
    SETS,
    INTERVALS,
    RANGE,
)
from core.modify import Modify
from core.analyze import Analyze

from containers.bar import Bar
from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition


class Generate:
    """
    This class handles all generative functions.
    """

    def __init__(self):
        seed()
        self.mod = Modify()  # modifier class

    ### TITLE ###

    @staticmethod
    def new_title() -> str:
        """
        Generate a composition title from 1-4 random words.

            Random word generation technique from:
            https://stackoverflow.com/questions/18834636/random-word-generator-python
        """
        try:
            url = "https://www.mit.edu/~ecprice/wordlist.10000"  # get word list
            response = urllib.request.urlopen(url)
            text = response.read().decode()  # decode data to text string
            words = text.splitlines()  # separate words into list
            t = 0
            total = randint(1, 3)  # pick 1 to 3 random words
            name = choice(words)
            while t < total:
                name = name + " " + choice(words)
                t += 1
        except urllib.error.URLError as e:
            print(f"unable to retrieve word list: {e}")
            name = "untitled - "
        except Exception as e:
            print(f"exception occurred trying to retrieve word list: {e}")
            name = "untitled - "
        return name

    @staticmethod
    def new_composer() -> str:
        return get_full_name()

    def init_comp(
        self, tempo: float = None, title: str = None, composer: str = None
    ) -> Composition:
        """
        Initializes a Composition() object by creating
        the title, composer name, tempo, and file names:
        (date, midi and txt file names)

        tempo and composer name could also be provided.
        """
        comp = Composition()

        if tempo is None:
            comp.tempo = self.new_tempo()
        elif tempo > 40.0 or tempo < 208.0:
            comp.tempo = tempo
        else:
            comp.tempo = 60.0  # erroneous tempo values are replaced with 60bpm
        if title is None:
            comp.title = self.new_title()
        else:
            comp.title = title
        if composer is None:
            comp.composer = self.new_composer()
        else:
            comp.composer = composer

        comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
        comp.midi_file_name = f"{comp.title}.mid"
        comp.txt_file_name = f"{comp.title}.txt"

        return comp

    ### TEMPO ###

    @staticmethod
    def new_tempo() -> float:
        """
        Picks tempo between 40-208bpm.
        """
        return choice(TEMPOS)

    ### INSTRUMENTS ###

    @staticmethod
    def new_instrument() -> str:
        """
        Randomly picks a melodic/harmonic instrument from a given list. Returns a string.
        Does NOT pick a percussion instrument!
        """
        return INSTRUMENTS[randint(0, 110)]

    @staticmethod
    def new_instruments(total: int) -> list[str]:
        """
        Generates a list of instruments of n length, where n is supplied from elsewhere.
        Returns a list.
        """
        return [INSTRUMENTS[randint(0, 110)] for inst in range(total)]

    ### PITCH ###

    @staticmethod
    def rand_note() -> str:
        """
        Picks a note at random between octaves 1 and 7.
        Returns a string representing the note, such as "C#2"
        """
        return f"{choice(PITCH_CLASSES)}{randint(1, 7)}"

    @staticmethod
    def choose_note(scale: list[str]) -> str:
        """
        Picks a note at random from a given list of notes
        """
        return choice(scale)

    def new_notes(
        self, data=None, root: list = None, total: int = None
    ) -> tuple[list, list, list]:
        """
        Generates a set of notes to be used as a melody. Can also
        use a specified root scale, and a specified note total.

        Can also return a list of notes without any input. If this is the case,
        new_notes() will decide how many to generate (between 3 and 50).

        Data that can be used:
            A supplied data list (list[int]) of n length functions as *index numbers*
            against a generated "source scale" to select melody notes.

        User also has the option to supply a "root" scale, though only if the program
        is accessing this method directly! new_melody() and other methods that call this
        function don't supply a root if none is chosen by the user.

        Returns a tuple:
            notes list to be used as a melody (list[str]),
            note meta data (list[str]),
            original source scale (list[str])
        """

        meta_data = []  # save forte numbers and/or pitch class sets
        octave = randint(2, 3)  # initial starting octave
        if root is None:
            root, info = self.pick_root(transpose=True, octave=None)
            meta_data.append(info)
        if data is None:
            if total is None:
                # Pick total: 10 - 50 if we're generating random notes
                gen_total = randint(9, 49)
            else:
                gen_total = total
        # Or the largest value of the supplied data set. This will give
        # us the maximum number of notes we will need to generate and still
        # have a viable range to choose from -- i.e., if the largest element
        # in the data set is 100, then we will get a set of 100 notes in our
        # source scale, so we can map the inputted 100 to the note in the
        # source scale by treating the data value as an index number.
        else:
            gen_total = max(data) + 1

        # Generate source scale
        # NOTE: This only uses a supplied root scale once!
        # After we reach the final octave this will pick another
        # scale to build off of. May need to parameterize this behavior.
        n = 0
        scale = []
        for _ in range(gen_total):
            note = f"{root[n]}{octave}"
            scale.append(note)
            n += 1
            if n == len(root):
                octave += 1
                if octave > 5:
                    octave = randint(2, 3)
                    root, info = self.pick_root(transpose=True, octave=None)
                    meta_data.append(info)
                n = 0

        # Randomly pick notes from the generated source
        # scale to create an arrhythmic melody.
        notes = []
        if data is None:
            # Total notes in melody will be between 3 and
            # however many notes are in the source scale if no
            # total value is provided.
            if total is None:
                pick_total = randint(3, len(scale))
            else:
                pick_total = total
            notes = [choice(scale) for _ in range(pick_total)]
        # ...Or pick notes according to integers in data array
        else:
            # Map notes to the inputted data to generate a melody.
            # Total number of notes is equivalent to the
            # number of elements in the data set. Any supplied
            # total value won't matter here since we're going of len(data)
            # for our total because reasons.
            data_len = len(data)
            for i in range(data_len):
                notes.append(scale[data[i]])

        return notes, meta_data, scale

    @staticmethod
    def choose_notes(source_notes: list, total: int) -> list:
        """
        Choose a set (size total) of notes at random from a given set of notes.
        """
        return [choice(source_notes) for _ in range(total)]

    def pick_root(self, transpose: bool = True, octave: int = None) -> tuple[list, str]:
        """
        Picks a randomly chosen and transposed scale, a 5 to 9
        note Forte pitch class prime form, or randomly generated scale,
        each randomly transposed as well.

        Set transpose to false if an non-transposed root scale is preferred.
        This will default to the starting pitch always being C.

        Returns tuple:
            list[str] of note name strings (with or without an assigned octave)
            info (str) about the chosen scale.
        """
        # use scale? (1), pcs prime form (2), or invented scale(3)?
        choice = randint(1, 3)
        if choice == 1:
            if transpose:
                mode, pcs, scale = self.pick_scale(transpose=True)
                info = f"{scale[0]} {mode}"
            else:
                mode, pcs, scale = self.pick_scale(transpose=False)
                info = f"{scale[0]} {mode}"
        elif choice == 2:
            if transpose:
                fn, pcs, scale = self.pick_set(transpose=True)
                info = f"set {fn} transposed to {scale[0]}"
            else:
                fn, pcs, scale = self.pick_set(transpose=False)
                info = f"set {fn} un-transposed {scale[0]}"
        else:
            if transpose:
                scale, pcs = self.new_scale(transpose=True)
                info = f"invented scale: {scale} pcs: {pcs}"
            else:
                scale, pcs = self.new_scale(transpose=False)
                info = f"invented scale: {scale} pcs: {pcs}"

        scale = to_str(pcs=pcs, octave=octave)
        return scale, info

    def pick_scale(
        self, transpose: bool = True, octave: int = None
    ) -> tuple[str, list[int], list]:
        """
        Picks a scale, randomly transposes it (if indicated),
        and appends a specified octave (if needed).

        Returns a tuple:
            the scale name (str),
            un-transposed scale pcs (list[int]),
            note list (list[str]) *without assigned octave by default.*

        Supply a value for o if a specified octave is needed.
        """
        scale = choice(list(SCALES.keys()))
        pcs = SCALES[scale]
        if transpose:
            pcs_t = self.mod.transpose(pcs, randint(1, 11), oct_eq=False)
            notes = to_str(pcs_t, octave=octave)
        else:
            notes = to_str(pcs, octave=octave)
        return scale, pcs, notes

    def pick_set(
        self, transpose: bool = True, octave: int = None
    ) -> tuple[str, list[int], list]:
        """
        Selects prime form and transposes a random distance (or not)

        Returns a tuple:
            forte number/fn (str),
            un-transposed prime form pcs (list[int]),
            note list (list[str]) *without an assigned octave* by default.

        Supply a value for o if a specified octave is needed.
        """
        forte_number = choice(list(SETS.keys()))
        pcs = SETS[forte_number]
        if transpose:
            pcs_t = self.mod.transpose(pcs, randint(1, 11), oct_eq=False)
            scale = to_str(pcs_t, octave=octave)
        else:
            scale = to_str(pcs, octave=octave)
        return forte_number, pcs, scale

    def new_scale(
        self, transpose: bool = True, octave: int = None
    ) -> tuple[list, list[int]]:
        """
        Returns a randomly generated 5 to 8 note scale with or without an octave
        to be used as a 'root'. Can take an int as a starting octave
        (between 2 and 5), or not.

        To be used externally from newNotes() to supply a new "root," as an option
        for the user.

        Returns a tuple: notes (list[str]) and the original pitch class set, (list[int]).
        """
        pcs = []
        total = randint(5, 8)
        """
        Current approach. Outputs are quite interesting, though I think this
        is the least efficient way to go about this...
        """
        while len(pcs) < total:
            n = randint(0, 11)
            if n not in pcs:
                pcs.append(n)
        # pcs = [randint(0,11) for x in range(total) if x not in pcs]
        pcs.sort()
        if transpose:
            pcs = self.mod.transpose(pcs, randint(1, 11), oct_eq=False)
        scale = to_str(pcs, octave)
        return scale, pcs

    @staticmethod
    def new_source_scale(root: list[str]) -> list[str]:
        """
        Generates a list[str] "source scale" based off a
        supplied root (list[str]). List should contain
        strings representing notes without an assigned octave,
        i.e.: root = ["C", "D", "E", ...]

        Does not pick additional roots! Mostly used by other methods.

        Returns a list[str] with appended octaves (2-6)
        """
        n = 0
        o = 2
        scale = []
        for _ in range(28):
            scale.append(f"{root[n]}{o}")
            n += 1
            if n == len(root):
                o += 1
                if o == 6:
                    o = 2
                n = 0
        return scale

    def new_source_scales(self, total: bool = None) -> tuple[dict, list]:
        """
        generates a dictionary of source scales to choose from.

        returns a tuple:
            sources (dict[int, list[str]])
            scale_info (list[str])
        """
        if total is None:
            total = randint(3, 8)  # pick 3-8 scales if no total is provided

        sources = {}
        scale_info = []
        for scale in range(total):
            root, info = self.pick_root()
            scale_info.append(info)
            sources[scale] = self.new_source_scale(root)

        return sources, scale_info

    @staticmethod
    def derive_scales(pcs: list, octave: int = None) -> dict:
        """
        Generate derivative scales based on each note in a given scale.
        Requires a pitch class set (pcs) list[int] who's values are
        between 0 - 11, and returns a dictionary of variant scales (list[str])

        Each variant scale will have an assigned octave, with or without
        user input.

        1. Start with first note in pitch class set (pcs).

        2. Derive each subsequent note by adding a randomly
           chosen value to the sum of the previous

           n0+=rand(1,3), n1 = n0+=rand(1,3), n2 = n1+=rand(1,3), etc...

        3. Repeat step 2 with next note in supplied pcs up to end of scale.
        """
        variants = {}
        pcs_len = len(pcs)
        for i in range(pcs_len):
            scale_variant = []
            note = pcs[i]
            while len(scale_variant) < pcs_len:
                note += randint(1, 3)
                scale_variant.append(note)
            variants[i] = scale_variant

        for scale in variants:
            variants[scale] = to_str(variants[scale], octave=octave, oct_eq=False)

        return variants

    @staticmethod
    def pick_arp(key: str) -> list[int]:
        """
        Returns a list[int] of pitch classes outlining a one-octave
        arpeggio.
        """
        if key in ARPEGGIOS.keys():
            return ARPEGGIOS[key]
        else:
            raise ValueError(
                f"{key} is not a valid parameter. "
                f"available parameters: {list(ARPEGGIOS.keys())}"
            )

    @staticmethod
    def new_12tone_row() -> list[str]:
        """
        Generates a 12-tone row. Returns a note list[str].
        Notes don't have an assigned octave.
        """
        return sample(PITCH_CLASSES, len(PITCH_CLASSES))

    @staticmethod
    def new_12tone_intervals() -> list:
        """
        Returns a list of 11 non-repeating intervals to generate 12-tone row
        transpositions.
        """
        return sample(INTERVALS["Chromatic Scale"], len(INTERVALS["Chromatic Scale"]))

    @staticmethod
    def new_palindrome(melody) -> Melody:
        """
        Takes either a list of chord() objects or a single melody()
        object, and creates a palindrome from it.

        Returns either a modified list[chord()], or modified melody()
        """
        # chord() list
        if type(melody) == list:
            mel_rev = melody
            mel_rev.reverse()
            melody.extend(mel_rev)
        # melody() object
        elif isinstance(melody, Melody):
            melody.notes.extend(melody.notes.reverse())
            melody.rhythms.extend(melody.rhythms.reverse())
            melody.dynamics.extend(melody.dynamics.reverse())
        else:
            raise TypeError(
                "parameter must be either a list or Melody() object"
                f"param was type: {type(melody)}"
            )
        return melody

    ### RHYTHM ###

    @staticmethod
    def new_rhythm() -> float:
        """
        Generates a single new rhythm. Not scaled to tempo!
        """
        return choice(RHYTHMS)

    def new_rhythms(
        self, total: int = None, tempo: float = None, source_rhythms: list = None
    ):
        """
        Generates a series of rhythms of n length, where n is supplied
        from elsewhere. Can also decide to pick 3 and 30 rhythms
        if no desired total is supplied. Will convert raw rhythm values
        to a given tempo, if provided. Otherwise, it'll just return an
        unaltered float list.

        Can also use a set of source_rhythms to choose from. If left empty (which is the default),
        then new_rhythms will choose from the default set of available rhythms.

        Uses infrequent and randomized repetitions.

        NOTE: Supply a smaller value for 'total' if a shorter pattern
              is needed. 'total' can be used to sync up with a given list or
              be hard-coded.
        """
        rhythms = []
        if total is None:
            total = randint(3, 30)
        if source_rhythms:
            _rhythms = source_rhythms
        else:
            _rhythms = RHYTHMS

        # generate rhythms
        while len(rhythms) < total:
            rhythm = choice(_rhythms)  # Pick rhythm and add to list
            if randint(1, 2) == 1:  # Repeat this rhythm or not?
                limit = self._rep_limit(total)
                total_reps = randint(1, limit)
                for _ in range(total_reps):
                    rhythms.append(rhythm)
                    if len(rhythms) == total:
                        break
            else:
                rhythms.append(rhythm)

        # scale to given tempo if provided.
        if tempo is not None and tempo != 60.0:
            rhythms = scale_to_tempo(tempo, rhythms)

        return rhythms

    @staticmethod
    def _rep_limit(total: int):
        limit = scale_limit(total)  # TODO: revisit this
        if limit == 0:
            limit += 2
        return limit

    ### DYNAMICS ###

    @staticmethod
    def new_dynamic(rests: bool = True) -> int:
        """
        Generates a single dynamic/velocity between 20 - 124
        OR a single rest!
        """
        if rests:
            return choice(DYNAMICS) if randint(0, 1) == 1 else REST
        else:
            return choice(DYNAMICS)

    @staticmethod
    def _new_dynamics_with_silences(total_dynamics: int, dynamics: list):
        """
        Creates a list of dynamic/velocities with optional silences.
        Will also randomly repeat a dynamic n times.
        """
        while len(dynamics) < total_dynamics:
            if randint(0, 1) == 1:  # Pick dynamic OR a rest
                dynamic = choice(DYNAMICS)
                if randint(1, 2) == 1:  # repeat?
                    # scale total reps with regards to the total number of dynamic/velocities we have
                    # we want to avoid repeating the dynamic/velocities *too* many times, so we try to
                    # repeat something with a "sane" number of repetiions -- i.e., doesn't dominate the
                    # entire set of dyanmics.
                    rep_limit = scale_limit(total_dynamics)
                    if rep_limit == 0:
                        rep_limit += 2
                    total_reps = randint(1, rep_limit)
                    for _ in range(total_reps):
                        dynamics.append(dynamic)
                        if len(dynamics) == total_dynamics:
                            break
                else:
                    dynamics.append(dynamic)
            else:
                dynamic = REST
                if randint(1, 2) == 1:  # repeat?
                    total_reps = randint(1, 2)  # only repeat rests 1-2 times for now...
                    for _ in range(total_reps):
                        dynamics.append(dynamic)
                        if len(dynamics) == total_dynamics:
                            break
                else:
                    dynamics.append(dynamic)

        return dynamics

    @staticmethod
    def _new_dynamics(total_dynamics: int, dynamics: list) -> list:
        """
        Generates a list of dynamics without silences(rests)
        """
        while len(dynamics) < total_dynamics:
            dynamic = choice(DYNAMICS)
            if randint(1, 2) == 1:  # repeat?
                # scale total reps with regards to the total number of dynamic/velocities we have
                # we want to avoid repeating the dynamic/velocities *too* many times, so we try to
                # repeat something with a "sane" number of repetiions -- i.e., doesn't dominate the
                # entire set of dyanmics.
                rep_limit = scale_limit(total_dynamics)
                if rep_limit == 0:
                    rep_limit += 2
                total_reps = randint(1, rep_limit)
                for _ in range(total_reps):
                    dynamics.append(dynamic)
                    if len(dynamics) == total_dynamics:
                        break
            else:
                dynamics.append(dynamic)

        return dynamics

    def new_dynamics(self, total: int = None, rests: bool = True) -> list[int]:
        """
        Generates a list of dynamics (MIDI velocities) of n length,
        where n is supplied from elsewhere. Uses infrequent repetition.
        Can also pick between 3 and 30 rhythms if no total is supplied.

        Randomly selects REST to insert a rest into a composition.

        Uses infrequent repetition.

        NOTE: Supply a smaller value for 'total' if a shorter pattern
              is needed. 'total' can be used to sync up with a given list or
              be hard-coded.
        """
        if total is None:
            total = randint(3, 30)
        if rests:
            return self._new_dynamics_with_silences(total, [])
        else:
            return self._new_dynamics(total, [])

    ### CHORDS ###

    @staticmethod
    def display_chord(chord: Chord) -> None:
        output = (
            f"\n------------Chord:-------------"
            f"\nnotes: {chord.notes}"
            f"\nrhythm: {chord.rhythm}"
            f"\ndynamic: {chord.dynamic}"
        )
        print(output)

    def display_chords(self, chords: list) -> None:
        print("\n----------------HARMONY INFO:-------------------")
        chord_len = len(chords)
        for i in range(chord_len):
            print("\n", i + 1, ": ", "Notes:", chords[i].notes)
            self.display_chord(chords[i])

    @staticmethod
    def get_chord_durations(chords: list) -> float:
        """
        Returns the total length  in seconds (float) of a series
        of chord() objects (chord progression).
        """
        duration = 0.0
        chord_len = len(chords)
        for chord in range(chord_len):
            duration += chords[chord].rhythm
        return duration

    def new_chord(
        self, tempo: float = None, scale: list = None, asyn: bool = True
    ) -> Chord:
        """
        Generates a 2-9 note chord with randomly chosen notes from either a supplied
        scale or self-selected or generated one.

        If asyn is True, the chord will also have its rhythm and dynamic randomly chosen.
        asyn is True by default.

        Returns a chord() object. Does not assign an instrument!
        """
        new_chord = Chord()
        if tempo is None:
            new_chord.tempo = 60.0
        else:
            new_chord.tempo = tempo
        if scale is None:
            # pick an existing scale/set or make a new one?
            if randint(1, 2) == 1:
                new_chord.source_notes, new_chord.info = self.pick_root(
                    octave=randint(2, 5)
                )
                new_chord.pcs = "None"
            else:
                new_chord.source_notes, new_chord.pcs = self.new_scale(
                    octave=randint(2, 5)
                )
                new_chord.info = "Invented Scale"
        else:
            new_chord.source_notes = scale

        # pick notes
        total = randint(2, 9)
        new_chord.notes = [choice(scale) for _ in range(total)]

        # only add randomized rhythm and dynamics if specified.
        # chords can just be a set of notes and the other parameters can be
        # handled externally.
        if asyn:
            rhythm = self.new_rhythm()
            if new_chord.tempo != 60:
                rhythm = scale_to_tempo(new_chord.tempo, rhythm)
            new_chord.rhythm = rhythm
            new_chord.dynamic = self.new_dynamic(rests=False)

        return new_chord

    def new_chords(
        self, total: int = None, tempo: float = None, scale: list = None
    ) -> list[Chord]:
        """
        Generates a progression from the notes of a given scale.
        Returns a list of chord() objects (5-11 if no total is
        supplied). Each chord will have 2 to 9 notes in various
        registers, as well as a unique dynamic and rhythm.

        chord() objects *wont* have assigned instruments!

        NOTE: Chords will be derived from the given scale ONLY!
              Could possibly add more randomly inserted chromatic
              tones to give progressions more variance and color.
        """
        chords = []
        if total is None:
            total = randint(5, 11)
        if tempo is None:
            tempo = self.new_tempo()
        if scale is None:
            scale = self.new_notes()[0]
        for _ in range(total):
            new_chord = self.new_chord(tempo, scale)
            chords.append(new_chord)
        return chords

    @staticmethod
    def new_triads(scale: list, total: int) -> list[Chord]:
        """
        generates a list of triads of t length from a given multi-octave
        source scale. a single octave scale will only yield 3 triads since
        the third chord will pick the last element in the list.

        ideally a list[str] of note chars in at least two octaves will
        be supplied.

        Pick notes by accessing every other index three times.

        returns a list of chord() objects. if t is not supplied, then
        it will generate as many chords as it can until an IndexError
        exception is raised.

        NOTE: chords don't have tempo or instrument assigned!
        """
        triads = []
        scale_len = len(scale)
        for i in range(4, scale_len):
            triad = Chord()
            triad.notes = [scale[i - 4], scale[i - 2], scale[i]]
            triad.rhythm = 2.0  # half note by default
            triad.dynamic = 100  # mezzo-forte-ish
            triads.append(triad)
            if len(triads) == total:
                break

        return triads

    @staticmethod
    def new_sym_triad(root: str, interval: int, n: int) -> list:
        """
        generates an intervallicly symmetrical chord of n length
        based off a given root (r) and interval (i).

        returns a list[int] between 0 - 11 of n length.

        Returns -1 if given interval is invalid.
        """
        if interval > 6 or interval < 1:
            raise ValueError("Interval must be between 1 and 6")
        if root > 11 or root < 0:
            root = oct_equiv(root)
        chord = []
        while len(chord) < n:
            chord.append(root)
            root += interval
            if root > 11:
                root = oct_equiv(root)
        return chord

    ### MELODIES ###

    @staticmethod
    def display_melody(m: Melody) -> None:
        """
        Displays melody() object data
        """
        output = (
            f"\n-----------MELODY Info------------"
            f"\nTempo: {m.tempo} bpm"
            f"\nInstrument: {m.instrument}"
            f"\nPitch Classes: {m.pcs}"
            f"\nSource Data: {m.source_data}"
            f"\nInfo: {m.info}"
            f"\nTotal Notes: {len(m.notes)}"
            f"\nNotes: {m.notes}"
            f"\nTotal rhythms: {len(m.rhythms)}"
            f"\nRhythms: {m.rhythms}"
            f"\nTotal Dynamics: {len(m.dynamics)}"
            f"\nDynamics: {m.dynamics}"
        )
        print(output)

    def new_melody(
        self,
        tempo: float = None,
        raw_data=None,
        data_type: int = None,
        total: int = None,
        inst_range: bool = None,
        rests: bool = True,
    ) -> Melody:
        """
        Picks tempo, notes, rhythms, and dynamics, with or without a
        supplied list from the user. It can process a list of ints
        (dt == 1), floats(2), single char strings/letters(3),
        or a hex number, represented as a single string(4)

        if data is supplied, then adding a value for t will be redundant
        since this just goes off the total elements in the data list.

        If no data is supplied, then it will generate a melody anyway.

        Returns a melody() object

        NOTE: Instrument is *NOT* picked! Needs to be supplied externally.
        """
        melody = Melody()

        # Process any incoming data
        if data_type is not None and raw_data is not None:
            source_data = raw_data
            melody.source_data = source_data
            processed_data = map_data(raw_data, data_type)
        else:
            melody.source_data = "None"
        # Set tempo
        if tempo is None:
            melody.tempo = self.new_tempo()
        else:
            melody.tempo = tempo

        # Pick notes from scratch
        if raw_data is None:
            if total is None:
                (melody.notes, melody.info, melody.source_notes) = self.new_notes()
            else:
                (melody.notes, melody.info, melody.source_notes) = self.new_notes(
                    total=total
                )
        # Or use supplied data. Supplied total isn't applicable with
        # a data set of n size, since n will just become the total we work with.
        else:
            (melody.notes, melody.info, melody.source_notes) = self.new_notes(
                data=processed_data
            )

        # remove any notes not within a supplied range (if available)
        if inst_range is not None:
            melody_len = len(melody.notes)
            for note in range(melody_len):
                if melody.notes[note] not in inst_range:
                    melody.notes.remove(melody.notes[note])

        # add rhythms and dynamics
        melody.rhythms = self.new_rhythms(len(melody.notes), melody.tempo)
        melody.dynamics = self.new_dynamics(len(melody.notes), rests)

        return melody

    def write_string_line(
        self, part: Melody, scale: list, total: int, asyn: bool = False
    ) -> Melody:
        """
        writes a melodic line for a string instrument (violin, viola, cello, or bass TBD)

        **doesn't add rhythm or dynamics** if asyn==False,
        which it is by default. if asyn==true, then any supplied
        total will be overwritten! still working on that
        quirk...

        returns a modified Melody() object
        """
        if part.instrument not in ["Violin", "Viola", "Cello", "Contrabass"]:
            raise ValueError("melody object must be assigned a string instrument")

        if asyn:
            # NOTE: this will redefine supplied total if asyn is True
            total = randint(12, 30)

        for _ in range(total):
            # limited to octaves 4 and 5 for violins
            if part.instrument == "Violin":
                note = scale[randint(13, len(scale) - 1)]
                while note not in RANGE["Violin"]:
                    note = scale[randint(13, len(scale) - 1)]
                part.notes.append(note)

            # limit to octaves 3 and 4 for viola
            elif part.instrument == "Viola":
                note = scale[randint(7, len(scale) - 8)]
                while note not in RANGE["Viola"]:
                    note = scale[randint(7, len(scale) - 8)]
                part.notes.append(note)

            # limit to octaves 2 and 3 for cello
            elif part.instrument == "Cello":
                note = scale[randint(0, len(scale) - 16)]
                while note not in RANGE["Cello"]:
                    note = scale[randint(0, len(scale) - 16)]
                part.notes.append(note)

        if asyn:
            # add independent rhythms and dynamics of n length
            part.rhythms.extend(
                self.new_rhythms(total=len(part.notes), tempo=part.tempo)
            )
            part.dynamics.extend(self.new_dynamics(total=len(part.notes)))

        return part

    ### NEW COMPOSITION ###

    def new_composition(self, data=None, data_type=None) -> Composition:
        """
        Generates 1 melody and set of harmonies with our without
        inputted data.

        Takes a 0x-xxxxxx hex humber representing a color, or
        an array of ints, floats or chars of any length as arguments,
        plus the data type represented by an int
        (int (1), float (2), char (3), or hex number (4)).

        Outputs a a MIDI file, a .txt file with the compositions' data (title, instrumentation,
        notes, etc...).

        Returns a composition() object on success, or -1 on failure.
        """
        comp = self.init_comp()
        comp.ensemble = "duet"

        # Generate a melody only if we have both data and data_type args
        if data is not None and data_type is not None:
            melody = self.new_melody(
                tempo=comp.tempo, raw_data=data, data_type=data_type
            )
        else:
            melody = self.new_melody(tempo=comp.tempo)
        # Pick instrument
        melody.instrument = self.new_instrument()
        # Save melody info
        comp.add_part(melody, melody.instrument)

        # Generate harmonies from this melody.
        # Total is between half the number of notes
        # in the melody and total num of notes.
        chords = self.new_chords(
            total=randint(floor(len(melody.notes) / 2), len(melody.notes)),
            tempo=comp.tempo,
            scale=melody.notes,
        )
        # Pick keyboard instrument and apply to all chord objects
        instr = INSTRUMENTS[randint(0, 8)]
        for i in range(len(chords)):
            chords[i].instrument = instr

        # Save chord object list
        comp.add_part(chords, instr)

        # Add title and write out MIDI
        comp.title = f"{comp.title} for mixed duet"
        export_midi(comp)

        # display final info
        comp.display()
        return comp
