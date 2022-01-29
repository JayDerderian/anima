'''
this module handles the importing and analysis of MIDI files. 
this uses pretty_midi as the importing tool and mingus to help
analyze the note content.

this module also handles pitch class set analysis using recently-
generated Composition() objects. 

comp object analysis:
    - get all PC's from each part
    - find most common pitch classes
    - list source data


'''

from utils.midi import load
from utils.tools import removeoct
from core.constants import NOTES, PITCH_CLASSES

class Analyze:
    '''
    class of analysis functions to be used with composition() and MidiFile()
    objects.
    '''
    def __init__(self) -> None:
        pass

    def getpcs(notes):
        '''
        matches pitch strings to pitch class integers.
        
        returns the corresponding pcs list[int]. list is unsorted, that is,
        it's in the original order of the elements in the submitted notes list
        '''
        pcs = []
        if type(notes)==str:
            # check if there's an octave int present
            if notes.isalpha()==False:                
                note = removeoct(notes)
                pcs.append(PITCH_CLASSES.index(note))
            else:
                pcs.append(PITCH_CLASSES.index(notes))
        elif type(notes)==list:
            nl = len(notes)
            for n in range(nl):
                if notes[n].isalpha()==False:
                    note = removeoct(notes[n])
                    pcs.append(PITCH_CLASSES.index(note))
                else:
                    pcs.append(PITCH_CLASSES.index(notes[n]))
        return pcs


    def getintervals(self, notes):
        '''
        generates a list of intervals from a given melody.
        total intervals will be len(m.notes)-1.
        
        difference between index values with NOTES corresponds to distance
        in semi-tones!
        '''
        intrvls = []
        ind = self.getindex(notes)
        ind_len = len(ind)
        for n in range(1, ind_len):
            intrvls.append(ind[n]-ind[n-1])
        return intrvls

    def getindex(self, notes):
        '''
        gets the index or list of indicies of a given note or 
        list of notes in NOTES. 
        
        note name str must have an assigned octave between 0-8. 
        
        the returned list[int] should be used by transpose() with 
        octeq set to False. those resulting values should be mapped 
        back against NOTES to get octave-accurate transposed notes
        '''
        if type(notes)==str:
            return NOTES.index(notes)
        elif type(notes)==list:
            indicies = []
            l = len(notes)
            for n in range(l):
                indicies.append(NOTES.index(notes[n]))
            return indicies
        else:
            raise TypeError("notes must be a single str or list[str]! type is:", type(notes))
    

    def getrange(self, notes:list[str]):
        '''
        returns the lowest and highest note in a given set of notes
        in a tuple: (min, max)
        '''
        for note in notes:
            (min, max) = (10000, -1)
            n = NOTES.index(note)
            if n <  int(min):
                min = n
            elif n > int(max):
                max = n
        return (min, max)

    
    # Generates a 12-tone matrix from a given row
    def new_matrix(self, row, intrvls):
        '''
        NOTE: NOT READY

        Generates a 2-D array/12-tone matrix from a given pitch class set (pcs = list[int]). 
        Requires a list of 11 positive intervals between 1-11 ([1, 4, 2, 6]) to iterate off of.

        The matrix is generating by appending a transposition
        of the original row to each subsequent index. 
        All other information, such as retrogressions, inversions, and 
        retrogressions + inversions can found using some print tricks.

        Returns a 2-D matrix - 'm'

        ---------

        Print original row:        
            print(m[0])

        Print each row retrograde:
            for i in range(len(m[i])):
                retro = m[i]
                retro.reverse()
                print(retro)

        Print each row inversions (matrix column, top to bottom):
            for i in range(len(m))
                inv = [row[i] for row in m]
                print(inv)

        Print each row retrograde inversions (matrix column, bottom to top):
            for i in range(len(m))
                ret_inv = [row[i] for row in m]
                ret_inv[i].reverse()
                print(ret_inv)

        --------
        NOTE: maybe there's a way to poplulate the matrix using synxtax like this:
        arr = [[r]*cols]*rows, where r is a modified version (transposition) of the 
        original row. 
        
        rows and cols are declared as a tuple (rows, cols = (n, n) 
        where n is some int)
        '''
        m = [[]]
        # add original row to first matrix row
        m.append(row)
        for i in range(len(intrvls)):
            r = self.transpose(row, intrvls[i])
            print("\nadding P", intrvls[i], ":", r)
            m.insert(i, r)
        return m

    # display 12-tone matrix
    def print_matrix(self, matrix):
        '''
        Display a twelve-tone matrix (2D list)
        '''
        for x in matrix:
            for y in x:
                print(y, end = " ")
            print()
       

    # Returns a list of MIDI pitch numbers. 
    # Each index number functions as a tag to reference specific pitches in the file
    def get_notes(tune):
        '''
        gets notes from a given PrettyMidi() object
        '''
        notes = []  
        for instrument in tune.instruments:
            for note in instrument.notes:
                notes.append(note.pitch)
        return notes
        

    # Determines difference between given tempo and standard second 
    def tempo_difference(tune):
        second = 60
        tempo = tune.estimate_tempo()
        difference = second/tempo
        return difference

    # Get pretty_midi's estimated global tempo in bpm
    def get_tempo(thisTune):
        return thisTune.estimate_tempo()

    # Get pretty_midi's note start times
    def get_beats(tune):
        return tune.get_beats(start_time = 0.0)

    # Get pretty_midi's downbeat locations (tempo/time-sig changes)
    def get_down_beats(tune):
        return tune.get_downbeats()

        
    # Retrieves the interval vector for a given pitch class set
    '''
    Note:
        1. Input scale (array of integers of n length)
        2. Loop: subtract a[1] from a[n], a[2] - a[n],
            Store each result as a separate element in an interval list/array
        3. Count each value in the interval array; how many 1's, 2's, 3's, etc thru 6.  
    '''
    '''
    def get_vector(self, scale):
        print("\nRetrieving interval vector...")
        if(not scale):
            print("...No scale inputted!")
        i = 0
        vector = [6]
        intervals = self.countIntervals(scale)
        while(i < len(intervals)):
            if(intervals[i] == 1):
                vector[0] += 1 
            elif(intervals[i] == 2):
                vector[1] += 1
            elif(intervals[i] == 3): 
                vector[2] += 1
            elif(intervals[i] == 4):
                vector[3] += 1
            elif(intervals[i] == 5):
                vector[4] += 1
            elif(intervals[i] == 6):
                vector[5] += 1
            i += 1
        return vector
    '''