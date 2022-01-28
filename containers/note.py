#**********************************************************************************************#
#---------------------------This class handles individual note data----------------------------#
#**********************************************************************************************#

from core.constants import DYNAMICS, NOTES, RHYTHMS
from utils.tools import scaletotempo

class Note():
    '''
    container for working with Instrument() objects, as well as Mido's
    MidiFile, and Track() objects
    '''

    def __init__(self, velocity, pitch, start, end):

        # data
        self.name = ''              # note name string ("C#4")
        self.velocity = velocity    # MIDI velocity 
        self.pitch = pitch          # MIDI pitch number
        self.start = start          # start time (float)
        self.end = end              # end time(float)
    
    
    def __repr__(self):
        return f'Note (pitch = {self.pitch}, start={self.start}), end={self.end}, velocity={self.velocity})'
        
    def duration(self):
        return self.end - self.start