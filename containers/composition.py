'''
Module for handling all composition data. Contains a Composition() class/container. 
'''

from containers.chord import Chord
from containers.melody import Melody


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
        progression duration, and the longest melodichord duration,
        compares them then returns the largest of the three. 
        '''
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
        # get melodichord totals
        if len(self.melodichords) > 0:
            mclen = len(self.melodichords)
            for item in range(mclen):
                if isinstance(self.melodichords[item], Melody):
                    ml = self.melodichords[item].duration()
                    if ml > mlong:
                        mlong = ml
                elif isinstance(self.melodichords[item], Chord):
                    cl = self.melodichords[item].duration()
                    if cl > clong:
                        clong = cl

        return mlong if mlong > clong else clong
    
    def get_info(self):
        '''returns a dictionary with the title, composer, and duration'''
        return {"Title": self.title, "Composer": self.composer, "Duration": self.duration()}