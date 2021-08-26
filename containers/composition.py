'''
Module for handling all composition data. Contains a Composition() class/container. 
'''

class Composition():
    '''
    This is a container for all things related to a stand-alone music composition. Data includes
    a global tempo, the piece's title, an array of melody() objects representing each instruments part, 
    an dictionary of of chord() object lists for harmony instruments, and other pretinant data about the piece.

    Title, composer, date of composition, text file name, MIDI file name, source data (if any), global tempo,
    instrument list, melodies, and harmonies.

    NOTE: Find a way to track if an instrument has been picked. Maybe picked list, and a corresponding
          search method. This will allow for more randomization in assigning instruments to various parts.
    '''
    # Constructor
    def __init__(self, title=None, composer=None, tempo=None):

        if title is not None and composer is not None:
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
        self.midiFileName = ""
        # Text file name
        self.txtFileName = ""

        # Global tempo (float)
        if tempo is not None:
            self.tempo = tempo
        else:
            # Default tempo if none is provided
            self.tempo = 60.0

        # Ensemble size string ("duo", "trio", etc...)
        self.ensemble = ""
        # List of instruments (strings)
        self.instruments = []
        # List of picked instruments
        self.instr_used = []
        # List of melody() objects. 
        self.melodies = []
        # List dictionary of chord() object lists (progressions). 
        # Key (int) functions as index. 
        self.chords = {}
        # List of percussion() objects.
        self.percussion = []
    
    # Check if there's data in this instance
    def isComplete(self):
        '''
        Check if this composition has all required data:

        -Title (string)
        -Composer (string)
        -File name (string)
        -Tempo (float)
        -Original source data (int or char list)
        -Global tempo (float)
        -List of melodies (melody() objects)
        -List of harmonies (chord() objects)
        '''
        if(self.title != "" 
            and self.composer != "" 
            and self.date != ""
            and self.txtFileName != ""
            and self.midiFileName != ""
            and self.tempo != 0.0
            and len(self.instruments) != 0
            and len(self.melodies) != 0 
            and len(self.chords) != 0):
            return True
        else:
            if(self.title == ""):
                print("\ncomposition() - ERROR: no title inputted!")
            elif(self.composer == ""):
                print("\ncomposition() - ERROR: no composer info inputted!")
            elif(self.date == ""):
                print("\ncomposition() - ERROR: no date info inputted!")
            elif(self.midiFileName == ""):
                print("\ncomposition() - ERROR: no MIDI file name inputted!")
            elif(self.txtFileName == ""):
                print("\ncomposition() - ERROR: no .txt file name inputted!")
            elif(self.tempo == 0.0):
                print("\ncomposition() - ERROR: no tempo inputted!")
            elif(len(self.instruments) == 0):
                print("\ncomposition() - ERROR: no instruments inputted!")
            elif(len(self.melodies) == 0):
                print("\ncomposition() - ERROR: no melodies inputted!")
            elif(len(self.chords) == 0):
                print("\ncomposition() - ERROR: no harmonies inputted!")
            return False
        
    # Have all the instruments been picked?
    def allPicked(self):
        # NOTE: This returns sorted versions of original lists. Might affect how instruments are 
        # selected? 
        # if sorted(self.instruments) == sorted(self.instr_used):
        #     return True
        return sorted(self.instruments) == sorted(self.instr_used) if True else False

    # Has this instrument been picked?
    def isPicked(self, instr):
        for i in range(len(self.instr_used)):
            if instr == self.instr_used[i]:
                return True
        return False

    # Adjust for given tempo when calculating composition duration
    def tempoAdjust(self, rhythms):
        diff = 60/self.tempo
        if type(rhythms) == float:
            rhythms *= diff
        elif type(rhythms) == list:
            for i in range(len(rhythms)-1):
                rhythms[i] *= diff
        return rhythms    

    # Get duration of composition
    def duration(self):
        '''
        Returns length of composition by returning largest value of either melody
        list or chord prog dictionary. 
        
        Checks against self.tempo to ensure accurate values
        '''
        ml = 0.0
        cl = 0.0
        # get melody totals
        for i in range(len(self.melodies)):
            # make a copy to avoid altering original values
            rhythms = self.melodies[i].rhythms
            # adjust values if tempo isn't 60bpm
            if self.tempo != 60.0:
                rhythms = self.tempoAdjust(rhythms)
            for j in range(len(rhythms)):
                ml += rhythms[j]
        # get chord totals
        key = 1
        for i in range(len(self.chords)):
            # make a copy as to not modify original entries
            chords = self.chords[key]
            for j in range(len(chords)):
                if self.tempo != 60.0:
                    # make a copy as to not modify original entries
                    r = self.tempoAdjust(chords[j].rhythm)
                    cl += r
                else:
                    cl += chords[j].rhythm
            key +=1
        return ml if ml > cl else cl