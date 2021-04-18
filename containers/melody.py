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
    def isEmpty(self):
        if(self.tempo != 0.0 
            and self.notes is not None 
            and self.rhythms is not None 
            and self.dynamics is not None):
            return False
        return True

    #---------------------------Input all data-----------------------------#

    def inputAll(self, newNotes, newRhythms, newDynamics, newTempo):    
        if(newNotes and newRhythms and newDynamics and newTempo):
            self.tempo = newTempo
            for i in range(len(newRhythms)):
                self.notes.append(newNotes[i])
                self.rhythms.append(newRhythms[i])
                self.dynamics.append(newDynamics[i])
        if(self.isEmpty() == False):    
            return True
        else:
            return False
                
                
    #-------------------------------Getters--------------------------------#

    def getNotes(self):
        if(self.notes is not None):
            myNotes = []
            for i in range(len(self.notes)):
                myNotes[i] = self.notes[i]
        else:
            return None
        if(myNotes is not None):
            return myNotes
        else:
            return None

    def getRhythms(self):
        if(self.rhythms is not None):
            myRhythms = []
            for i in range(len(self.rhythms)):
                myRhythms[i] = self.rhythms[i]
        else:
            return None
        if(myRhythms is not None):
            return myRhythms
        else:
            return None

    def getDynamics(self):
        if(self.dynamics is not None):
            myDynamics = []
            for i in range(len(self.dynamics)):
                myDynamics[i] = self.dynamics[i]
        else:
            return None
        if(myDynamics is not None):
            return myDynamics
        else:
            return None            