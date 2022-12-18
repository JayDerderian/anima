"""
Module for handling all composition data. Contains a Composition() class/container.
"""
# from core.analyze import Analyze
from containers.chord import Chord
from containers.melody import Melody


class Composition:
    """
    This is a container for all things related to a stand-alone music composition.

    Title, composer, date of composition, MIDI file name, text file name, global tempo,
    ensemble type, instrument list, list of picked instruments, lists melodies, and
    a dictionary of chord progressions.
    """
    def __init__(self, title=None, composer=None, tempo=None):

        if title is not None:
            self.title = title
        else:
            self.title = ""
        if composer is not None:
            self.composer = composer
        else:
            self.composer = ""
        self.date = ""
        self.midi_file_name = ""
        self.txt_file_name = ""

        # global tempo
        if tempo is not None:
            self.tempo = tempo
        else:
            self.tempo = 60.0

        # "trio," "duet", etc..
        self.ensemble = ""
        # list of instruments in the piece
        self.instruments = []
        # self.parts is a dictionary where each entry is a list
        # of either Melody() or Chord() (or both!) objects,
        # or a single Melody() or Chord() object
        # the key is the name of the instrument, the value is the object
        self.parts = {}

    def __repr__(self) -> str:
        if len(self.instruments) == 0:
            return ""
        elif len(self.instruments) == 1:
            return f"{self.title} for solo {self.instruments[0]}"
        else:
            return f"{self.title} for {len(self.instruments)} instruments"

    def _get_instrument_list(self) -> list:
        return self.instruments


    def _duration(self) -> float:
        """
        Finds the longest individual part in the piece.
        This will be the duration (in seconds)
        """
        longest = 0.0
        for track in self.parts:
            dur = 0.0
            if isinstance(self.parts[track], Melody) or isinstance(self.parts[track], Chord):
                dur += self.parts[track].duration()
                if dur > longest:
                    longest = dur
            elif isinstance(self.parts[track], list):
                # sum the entire list since each object is considered
                # a "single" part here
                for obj in self.parts[track]:
                    dur += obj.duration()
                if dur > longest:
                    longest = dur
        return longest

    ### Public methods ###

    def is_used(self, instr: str) -> bool:
        """
        Has this instrument been picked already?
        """
        return True if instr in self.instruments else False

    def all_picked(self, instruments: list) -> bool:
        """
        Have *all* the instruments been used?
        Compares against an externally generated instrument list.
        """
        return True if instruments == self.instruments else False

    def how_many(self, instr: str) -> int:
        """
        Determines how many occurrences of this instrument are in this piece
        """
        return self.instruments.count(instr)

    def add_instrument(self, instrument: str) -> None:
        self.instruments.append(instrument)

    def remove_instrument(self, instrument: str) -> None:
        if instrument in self.instruments:
            self.instruments.remove(instrument)

    def display(self) -> None:
        """
        display composition info
        """
        output = f"\ntitle: {self.title}" \
                 f"\ntempo: {self.tempo}" \
                 f"\ncomposer: {self.composer}" \
                 f"\nduration: {self.duration()}" \
                 f"\nmidi file: {self.midi_file_name}" \
                 f"\ntext file: {self.txt_file_name}\n"
        print(output)

    def duration(self) -> str:
        """
        returns the compositions' duration as a formatted string
        """
        minutes, seconds = divmod(self._duration(), 60)
        return str(int(minutes)) + " min " + str(seconds) + " sec "

    def add_part(self, part, instr: str) -> None:
        """
        Add a part to this composition
        """
        self.instruments.append(instr)
        self.parts.update({
            f"{instr} {self.how_many(instr) + 1}": part
        })

    def remove_part(self, part: str) -> None:
        """
        Remove a part from this composition.
        part param must be a string like 'violin 1'
        """
        if part in list(self.parts.keys()):
            self.instruments.remove(part)
            del self.parts[part]
