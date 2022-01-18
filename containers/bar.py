'''
class/container for dealing with individual measures.
'''

from containers.melody import Melody
from utils.meter import is_valid
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
    bar = {"Notes":[],            # dictionary representing the current bar
           "Rhythms":[], 
           "Dynamics":[]
          }                      
                                   

    def __init__(self, meter=None, tempo=None, instrument=None):
        if meter==None:
            self.meter = (4,4)    # defaults to 4/4 if no meter is provided
        else:
            if type(meter) == tuple:
                self.meter = (meter[0], meter[1])
            else:
                raise TypeError("meter must be a tuple!")
        
        if tempo==None:
            self.bar["Tempo"] = 60.0
        else:
            if type(tempo) == float and tempo > 40 and tempo < 240:
                self.bar["Tempo"] = tempo
            else:
                raise TypeError("tempo must be a float, or is out of range!")
        
        self.length = self.meter[0] * scaletotempo(self.bar["Tempo"], self.meter[1])
        
        if instrument!=None:
            self.instrument = instrument
        else:
            self.instrument = 'Acoustic Grand Piano'

    # see if this bar is empty or not
    def is_empty(self):
        '''is this bar empty?'''
        return True if self.length == 0 else False
    
    # see how much space is left in the bar. 
    def space_left(self):
        '''return the remaining time left in the bar'''
        return self.length - self.current_beat
    
    # clears all contained values to reuse this bar instance
    def clear(self):
        '''
        clears all fields
        '''
        self.meter = ()
        self.tempo = 0.0
        self.length = 0.0
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
        if is_valid(meter):
            self.meter = (meter[0], meter[1])
        else:
            raise ValueError("invalid meter!")

    def add_notes(self, mel):
        '''
        takes a Melody() object or dictionary with "Notes", 
        "Rhythms", "Dynamics", and "Tempo" keys and adds all notes that can be 
        contained within this bar.

        this basically assumes the note/rhythm/dynamic lists are of n length,
        and weren't concerned with fitting in any specific meter. remaining 
        notes, rhythms, and dynamics are returned as a dictionary. 

        use this once with the initial Melody() object, then iterate through 
        the resulting dict until it's empty. one should also be able to switch
        the meter of each bar against whatever note/rhy/dyn lists you started with,
        assuming you'd want to switch it up as you go. 
        '''
        left_overs = {"Notes":[], "Rhythms": [], "Dynamics": []}

        # store initial lists in a temp dictionary  
        if isinstance(mel, Melody):
            # move things over to pull from and return after each added item is 
            # popped from the list
            left_overs["Notes"] = mel.notes
            left_overs["Rhythms"] = mel.rhythms
            left_overs["Dynamics"] = mel.dynamics

        elif type(mel)==dict:
            # move items over to pull from and return after each added item is 
            # popped from the list
            left_overs["Notes"] = mel["Notes"]
            left_overs["Rhythms"] = mel["Rhythms"]
            left_overs["Dynamics"] = mel["Dynamics"]

        # iterate through notes/rhythms/dynamics until we reach or exceed our 
        # limit
        l = len(left_overs["Notes"])
        for cur in range(l):
            self.bar["Notes"].append(left_overs["Notes"][cur])
            self.bar["Rhythms"].append(left_overs["Rhythms"][cur])
            self.bar["Dynamics"].append(left_overs["Dynamics"][cur])
            
            # pop current items from each list
            left_overs["Notes"].pop(left_overs["Notes"][cur])
            left_overs["Rhythms"].pop(left_overs["Rhythms"][cur])
            left_overs["Dynamics"].pop(left_overs["Dynamics"][cur])

            # current place in the bar. once we reach the total 
            self.current_beat += left_overs["Rhythms"][cur]
            # if we've reached or exceeded our length, end loop!
            if self.current_beat >= self.length:
                # get the extra difference and modify the
                # first element of the rhythms list to be this
                # value, so the total note duration isn't lost between
                # subsequent measures
                if self.current_beat > self.length:
                    left_overs["Rhythms"][0] = self.current_beat - self.length
                break
        
        # return remaining notes/rhy/dyn, or match against string to 
        # indicate you're done with all your lists.
        return left_overs if len(left_overs) > 0 else "Done!"
