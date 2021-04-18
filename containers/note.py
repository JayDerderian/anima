#**********************************************************************************************#
#---------------------------This class handles individual note data----------------------------#
#**********************************************************************************************#

class note():
    '''
    A class/container for managing all data relevant to individual notes:
    name (string, i.e. "C#2"), duration (float: seconds), and dynamics (int: MIDI velocity)
    '''
    #Constructor
    def __init__(self):
            
        #Data
        self.name = ""
        self.rhythm = 0.0
        self.dynamic = 0

    #Check if there's data
    def isEmpty(self):
        if(self.name == "" 
            or self.rhythm == 0.0
            or self.dynamic == 0):
            return True
        return False