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

    # Check if there's *any* data
    def anyData(self):
        '''
        Are *any* of the fields used?
        '''
        if(self.tempo != 0.0
            or len(self.notes) != 0
            or self.rhythm != 0.0
            or len(self.dynamics) != 0):
            return True
        return False

    # Check if there's *complete* data
    def hasData(self):
        '''
        Is there *complete* chord data? 
        If True, then all fields have been used.
        '''
        if(self.tempo != 0.0
            and len(self.notes) != 0
            and self.rhythm != 0.0
            and len(self.dynamics) != 0):
            return True
        return False
    
    # Remove all data
    def erase(self):
        '''
        Erase *all* chord data. Returns True if succesfull. 
        '''
        if(self.anyData() == True):
            self.tempo = 0.0
            self.notes.clear()
            self.rhythm = 0.0
            self.dynamics.clear()
            return True
        # Make sure it actually worked
        if(self.anyData() == True):
            print("\nchord().erase - ERROR: unable to erase all data!")
            return False
        else:
            return True