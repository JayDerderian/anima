"""
a class/container for note information. this is mostly intended to work within
the midi.py module
"""


class Note:
    """
    Container for working with Instrument() objects, as well as Mido's
    MidiFile and Track() objects
    """

    def __init__(self, velocity, pitch, start, end):
        self.name = ''  # note name string ("C#4")
        self.velocity = velocity  # MIDI velocity
        self.pitch = pitch  # MIDI pitch number
        self.start = start  # start time (float)
        self.end = end  # end time(float)

    def __repr__(self):
        return f'Note (pitch = {self.pitch}, start={self.start}), ' \
               f'end={self.end}, velocity={self.velocity})'

    def duration(self):
        return self.end - self.start
