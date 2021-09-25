'''
Module for the Melody() class/container. Used for individual melody data in compositions.
'''

class Melody():
    '''
    A class/container for managing all data relevant to melodies. 

    Stores: original Forte number, inputted source data, original source scale, 
    tempo, instrument, notes, rhythms, and dynamics.
    '''

    def __init__(self, tempo=None, instrument=None):
            
        # Meta-data
        self.info = 'None'
        self.pcs = []
        self.sourceData = 'None'
        self.sourceScale = 'None'

        # Data
        if tempo is None and instrument is None:
            self.tempo = 0.0
            self.instrument = 'None'
        else:
            self.tempo = tempo
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