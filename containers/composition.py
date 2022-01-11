'''
Module for handling all composition data. Contains a Composition() class/container. 
'''

class Composition():
    '''
    This is a container for all things related to a stand-alone music composition. 

    Title, composer, date of composition, MIDI file name, text file name, global tempo, 
    ensemble type, instrument list, list of picked instruments, lists melodies, and 
    a dictionary of chord progressions.
    '''
    # Constructor
    def __init__(self, title=None, composer=None, tempo=None):

        if title==None and composer==None:
            # Title
            self.title = title
            # Composer name
            self.composer = composer
        else:
            self.title = ""
            self.composer = ""
            
        # Date of composition
        self.date = ""

        # MIDI file name
        # NOTE: May need to store individual user's file path here?
        self.midi_file_name= ""
        # Text file name
        self.txt_file_name = ""

        # Global tempo (float)
        if tempo != None:
            self.tempo = tempo
        else:
            # Default tempo if none is provided
            self.tempo = 60.0

        # Ensemble size string ("duo", "trio", etc...)
        self.ensemble = ""
        # List of instruments
        self.instruments = []
        # List of melody() objects. Used for single-line instruments 
        self.melodies = []
        # List dictionary of chord() object lists (progressions). 
        # Key (int) functions as index. 
        self.chords = {}
        # List of both melody() and chord() objects (for pianos and guitars). better name forthcoming.
        self.melodichords = []


    # Has this instrument been picked?
    def is_picked(self, instr):
        '''
        Has this instrument been picked already? 
        '''
        return True if instr in self.instruments else False


    # Have all the instruments been picked?
    def all_picked(self, instruments):
        '''
        Have *all* the instruments been used? 
        Compares against an externally generated instrument list.
        '''
        return True if instruments==self.instruments else False

    # Get duration of composition
    def duration(self):
        '''
        Returns the duration of a composition in seconds.

        Finds the longest melody duration, the longest chord 
        progression duration, compares then returns the largest 
        of the two. 
        '''
        # get melody totals
        mlong = 0.0
        clong = 0.0
        ml = 0.0
        cl = 0.0
        if len(self.melodies) > 0:
            for m in range(len(self.melodies)):
                ml = self.melodies[m].duration()
                if ml > mlong:
                    mlong = ml
        # get chord totals
        if len(self.chords) > 0:
            for prog in range(len(self.chords)):
                c = self.chords[prog]
                # entries might be a list of chord() objects or
                # a single chord!
                if type(c) == list:
                    for chord in len(c):
                        cl = chord.rhythm
                    if cl > clong:
                        clong = cl
                else:
                    cl = c.rhythm
                    if cl > clong:
                        clong = cl
        return mlong if mlong > clong else clong