'''
Module for the Melody() class/container. Used for individual melody data in compositions.

TODO: create a method to break generated Melody() data into a list of Bar() objects, with 
      or without a common time signature. Tempo should be global.
'''

class Melody():
    '''
    A class/container for managing all data relevant to melodies. 

    Does not adhere to any strict time signature. Use Bar() if using a 
    time signature is preferred.

    Stores: original Forte number, inputted source data, original source scale, 
    tempo, instrument, notes, rhythms, and dynamics.
    '''

    def __init__(self, tempo=None, instrument=None):
            
        # Meta data
        self.info = 'None'
        self.pcs = []
        self.source_data = []
        self.source_scale = []

        # Data
        if tempo==None:
            self.tempo = 0.0
        else:
            self.tempo = tempo
        if instrument==None:
            self.instrument = 'None'
        else:
            self.instrument = instrument
        self.notes = []
        self.rhythms = []
        self.dynamics = []


    # Get duration of melody
    def duration(self):
        '''
        Returns the duration (float) of a melody in seconds.
        '''
        dur = 0.0
        for i in range(len(self.rhythms)):
            dur += self.rhythms[i]
        return dur

    # Get meta-data
    def get_meta_data(self):
        '''
        returns meta-data as a dictionary
        '''
        return {"Info": self.info, "PCS": self.pcs, "Source Data": self.source_data, "Source Scale": self.source_scale}
    
    # get pitch classes
    def get_pcs(self):
        '''
        return a list[int] of all pitch classes in this melody. may need to use tools.getpcs() prior
        to calling this
        '''
        return self.pcs if len(self.pcs) != 0 else [0]