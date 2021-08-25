'''
Module for the Melody() class/container. Used for individual melody data in compositions.
'''

class Melody():
    '''
    A class/container for managing all data relevant to melodies. 

    Stores: original Forte number, inputted source data, original source scale, 
    tempo, instrument, notes, rhythms, and dynamics.
    '''

    # Constructor
    def __init__(self):
            
        # Meta-data
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
        NOTE: doesn't include meta-data! 
        '''
        if(self.tempo != 0.0
            and self.instrument != ""
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
            elif(len(self.notes) == 0):
                print("\nmelody() - ERROR: no notes inputted!")
            elif(len(self.rhythms) == 0):
                print("\nmelody() - ERROR: no rhythms inputted!")
            elif(len(self.dynamics) == 0):
                print("\nmelody() - ERROR: no dynamics inputted!")
            return False
    
    # Adjust for given tempo when calculating composition duration
    def tempoAdjust(self, rhythms):
        '''
        Alters given list[float] or single float against self.tempo 
        '''
        diff = 60/self.tempo
        if type(rhythms) == float:
            rhythms *= diff
        elif type(rhythms) == list:
            for i in range(len(rhythms)-1):
                rhythms[i] *= diff
        return rhythms 

    # get duration of melody
    def duration(self):
        '''
        Returns duration (float) of melody by adding together 
        rhythmic values (in seconds)
        '''
        dur = 0.0
        # make a copy to avoid modifying original values
        rhythms = self.rhythms
        # adjust against tempo accordingly
        if self.tempo != 60.0:
            rhythms = self.tempoAdjust(rhythms)
        for i in range(len(rhythms)):
            dur += rhythms[i]
        return dur