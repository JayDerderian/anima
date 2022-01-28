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

    def __init__(self, v, p, s, e):

        # data
        self.name = ''       # note name string ("C#4")
        self.velocity = v    # MIDI velocity 
        self.pitch = p       # MIDI pitch number
        self.start = s       # start time (float)
        self.end = e         # end time(float)
    
    
    def __repr__(self):
        return f'Note (pitch = {self.pitch}, start={self.start}), end={self.end}, velocity={self.velocity})'
        
    def duration(self):
        return self.end - self.start