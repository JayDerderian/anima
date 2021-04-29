#*************************************************************************************#
#---------------------------This class handles melody data----------------------------#
#*************************************************************************************#


class melody():
    '''
    A class/container for managing all data relevant to melodies. This contains a 
    list for notes, rhythms, and dynamics, and their respective setters and getters.
    '''

    # Constructor
    def __init__(self):
            
        # Data
        self.tempo = 0.0
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
            and len(self.notes) > 0
            and len(self.rhythms) > 0
            and len(self.dynamics) > 0):
            return True
        return False

    #---------------------------Input all data-----------------------------#

    def inputAll(self, newNotes, newRhythms, newDynamics, newTempo):    
        if(newNotes and newRhythms and newDynamics and newTempo):
            self.tempo = newTempo
            for i in range(len(newRhythms)):
                self.notes.append(newNotes[i])
                self.rhythms.append(newRhythms[i])
                self.dynamics.append(newDynamics[i])
        if(self.isEmpty() == False):    
            return 0
        else:
            return -1
