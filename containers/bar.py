"""
class/container for dealing with individual measures.
"""

from containers.container import Container
from containers.melody import Melody

from core.analyze import Analyze, is_valid
from core.constants import INSTRUMENTS

from utils.tools import scale_to_tempo


class Bar(Container):
    """
    class/container for dealing with individual measures.
    """

    meter = ()  # the meter of this bar
    tempo = 0.0  # global composition tempo
    length = 0.0  # length of bar in seconds using the meter
    current_beat = 0.0  # current UNUSED beat (in seconds)
    instrument = ""  # instrument assigned to this bar
    full = False  # flag for indicating if this bar is full
    bar = {  # dictionary representing the current bar
        "Notes": [],
        "Rhythms": [],
        "Dynamics": [],
    }

    def __init__(self, meter=None, tempo=None, instrument=None):

        super().__init__()

        if meter is None:
            self.meter = (4, 4)  # defaults to 4/4 if no meter is provided
        else:
            if is_valid(meter):
                self.meter = (meter[0], meter[1])
            else:
                raise TypeError("invalid meter!")
        if tempo is None:  # defaults to 60bpm if none is provided
            self.tempo = 60.0
        else:
            if type(tempo) == float and 40 < tempo < 240:
                self.tempo = tempo
            else:
                raise TypeError(
                    f"tempo must be a float, or is out of range! tempo supplied: {tempo}"
                )

        # length (in seconds) = number of beats designated * counting rhythm (converted to seconds).
        self.length = self.meter[0] * scale_to_tempo(
            tempo=self.tempo, rhythms=self.meter[1]
        )
        # defaults to acoustic grand piano if no instrument is provided
        if instrument is None:
            self.instrument = "Acoustic Grand Piano"
        elif instrument in INSTRUMENTS:
            self.instrument = instrument
        else:
            raise TypeError(
                "Unsupported instrument! "
                "Can only use MIDI supported instruments for the moment :("
            )

    def space_left(self) -> float:
        """return the remaining time left in the bar in seconds"""
        return self.length - self.current_beat

    def clear(self) -> None:
        """
        clears all fields
        """
        self.meter = ()
        self.tempo = 0.0
        self.length = 0.0
        self.instrument = ""
        self.current_beat = 0.0
        self.bar["Notes"].clear()
        self.bar["Rhythms"].clear()
        self.bar["Dynamics"].clear()

    def duration(self) -> float:
        """
        gets the duration of the bar in seconds.
        assumes supplied rhythms have already been scaled
        to the tempo

        NOTE: this might not equal self.Length! this
              could be a partially completed bar.
        """
        if len(self.bar["Rhythms"]) == 0:
            return 0.0
        duration = sum(self.bar["Rhythms"])
        assert duration <= self.length, (
            f"calculated duration exceeds estimated length! "
            f"duration: {duration}"
            f"length: {self.length}"
        )
        return duration

    def set_meter(self, meter: tuple):
        """
        takes a supplied tuple and determines if it's a valid meter
        """
        if type(meter) != tuple:
            raise TypeError(
                "supplied meter was not a tuple! " "instead was:", type(meter)
            )
        if is_valid(meter):
            self.meter = (meter[0], meter[1])
        else:
            raise ValueError("invalid meter!")

    # TODO: test this
    def add_notes(self, mel: Melody) -> Melody:
        """
        Takes a Melody() object and adds notes, rhythms, and dynamics
        until either the bar is filled, the melody object is empty,
        OR the last rhythm of the Melody() object is too long to input.
        If this last part is the case, then the last rhythm will have the
        remaining difference subtracted from its initial value.
        This is intended to handle syncopation.

        This basically assumes the note/rhythm/dynamic lists are of n length,
        and weren't concerned with fitting in any specific meter. Remaining
        notes, rhythms, and dynamics are returned as a MODIFIED Melody() object!

        NOTE: if the last rhythm exceeds the total duration of the bar, the next
        bar's notes (and the last one of the current bar) will be re-attacked since
        the split difference of the rhythm is only split between the two bars.
        there currently isn't a way to "tie" the notes across the bars yet, and
        MIDI doesn't care about bar lines anyway.
        """

        self.tempo = mel.tempo
        self.instrument = mel.instrument

        while not mel.is_empty() or not self.full:
            # we're only ever accessing the first element of
            # each the melody objects lists since we're popping the first
            # element with each input. every sequential element will become
            # the first with each iteration.
            self.current_beat += mel.rhythms[0]
            # we're modifying the melody object in place here.
            # this will gradually shrink each of the lists.
            if self.current_beat < self.length:
                self.bar["Notes"].append(mel.notes.pop(mel.notes[0]))
                self.bar["Rhythms"].append(mel.rhythms.pop(mel.rhythms[0]))
                self.bar["Dynamics"].append(mel.dynamics.pop(mel.dynamics[0]))
            # this rhythm will cause us to exceed the length of the bar.
            # we need to add the last notes and chop off the difference from
            # the rhythm to fill the gap. we also don't want to remove the
            # elements since we'll need them in the next bar!
            elif self.current_beat >= self.length:
                diff = self.current_beat - self.length
                self.bar["Notes"].append(mel.notes[0])
                self.bar["Rhythms"].append((mel.rhythms[0] + self.current_beat) - diff)
                self.bar["Dynamics"].append(mel.dynamics[0])

                mel.rhythms[0] = diff
                self.full = True

        return mel
