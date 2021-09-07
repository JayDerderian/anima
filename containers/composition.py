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
        self.midiFileName = ""
        # Text file name
        self.txtFileName = ""

        # Global tempo (float)
        if tempo != None:
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
    

    # Check if there's data in this instance
    def isComplete(self):
        '''
        Check if this composition has all required data:

        -Title (str)
        -Composer (str)
        -Date (str)
        -MIDI File name (str)
        -Tempo (float)
        -Instruments (list[str])
        -Melodies (list[melody()])
        -Dictionary of harmonies (lists of chord() objects)
        '''
        if(self.title != "" 
            and self.composer != "" 
            and self.date != ""
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
            elif(self.tempo == 0.0):
                print("\ncomposition() - ERROR: no tempo inputted!")
            elif(len(self.instruments) == 0):
                print("\ncomposition() - ERROR: no instruments inputted!")
            elif(len(self.melodies) == 0):
                print("\ncomposition() - ERROR: no melodies inputted!")
            elif(len(self.chords) == 0):
                print("\ncomposition() - ERROR: no harmonies inputted!")
            return False

    # Has this instrument been picked?
    def isPicked(self, instr):
        '''
        Has this instrument been picked already? 
        '''
        return True if instr in self.instr_used else False


    # Have all the instruments been picked?
    def allPicked(self):
        '''
        Havel *all* the instruments been used?
        '''
        return True if self.instruments==self.instr_used else False

    # Get duration of composition
    def duration(self):
        '''
        Returns the duration of a composition in seconds. 
        '''
        ml = 0.0
        cl = 0.0
        # get melody totals
        if len(self.melodies) > 0:
            for m in range(len(self.melodies)):
                for rhythm in range(len(self.melodies[m].rhythms)):
                    ml += self.melodies[m].rhythms[rhythm]
        # get chord totals
        if len(self.chords) > 0:
            for c in range(len(self.chords)):
                chords = self.chords[c]
                for chord in range(len(chords)):
                    cl += chords[chord].rhythm
        return ml if ml > cl else cl