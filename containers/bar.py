'''
class/container for dealing with individual measures.
'''

from containers.melody import Melody

from core.analyze import Analyze
from core.constants import INSTRUMENTS

from utils.tools import scaletotempo


class Bar():
    '''
    class/container for dealing with individual measures.
    '''
    meter = ()                    # the meter of this bar
    tempo = 0.0                   # global composition tempo
    length = 0.0                  # length of bar in seconds using the meter
    current_beat = 0.0            # current UNUSED beat (in seconds)
    instrument = ""               # instrument assigned to this bar
    full = False                  # flag for indicating if this bar is full 
    bar = {                       # dictionary representing the current bar
        "Notes": [],            
        "Rhythms": [], 
        "Dynamics": []
    }
                     
                                   
    def __init__(self, meter=None, tempo=None, instrument=None):
        if meter==None:
            self.meter = (4,4)    # defaults to 4/4 if no meter is provided
        else:
            if Analyze.is_valid(meter):
                self.meter = (meter[0], meter[1])
            else:
                raise TypeError("invalid meter!")
        if tempo==None:           # defaults to 60bpm if none is provided
            self.tempo = 60.0
        else:
            if type(tempo) == float and tempo > 40 and tempo < 240:
                self.tempo = tempo
            else:
                raise TypeError(f"tempo must be a float, or is out of range! tempo supplied: {tempo}")
        
        # length (in seconds) = number of beats designated * counting rhythm (converted to seconds). 
        self.length = self.meter[0] * scaletotempo(self.tempo, self.meter[1])
        
        if instrument==None:
            self.instrument = 'Acoustic Grand Piano'
        elif instrument in INSTRUMENTS:
            self.instrument = instrument
        else:
            raise TypeError('Invalid instrument!')
    
    # see how much space is left in the bar. 
    def space_left(self):
        '''return the remaining time left in the bar in seconds'''
        return self.length - self.current_beat
    
    # clears all contained values to reuse this bar instance
    def clear(self):
        '''
        clears all fields
        '''
        self.meter = ()
        self.tempo = 0.0
        self.length = 0.0
        self.instrument = ''
        self.current_beat = 0.0
        self.bar["Notes"].clear()
        self.bar["Rhythms"].clear()
        self.bar["Dynamics"].clear()

    # gets the duration of the bar in seconds    
    def duration(self):
        '''
        gets the duration of the bar in seconds. 
        assumes supplied rhythms have already been scaled
        to the tempo

        NOTE: this might not equal self.length! this 
              could be a partially completed bar.
        '''
        if len(self.bar["Rhythms"]) == 0:
            return 0.0
        dur = 0.0
        for rhy in len(self.bar["Rhythms"]):
            dur += self.bar["Rhythms"][rhy]
        return dur

    # sets the meter for this measure
    def set_meter(self, meter):
        '''
        takes a supplied tuple and determines if it's a valid meter
        '''
        if type(meter) != tuple:
            raise TypeError("supplied meter was not a tuple! instead was:", type(meter))
        if Analyze.is_valid(meter):
            self.meter = (meter[0], meter[1])
        else:
            raise ValueError("invalid meter!")

    def add_notes(self, mel):
        '''
        Takes a Melody() object and adds notes rhythms and dynamics
        until either the bar is filled OR the last rhythm of the 
        Melody() object is too long to input. If this is the case, 
        then the last rhythm will have the remaining difference subtracted
        from its initial value. This is intended to handle syncopation.

        This basically assumes the note/rhythm/dynamic lists are of n length,
        and weren't concerned with fitting in any specific meter. Remaining 
        notes, rhythms, and dynamics are returned as a MODIFIED Melody() object!
        
        NOTE: if the last rhythm exceeds the total duration of the bar, the next 
        bar's notes (and the last one of the current bar) will be re-attacked since
        the split difference of the rhythm is only split between the two bars. 
        there currerntly isn't a way to "tie" the notes across the bars yet, and 
        MIDI doesn't care about bar lines anyways.
        '''

        self.tempo = mel.tempo
        self.instrument = mel.instrument

        while mel.is_empty() == False or self.full == False:

            self.current_beat += mel.rhythms[0]

            if self.current_beat < self.length:
                self.bar['Notes'].append(mel.notes[0])
                self.bar['Rhythms'].append(mel.rhythms[0])
                self.bar['Dynamics'].append(mel.dynamics[0])

                mel.notes.pop(mel.notes[0])
                mel.rhythms.pop(mel.rhythms[0])
                mel.dynamics.pop(mel.dynamics[0])

            elif self.current_beat >= self.length:
                diff = self.current_beat - self.length
                self.bar['Notes'].append(mel.notes[0])
                self.bar['Rhythms'].append((mel.rhythms[0] + self.current_beat) - diff )
                self.bar['Dynamics'].append(mel.dynamics[0])

                mel.rhythms[0] = diff
                self.full = True

        return mel