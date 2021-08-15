#************************************************************************************************************************#
#---------------------------------This class manages MIDI file analysis functions----------------------------------------#
#************************************************************************************************************************#
'''
Notes:


'''
import math
import pretty_midi as pm



#Retrieve MIDI note number
def getNoteNumber(self, thisTune):
    if(not thisTune):
        return 0
    #Test output
    print("\nMIDI note number: ", thisTune.instruments.Notes.pitch)
    return thisTune.instrument.note.pitch        

#Returns a list of MIDI pitch numbers. 
#Each index number functions as a tag to reference specific pitches in the file
def getNotes(self, thisTune):
    theNotes = []  
    print("\nGenerating MIDI note list...")
    for instrument in thisTune.instruments:
        for note in instrument.notes:
            theNotes.append(note.pitch)
    #Test output
    if(not theNotes):
        print("...Unable to generate note list!")
    print("...MIDI Note list created!")
    #print(theNotes)
    return theNotes

#Collects all data about each note (Note: velocity, pitch, start/end)
def getNoteData(self, thisTune):
    noteData = []
    print("\nCollecting note data...")
    for instrument in thisTune.instruments:
        noteData.append(instrument.notes)
    #Test output
    if(not noteData):
        print("...Unable to gather note data")
    print("...Retrieved note data!")
    #print(noteData)
    return noteData

#Get total number of notes in the MIDI file
def getTotalNotes(self, thisTune):
    noteCount = 0
    print("\nCounting notes...")
    for instrument in thisTune.instruments:
        for note in instrument.notes:
            noteCount += 1
    #Test output
    if(not noteCount):
        print("...Unable to complete note count!")
    print("Total Notes: ", noteCount)
    return noteCount

#Check for duplicate pitch classes in a tone row.
def duplicates(self, row):
    if(not row):
        print("...No row recieved!")
    result = []
    for i in row:
        if i not in row:
            result.append(i)
    return result
    
#Get total number of tracks/instruments
def getTotalInstruments(self, thisTune):
    totalInstruments = 0
    print("\nCounting instruments/tracks...")
    for instrument in thisTune.instruments:
        totalInstruments += 1
    #Test output
    if(totalInstruments == 0):
        print("No tracks found!")
    print("Total tracks: ", totalInstruments)
    return totalInstruments

#Determines difference between given tempo and standard second 
def tempoDifference(self, thisTune):
    second = 60
    tempo = thisTune.estimate_tempo()
    difference = second/tempo
    return difference

#Get pretty_midi's estimated global tempo in bpm
def getTempo(self, thisTune):
    tempo = thisTune.estimate_tempo()
    return tempo

#Get pretty_midi's note start times
def getBeats(self, thisTune):
    startTimes = thisTune.get_beats(start_time = 0.0)
    return startTimes

#Get pretty_midi's downbeat locations (tempo/time-sig changes)
def getDownBeats(self, thisTune):
    downBeats = thisTune.get_downbeats()
    return downBeats

#Gets note duration (in seconds)
def getDuration(self, start, end):
    return end - start

#Displays piano roll of MIDI data
def displayMIDIterminal(self):
    roll = pm.PrettyMIDI.get_piano_roll()
    print(roll)

#-----------------------------Composition analysis--------------------------------#    

# Generates a 12-tone matrix from a given row
def newMatrix(self, row, intrvls):
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
def printMatrix(self, matrix):
    '''
    Display a twelve-tone matrix (2D list)
    '''
    for x in matrix:
        for y in x:
            print(y, end = " ")
        print()
        
#Retrieves the interval vector for a given pitch class set
'''
Note:
    1. Input scale (array of integers of n length)
    2. Loop: subtract a[1] from a[n], a[2] - a[n],
        Store each result as a separate element in an interval list/array
    3. Count each value in the interval array; how many 1's, 2's, 3's, etc thru 6.  
'''
'''
def getVector(self, scale):
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

def countIntervals(self, scale):
    print("\nCounting intervals...")
    i = 0
    j = 0
    end = len(scale) - 1
    intervals = []
    vector = []
    for i in range(len(scale))
        intervals.append(scale[i] - scale[end])
    return intervals
'''

#Count intervals between notes
'''
Note: Need to find a way to retireve MIDI note number 
from thisTune

def findIntervals(self, thisTune, theNotes):
    if(not thisTune):
        return 0
    notes = []
    intervals = [6]
    print("\nCounting intervals...")
    for instrument in thisTune.instruments:
        for note in instrument.notes:
                

    ERROR - Exception has occurred: TypeError
    list indices must be integers or slices, not Note
    notes.append(pretty_midi.note_name_to_number) 
                            
    if(self.getInterval(notes[note] - notes[note-1]) == 1):
        intervals[0] += 1
    elif(self.getInterval(notes[note] - notes[note-1]) == 2):
        intervals[1] += 1
    elif(self.getInterval(notes[note] - notes[note-1]) == 3):
        intervals[2] += 1
    elif(self.getInterval(notes[note] - notes[note-1]) == 4):
        intervals[3] += 1
    elif(self.getInterval(notes[note] - notes[note-1]) == 5):
        intervals[4] += 1
    elif(self.getInterval(notes[note] - notes[note-1]) == 6):
        intervals[5] += 1

    if(not intervals):
        print("...No intervals found!")
    print("Interval list: ", intervals)
    return intervals
'''

