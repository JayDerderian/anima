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
        Returns length of composition by returning largest value of either melody
        list or chord prog dictionary. 
        
        Checks against self.tempo to ensure accurate rhytmic values.
        '''
        ml = 0.0
        cl = 0.0
        # get melody totals
        for i in range(len(self.melodies)):
            for j in range(len(self.melodies[i].rhythms)):
                ml += self.melodies[i].rhythms[j]
        # get chord totals
        for i in range(len(self.chords)):
            chords = self.chords[i]
            for j in range(len(chords)):
                cl += chords[j].rhythm
        return ml if ml > cl else cl