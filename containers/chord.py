'''
This module contains the Chord() class, used to contain information unique to Chord() objects.
'''

class Chord():
    '''
    A class/container for managing all data relevant to a single chord. 
    
    This contains the tempo (float: BPM), a list for notes (strings: i.e. "C#2"),
    a rhythm (float: duration in seconds), and list for dynamics (int: MIDI velocity numbers).
    '''
    # Constructor
    def __init__(self, instrument=None, tempo=None):
        '''
        Initialize with several empty lists. Use any inputted instrument or tempo data!
        '''
        # Metadata
        self.sourceNotes = []
        self.fn = ""
        self.pcs = []

        # Data
        if instrument==None and tempo==None:
            self.instrument = ""
            self.tempo = 0.0
        else:
            self.instrument = instrument
            self.tempo = tempo
        
        self.notes = []
        self.rhythm = 0.0
        self.dynamics = []