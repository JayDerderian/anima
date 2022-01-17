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
        self.info = "None"
        self.pcs = []
        self.source_notes = []
        self.source_data = []
        
        # Data
        if instrument==None and tempo==None:
            self.instrument = ""
            self.tempo = 0.0
        else:
            self.instrument = instrument
            self.tempo = tempo
        
        self.notes = []
        self.rhythm = 0.0
        self.dynamic = 0.0

    # get duration
    def duration(self):
        '''returns the assigned rhythm, which is in seconds adjusted for tempo (hopefully)'''
        return self.rhythm 

    # get meta-data
    def get_meta_data(self):
        '''
        returns meta-data as a dictionary'''
        return {"Info": self.info, "PCs": self.pcs, "Source Notes": self.source_notes, "Source Data": self.source_data}

