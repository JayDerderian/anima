#*******************************************************************************************#
#-------------------------------This class composition data---------------------------------#
#*******************************************************************************************#

class composition():
    '''
    This is a container for all things related to a stand-alone music composition. Data includes
    a global tempo, the piece's title, an array of melody() objects, and an array of chord() objects.
    '''
    # Constructor
    def __init__(self):

        # Title
        self.title = ""
        # File name for associated .txt file. May need to store
        # individual user's file path here?
        self.fileName = ""
        # Original inputted data (array of ints, floats, chars, or str copy
        # of hex number) for each melody() object.
        self.sourceData = []
        '''
        NOTE: Need a way to generate a single instrument list from the
        melodies and chord lists. Both object list elements are considered
        individual instruments.  
        '''
        # Global tempo (float)
        self.tempo = 0.0
        # List of instruments (strings)
        self.instruments = []
        # List of melody() objects. 
        self.melodies = []
        # List of chord() objects. 
        self.chords = []
    
    # Check if there's data in this instance
    def hasData(self):
        '''
        Check if this composition has all required data:

        -Title (string)
        -File name (string)
        -Original source data (int or char list)
        -Global tempo (float)
        -List of melodies (melody() objects)
        -List of harmonies (chord() objects)
        '''
        if(self.title != "" and
            self.fileName != "" and
            self.tempo != 0.0 and
            len(self.sourceData) != 0 and
            len(self.instruments) != 0 and
            len(self.melodies) != 0 and 
            len(self.chords) != 0):
            return True
        else:
            if(self.title == ""):
                print("\ncomposition() - ERROR: no title inputted!")
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