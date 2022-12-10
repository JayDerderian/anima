"""
Module for handling all composition data. Contains a Composition() class/container.
"""

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

        self.ensemble = ""  # "trio," "duet", etc..
        self.instruments = []  # list of instruments
        # self.tracks is a dictionary where each entry is a list
        # of either Melody() or Chord() (or both!) objects.
        self.tracks = dict


    def __repr__(self) -> str:
        if len(self.instruments) == 0:
            return ""
        elif len(self.instruments) == 1:
            return f"{self.title} for solo {self.instruments[0]}"
        else:
            return f"{self.title} for {len(self.instruments)} instruments"


    def _get_instrument_list(self) -> list:
        return list(self.tracks.keys())


    def is_picked(self, instr: str) -> bool:
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
                 f"tempo: {self.tempo}" \
                 f"composer: {self.composer}" \
                 f"duration: {self.duration()}" \
                 f"\nmidi file: {self.midi_file_name}" \
                 f"text file: {self.txt_file_name}"
        print(output)


    def _duration(self) -> float:
        """
        gets the max duration from the dictionary of tracks
        """
        longest = 0.0
        for track in self.tracks:
            dur = 0.0
            for obj in self.tracks[track]:
                dur += obj.duration()
            if dur > longest:
                longest = dur
        return longest


    def duration(self) -> str:
        """
        returns the compositions' duration as a formatted string
        """
        minutes, seconds = divmod(self._duration(), 60)
        return str(int(minutes)) + " min " + str(seconds) + " sec "
