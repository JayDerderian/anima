"""
This module contains the Chord() class, used to contain information unique to Chord() objects.
"""

from containers.container import Container
from core.constants import INSTRUMENTS


class Chord(Container):
    """
    A class/container for managing all data relevant to a single chord.

    This contains the tempo (float: BPM), a list for notes (strings: i.e. "C#2"),
    a rhythm (float: duration in seconds), and list for dynamics (int: MIDI velocity numbers).
    """

    def __init__(self, instrument=None, tempo=None):
        """
        Initialize with several empty lists. Use any inputted instrument or tempo data!
        """
        super().__init__()

        if instrument is None:
            self.instrument = "Acoustic Grand Piano"
        elif instrument in INSTRUMENTS:
            self.instrument = instrument
        else:
            raise ValueError(f"{instrument} is not a valid instrument!")
        if tempo is None:
            self.tempo = 60.0
        elif tempo < 40.0 or tempo > 280.0:
            raise ValueError(
                "tempo is out of range! "
                f"must be between 40.0 and 280.0. tempo supplied: {tempo}"
            )
        else:
            self.tempo = tempo

        self.notes = []
        self.rhythm = 0.0
        self.dynamic = 0.0

    def duration(self):
        """returns the assigned rhythm, which is in seconds adjusted for tempo (hopefully)"""
        return self.rhythm

    def get_meta_data(self):
        """returns meta-data as a dictionary"""
        return {
            "Info": self.info,
            "PCs": self.pcs,
            "Source Notes": self.source_notes,
            "Source Data": self.source_data,
        }
