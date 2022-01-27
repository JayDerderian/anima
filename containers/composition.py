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

        self.midi_file_name = ""            # midi file name
        self.txt_file_name = ""             # text file name

        if tempo != None:                   # global tempo
            self.tempo = tempo
        else:
            self.tempo = 60.0

        self.ensemble = ""                  # "trio," "duet", etc.. 
        self.mode = "None"                  # mode used in composition, if any
        self.instruments = []               # list of all instruments in the piece
        self.bars = []                      # list of Bar() objects
        self.melodies = []                  # list of Melody() objects
        self.chords = {}                    # dictionary of Chord() objects or lists of Chord() objects
        self.melodichords = {}              # dictionary of alternating Melody() and Chord() object lists 
                                            # for instruments that can play both (like a piano, guitar, etc...)
        self.percussion = []                # list of percussion instruments

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

    # get info about composition
    def get_info(self):
        '''
        Returns a dictionary with the title, composer, duration, midi and txt file names
        '''
        return {"Title": self.title, "Composer": self.composer, "Ensemble": self.ensemble,
                "Instruments": self.instruments, "Duration": self.duration(), 
                "MIDI file": self.midi_file_name, "Text File": self.txt_file_name}

    # display info
    def display(self):
        '''
        display composition info
        '''
        print("\ntitle:", self.title)
        print("tempo:", self.tempo)
        print("composer:", self.composer)
        print("date:", self.date)
        print("duration:", self.duration())
        print("\nmidi file:", self.midi_file_name)
        print("txt file:", self.txt_file_name)

    # Get duration of composition
    def _duration(self):
        '''
        Returns the duration of a composition in seconds
        as a float, which should ideally be passed to duration_str(). 

        Finds the longest melody duration, the longest chord 
        progression duration, and the longest melodichord duration,
        compares them then returns the largest of the three. 
        '''
        ml = 0.0
        cl = 0.0
        mlcl = 0.0
        longest = 0.0
        if len(self.melodies) > 0:
            mlen = len(self.melodies)
            for m in range(mlen):
                ml = self.melodies[m].duration()
                if ml > longest:
                    longest = ml
        if len(self.chords) > 0:
            clen = len(self.chords)
            for prog in range(clen):
                cds = self.chords[prog]
                cdslen = len(cds)
                for chord in range(cdslen):
                    cl += cds[chord].rhythm
                if cl > longest:
                    longest = cl
        if len(self.melodichords) > 0:
            mclen = len(self.melodichords)
            for item in range(mclen):
                if isinstance(self.melodichords[item], Melody):
                    mlcl += self.melodichords[item].duration()
                elif isinstance(self.melodichords[item], Chord):
                    mlcl += self.melodichords[item].rhythm
                if mlcl > longest:
                    longest = mlcl
        return longest
    
    def duration(self):
        '''
        returns the compositions duration as a formatted string
        '''
        min, sec = divmod(self._duration(), 60)
        return str(int(min)) + " min " + str(sec) + " sec "