'''
this module handles the analysis of composition() objects and
MIDI files. 

comp object analysis:
    - get all PC's from each part
    - count all PCS
    - find most common pitch classes
    - match PCS against sets and scales

    - convert given rhythms to base rhythms (RHYTHMS),
    - and create a rhythm analysis

    - list source data

'''

from utils.tools import removeoct
from core.constants import NOTES, PITCH_CLASSES, RHYTHMS

class Analyze:
    '''
    class of analysis functions to be used with composition() and MidiFile()
    objects.
    '''
    def __init__(self) -> None:
        pass

    def getpcs(self, comp):
        '''
        gets all pitch classes from each part in a composition() object
        '''
        pcs = []
        if len(comp.melodies) > 0:
            ml = len(comp.melodies)
            for m in range(ml):
                pcs.extend(self._getpcs(comp.melodies[m].notes))
            return pcs
        elif len(comp.chords) > 0:
            pcs = []
            cl = len(comp.chords)
            for c in range(cl):
                chords = comp.chords[c]
                chrdlen = len(chords)
                for chrd in range(chrdlen):
                    pcs.extend(self._getpcs(chords[chrd].notes))
            return pcs
        elif len(comp.melodichords) > 0:
            ml_len = len(comp.melodichords)
            for m in range(ml_len):
                pcs.extend(self._getpcs(comp.melodichords[m].notes))
        return pcs


    def _getpcs(self, notes):
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
        ind = self._getindex(notes)
        ind_len = len(ind)
        for n in range(1, ind_len):
            intrvls.append(ind[n]-ind[n-1])
        return intrvls


    def _getindex(self, notes):
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
    

    def checkrange(self, notes:list[str], ran:list[str]):
        '''
        checks for and removes and removes any notes
        not within the range of a given instrument.

        returns a modified note list[str]
        '''
        diff = self.get_diff(notes, ran)
        if len(diff) > 0:
            difflen = len(diff)
            for note in range(difflen):
                notes.remove(diff[note])
        return notes


    def get_diff(self, notes, ran):
        '''removes notes not in range of a given instrument with a provided range'''
        return [notes for notes in notes + ran if notes not in notes or notes not in ran]


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
    def new_12tone_matrix(self, row, intrvls):
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
    def MIDI_num_to_note_name(self, midi_notes):
        '''
        returns the corresponding MIDI note for a 
        given note name string. apparently MIDI note numbers
        are the given index of a note in NOTES plus 21
        '''
        if type(midi_notes) == list:
            notes = []
            for n in range(midi_notes):
                notes.append(NOTES.index(midi_notes[n])-21)
            return notes
        elif type(midi_notes) == int:
            return NOTES.index(midi_notes)-21
        else:
            raise TypeError("midi_notes must be a list or single int! type is:", type(midi_notes))