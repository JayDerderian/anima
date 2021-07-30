#*************************************************************************************#
#---------------------------This class handles melody data----------------------------#
#*************************************************************************************#


class melody():
    '''
    A class/container for managing all data relevant to melodies. This contains a 
    list for notes, rhythms, and dynamics, and their respective setters and getters.

    Stores: tempo, instrument, generation method, original Forte number(if applicable), 
    inputted source data, notes, rhythms, and dynamics.
    '''

    # Constructor
    def __init__(self):
            
        # Meta-data
        self.genMethod = ""
        self.fn = []
        self.sourceData = []
        self.sourceScale = []

        # Data
        self.tempo = 0.0
        self.instrument = ""
        self.notes = []
        self.rhythms = []
        self.dynamics = []

    # Check if there's complete melody data
    def hasData(self):
        '''
        Is there complete melody data? 
        If True, all data fields have been used.
        '''
        if(self.tempo != 0.0
            and self.instrument != ""
            and len(self.sourceData) > 0 
            and len(self.notes) > 0
            and len(self.rhythms) > 0
            and len(self.dynamics) > 0
            and len(self.sourceData) > 0):
            return True
        else:
            if(self.tempo == 0.0):
                print("\nmelody() - ERROR: no tempo inputted!")
            elif(self.instrument == ""):
                print("\nmelody() - ERROR: no instrument selected!")
            elif(len(self.sourceData) == 0):
                print("\nmelody() - ERROR: no source data inputted!")
            elif(len(self.notes) == 0):
                print("\nmelody() - ERROR: no notes inputted!")
            elif(len(self.rhythms) == 0):
                print("\nmelody() - ERROR: no rhythms inputted!")
            elif(len(self.dynamics) == 0):
                print("\nmelody() - ERROR: no dynamics inputted!")
            return False