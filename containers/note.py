#**********************************************************************************************#
#---------------------------This class handles individual note data----------------------------#
#**********************************************************************************************#

from core.constants import DYNAMICS, NOTES, RHYTHMS
from utils.tools import scaletotempo

class Note():
    '''
    A class/container for managing all data relevant to individual notes:
    name (string, i.e. "C#2"), duration (float: seconds), and dynamics (int: MIDI velocity)
    '''

    def __init__(self):

        # data
        self.instrument = ""
        self.tempo = 0.0
        self.name = ""
        self.rhythm = 0.0
        self.dynamic = 0
    
    # setters n' getters
    def get_info(self):
        '''returns a dictionary containing all info about this note'''
        return {"Instrument": self.instrument, "Tempo": self.tempo, 
                "Name": self.name, "Rhythm": self.rhythm, "Dynamic": self.dynamic}

    def change_note_name(self, note:str):
        '''change the name of the note'''
        if note in NOTES:
            self.note = note
        else:
            raise ValueError("not a valid note!")

    def change_dynamic(self, dyn:int):
        '''change the dynamic of this note'''
        if dyn in DYNAMICS:
            self.dynamic = dyn
        else:
            raise ValueError("not a valid dynamic!")
    
    def change_rhythm(self, rhy:float):
        '''change the rhythm of this note'''
        if scaletotempo(self.tempo, rhy, revert=True) in RHYTHMS:
            self.rhythm = rhy
        else:
            raise ValueError("rhythm not found in constants!")