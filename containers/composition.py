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

    def __init__(self, title=None, composer=None, tempo=None):

        if title==None and composer==None:  # title and composer
            self.title = title
            self.composer = composer
        else:
            self.title = ""
            self.composer = ""
            
        self.date = ""                      # date

        self.midi_file_name= ""             # midi file name
        self.txt_file_name = ""             # text file name

        if tempo != None:                   # global tempo
            self.tempo = tempo
        else:
            self.tempo = 60.0

        self.ensemble = ""                  # "trio," "duet", etc.. 
        self.instruments = []               # list of all instruments in the piece
        self.melodies = []                  # list of Melody() objects
        self.chords = {}                    # dictionary of Chord() object lists
        self.melodichords = []              # list of alternating Melody() and Chord() objects


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