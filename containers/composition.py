#***************************************************************************************************#
#-------------------------------This class handles composition data---------------------------------#
#***************************************************************************************************#

class Composition():
    '''
    This is a container for all things related to a stand-alone music composition. Data includes
    a global tempo, the piece's title, an array of melody() objects representing each instruments part, 
    an array of chord() objects for harmony instruments, and other pretinant data about the piece.

    Title, composer, date of composition, file name, source data (if any), global tempo,
    instrument list, melodies, and harmonies.

    NOTE: Find a way to track if an instrument has been picked. Maybe picked list, and a corresponding
          search method. This will allow for more randomization in assigning instruments to various parts.
    '''
    # Constructor
    def __init__(self, title, composer, tempo):

        # Title
        self.title = title
        # Composer name
        self.composer = composer
        # Date of composition
        self.date = ""
        # MIDI file name
        # NOTE: May need to store individual user's file path here?
        self.midiFileName = ""
        # Text file name
        self.txtFileName = ""

        # Global tempo (float)
        self.tempo = tempo
        # Ensemble size string ("duo", "trio", etc...)
        self.ensemble = ""
        # List of instruments (strings)
        self.instruments = ""
        # List of picked instruments
        self.picked = []
        # List of melody() objects. 
        self.melodies = []
        # List of chord() objects. 
        self.chords = []
        # List of percussion() objects.
        self.percussion = []
    
    # Check if there's data in this instance
    def isComplete(self):
        '''
        Check if this composition has all required data:

        -Title (string)
        -File name (string)
        -Original source data (int or char list)
        -Global tempo (float)
        -List of melodies (melody() objects)
        -List of harmonies (chord() objects)
        '''
        if(self.title != "" 
            and self.composer != "" 
            and self.date != ""
            and self.fileName != ""
            and self.tempo != 0.0
            and len(self.sourceData) != 0
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
            elif(self.fileName == ""):
                print("\ncomposition() - ERROR: no file name inputted!")
            elif(self.tempo == 0.0):
                print("\ncomposition() - ERROR: no tempo inputted!")
            elif(len(self.sourceData) == 0):
                print("\ncomposition() - ERROR: no source data inputted!")
            elif(len(self.instruments) == 0):
                print("\ncomposition() - ERROR: no instruments inputted!")
            elif(len(self.melodies) == 0):
                print("\ncomposition() - ERROR: no melodies inputted!")
            elif(len(self.chords) == 0):
                print("\ncomposition() - ERROR: no harmonies inputted!")
            return False
        