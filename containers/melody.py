"""
Module for the Melody() class/container. Used for individual melody data in compositions.

TODO: create a method to break generated Melody() data into a list of Bar() objects, with
      or without a common time signature. Tempo should be global.

NOTE: one possible way to use melody objects would be to make sure that whatever length you want
      is adherent to a consistent meter by checking whether the total length is a modulo of a given beat division

      if we want a piece to be in all 4/4, then the length of the melody should me mel.duration() % 4 == 0.
"""

class Melody:
    """
    A class/container for managing all data relevant to melodies.

    Does not adhere to any strict time signature. Use Bar() if using a
    time signature is preferred.

    Stores: original Forte number, inputted source data, original source scale,
    tempo, instrument, notes, rhythms, and dynamics.
    """

    def __init__(self, tempo=None, instrument=None):
            
        # Meta data
        self.info = 'None'
        self.pcs = []
        self.source_data = []
        self.source_scale = []

        if tempo is None:
            self.tempo = 0.0
        else:
            self.tempo = tempo
        if instrument is None:
            self.instrument = 'None'
        else:
            self.instrument = instrument

        self.notes = []
        self.rhythms = []
        self.dynamics = []


    def duration(self) -> float:
        """
        Returns the duration (float) of a melody in seconds.
        """
        dur = 0.0
        for rhy in self.rhythms:
            dur += rhy
        return dur

    def is_empty(self) -> bool:
        """
        Returns true if the container is empty, otherwise false
        """
        if len(self.notes) == 0 and len(self.rhythms) == 0 and len(self.dynamics) == 0:
            return True
        return False

    def get_meta_data(self) -> dict:
        """
        returns meta-data as a dictionary
        """
        return {
            "Info": self.info,
            "PCS": self.pcs,
            "Source Data": self.source_data,
            "Source Scale": self.source_scale
        }
    
    def get_pcs(self) -> list:
        """
        return a list[int] of all pitch classes in this melody.

        NOTE: may need to use tools.get_pcs() prior to calling this
        """
        return self.pcs if len(self.pcs) != 0 else [0]