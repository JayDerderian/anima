#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------

    ***SEE NOTES.DOCX for complete notes and ideas!!!!!****

    TODO: Add a rhythm converter function to translate durations in self.rhythms
          to actual value in seconds for that rhythm in a specified tempo. 
          ex: q = 60, quarter = 1 sec, q = 72, quarter = 0.83 seconds.

          diff = inputtedTempo/60
          newRhythms.append(inputtedRhythms[i] * diff)

    TODO: Modify functions to allow for a variable number of possible arguments!!! 
          For example, in newChord(), modify it to generate 2-9 notes in 
          random octaves *only if a specified octave isn't supplied by the user*. 

          ex new syntax: newChord(self, *argv). Only pick random octave if none is supplied. 
          
          ***This will allow for the consolidation of many methods!!!!*** 
          
          If I can modify one to allow for a variety of parameters. 
          All tertian/ quartal/quintal chord generation methods could be consolidated 
          provided one can use a singlevariable for the constant interval used to build the chords.

          ex: if(not *argv):
                  note = self.note()
              note = self.aNote(octave)


    TODO: Add error return codes to ALL functions for testing purposes. Write test program in testing.py to run in main 
          during development.

    TODO: Additional 'decisions' to add:

        Pick x number of "note structures" utilizing this root
            How many lists of notes/scales/chords?
            Of a a given set of scales, pick which scale to be a "primary" scale 
            to base note/chord structures off of

        Generate "central" scale (non-repeating list of integers in ascending order between 0 - 11, starting with 0.)
            Generate n number of pc prime forms ("chords") from "central" scale.
        
        Of a given scale, pick x number of sub-structures (sub-sets) of n - len(super-set) - 1.

        Of a given scale, pick which note of that scale to be the "tonal center"

        Pick x number of notes in a given list to form a "block"
            Pick x number of times to repeat this block
            Must be smaller set for minimalist mode

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
from random import randint
from midi import midiStuff as mid
from decisions import decide as choice
from containers.melody import melody
from containers.note import note

#Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms ranging from pure "random"
    selections (see PRNG info), to more strict instructions.  

    Parent class: choice
    '''

    #Constructor
    def __init__(self):


        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#


        # Alphabet to map letters to notes.
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u',
                         'v', 'w', 'x', 'y', 'z']


        #--------Notes and Scales--------#

        #Enharmonically spelled note names starting on A. Indicies: 0-16
        self.noteNames = ["A", "A#", "Bb", "B", 
                          "C", "C#", "Db", "D", 
                          "D#", "Eb", "E", "F", 
                          "F#", "Gb", "G", "G#",
                          "Ab"]

        # Major scale template. Use with noteNames and 
        # alter values to transpose (mod12) and modify
        self.defaultScale = ["C", "D", "E", "F", "G", "A", "B"]

        # Major scale in PC notation.
        self.majorScale = [0, 2, 4, 5, 7, 9, 11]

        # Natural minor scale in PC notation
        self.minorScale = [0, 2, 3, 5, 7, 8, 10]

        # Harmonic minor scale in PC notation
        self.harMinScale = [0, 2, 3, 5, 7, 8, 11]

        # Melodic minor scalale in PC notation
        self.melMinorScale = [0, 2, 3, 5, 7, 9, 11]

        # Chormatic scale (using all sharps). Indicies 0 - 11.
        self.chromaticScaleSharps = ["C", "C#", "D", "D#", "E", "F",
                                     "F#", "G", "G#", "A", "A#", "B"] 

        # Chormatic scale (using all flats). Indicies 0 - 11.
        self.chromaticScaleFlats = ["C", "Db", "D", "Eb", "E", "F",
                                    "Gb", "G", "Ab", "A", "Bb", "B"]        

        # Octave numbers
        self.octave = [1, 2, 3, 4, 5, 6, 7]


        # Major scales
        self.scales = {1: ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 
                       2: ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
                       3: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#' ],
                       4: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
                       5: ['E', 'F#', 'G#', 'A', 'B', 'C#', "D#"],
                       6: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
                       7: ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
                       8: ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                       9: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
                       10:['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                       11:['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
                       12:['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']}


        #-----------Interval Lists----------#
        '''
        Notes:

            Develop interval sets that begin with 2 and end with 2,
            making the next cycle of intervals begin on a tone a half
            step higher than originally.

            "Self-transposing interval sets"

            ex. 
                c, d, e, f#, g, a, bb, c,
                db, eb, f, g, ab, bB, cb, db,
                d, e, f#, g#, a, b, c, d ...ect.  
        '''

        #Major
        self.major = [2, 2, 1, 2, 2, 2, 1]

        #Natural minor
        self.natMinor = [2, 1, 2, 2, 1, 2, 2]

        #Melodic minor
        self.melMinor = [2, 1, 2, 2, 2, 2, 1]

        #Harmonic minor
        self.harMinor = [2, 1, 2, 2, 1, 3]

        #Whole tone
        self.wholeTone = [2, 2, 2, 2, 2]

        #Octatonic
        self.octatonic = [2, 1, 2, 1, 2, 1, 2]

        #Triads
        self.majorTriad = [4, 3]
        self.minorTriad = [3, 4]
        self.diminishedTriad = [3, 3]
        self.augmentedTriad = [4, 4]
        
        
        #-------------Rhythm--------------#
        '''
        Notes:

            Durations in seconds (1 = quarter note (60bpm))
            Whole note to 32nd note
            
                [0] 4 = whole note                                                          
                [1] 3 = dotted half
                [2] 2 = half note           
                [3] 1.5 = dotted quarter    
                [4] 1 = quarter             
                [5] 0.75 = dotted eighth
                [6] 0.5 = eighth
                [7] 0.375 = dotted sixteenth
                [8] 0.25 = sixteenth 
                [9] 0.125 = thirty-second

            Note: Add tuplets as other self.lists! Need triplets, quintuplets, septuplets,
            nonuplets, and..11-uplets.

        '''
        #Rhythms (0-9)
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 
                        0.375, 0.25, 0.125]

        #Fast rhythms (0-8)
        self.rhythmsFast = [0.375, 0.28125, 0.25, 0.1875, 0.125, 0.09375, 
                            0.0625, 0.046875, 0.03125]

        #Slow rhythms (0-7) - [n2 = n1 + (n1/2)]
        self.rhythmsSlow = [8.0, 12.0, 18.0, 27.0, 
                            40.5, 60.75, 91.125, 136.6875]
        

        #------------Chords-------------#

        #Major, minor, augmented, and diminished triads
        self.triads = {1: [0,4,7], 2: [0,3,7], 
                       3: [0,4,8], 4: [0,3,6]}
        
        #Diminished, augmented, quartal, quintal chords
        self.symChords = {1: [0,3,6], 2: [0,4,8],
                          3: [0,5,10], 4: [0,2,7]}
        
  
        #------------Tempo-------------#

        #Tempos (indices: 0-38)
        self.tempo = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0, #1-9 (0-8)
                      60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, #10-18 (9-17)
                      92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
                      126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, #28-36 (27-35)
                      184.0, 200.0, 208.0] #37-39 (36-38)


        #-----------Dynamics------------#
        '''
        Note: MIDI velocity/dynamics range: 0 - 127
        '''

        #Dynamics (0-26)
        self.dynamics = [20, 24, 28, 32, 36, 40, 44, 48, 52,
                         56, 60, 64, 68, 72, 76, 80, 84, 88,
                         92, 96, 100, 104, 108, 112, 116, 120, 124]

        #Soft dynamics (0-8)
        self.dynamicsSoft = [20, 24, 28, 32, 36, 40, 44, 48, 52]

        #Medium dynamics (0-8)
        self.dynamicsMed = [56, 60, 64, 68, 72, 76, 80, 84, 88]

        #Loud dynamics (0-8)
        self.dynamicsLoud = [92, 96, 100, 104, 108, 112, 116, 120, 124]



    #--------------------------------------------------------------------------------#
    #-----------------------------Misc. Utility Functions----------------------------#
    #--------------------------------------------------------------------------------#

    #Convert base rhythms to values in a specified tempo
    def tempoConvert(self, newMelody):
        '''
        A rhythm converter function to translate durations in self.rhythms
        to actual value in seconds for that rhythm in a specified tempo. 
        
        ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

        60/72 = .83 - The result becomes the converter value to multiply all supplied
        durations against to get the new tempo-accurate durations.

        '''
        if(not newMelody):
            return -1
        diff = 60/newMelody.tempo
        for i in range(len(newMelody.rhythms) - 1):
            newMelody.rhythms[i] *= diff
        return newMelody
        
    
    #Are we at the end?
    def isEnd(self, row, totalLen):
        '''
        Utility for double checking whether
        a row is as long as it needs to be.
        '''
        if(row is None
            or totalLen <=0):
            return -1
        elif(len(row) == totalLen):
            return True
        return False

    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''Converts an array of floats to an array of ints'''
        if(len(data) == 0):
            print("ERROR: no data inputted!")
            return -1
        result = []
        for i in range(len(data)):
            result.append(int(data[i]))
        return result

    # Scale individual data set integers such that i = i < len(dataSet) - 1
    def scaleTheScale(self, data):
        '''
        This repeatedly subtracts the value of len(data) - 2 from each integer in the 
        data array. This will keep the newly inputted data array's values within the bounds 
        of the scale array. These values function as a collection of index numbers 
        to randomly chose from in order to pick note strings from the scale array.

        len(data) - 1 acts as a way to do some modulo arithmatic whose base is
        a dynamically determined value.

        NOTE: Alternate version where highest numbers must be divisible by
        len(data) - 2. Trying to make this function like octave equivalance.

        while(data[i] % len(data) - 2 != 0):
            data[i] = math.floor(data[i] % len(data) - 2) 
        '''
        if(len(data) == 0):
            print("ERROR: no data inputted") 
            return -1
        newData = []
        for i in range(len(data) - 1):
            while(data[i] > len(data) - 2):
                data[i] -= len(data) - 2
            newData.append(data[i])
        return newData

    # Maps letters to index numbers
    def mapLettersToNumbers(self, letters):
        '''
        Maps letters to index numbers, which will then be 
        translated into notes (strings).
        '''
        print("\nMapping letters to index numbers...")
        if(len(letters) == 0): 
            print("ERROR: no data inputted!")
            return -1
        # Make all uppercase characters lowercase
        for i in range(len(letters) - 1):
            if(letters[i].isupper() == True):
                letters[i] = letters[i].lower()
        numbers = []
        # Pick a letter
        for i in range(len(letters)):
            # Search alphabet letter by letter
            for j in range(len(self.alphabet) - 1):
                # If we get a match, store that index number
                if(letters[i] == self.alphabet[j]):
                    numbers.append(j)
        if(len(numbers) == 0):
            print("ERROR: no index numbers found!")
            return -1
        return numbers
    
    # Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        if(len(scale) == 0):
            print("ERROR: no scale inputted!")
            return -1
        k = 5
        minorScale = []
        for i in range(len(scale)):
            minorScale.append(scale[k])
            k += 1
            if(k > len(scale) - 1):
                k = 0
        if(len(minorScale) == 0):
            print("ERROR: unable to generate minor scale!")
            return -1
        return minorScale
    
    # Convert a hex number representing a color to an array of integers
    def hexToIntArray(self, hex):
        '''
        Converts a prefixed hex number to an array of integers.

        Algorithm:
            1. Convert to integer
            2. Break single integer into array of individual integers (ex 108 to [1, 0, 8])
               using list comprehension
        '''
        if(hex == 0 or hex == None):
            print("ERROR: Invalid input!")
            return -1
        # Convert to int
        hexStr = int(hex, 0)
        # Convert to array of ints (ie. 132 -> [1, 3, 2])
        numArr = [int(x) for x in str(hexStr)]
        return numArr

    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    def newTempo(self):
        '''
        Picks tempo between 40-208bpm.
        Returns a float upon success, 60.0 if fail.
        '''
        tempo = 0.0
        tempo = self.tempo[randint(0, len(self.tempo) - 1)]
        if (not tempo):
            return 60.0
        return tempo


    #-------------------------------------------------------------------------------#
    #-------------------------------------Pitch-------------------------------------#
    #-------------------------------------------------------------------------------#


    #Picks a single note in a random octave
    def note(self):
        '''
        Returns a randomly chosen pitch in a randomly chosen octave (i.e. C#3)
        '''
        note = self.numToNote(randint(0, len(self.noteNames) - 1))
        return note

    #Picks a single note in a specified octave
    def aNote(self, octave):
        '''
        Returns a randomly chosen chromatic pitch with a specified octave.
        '''
        if(octave > 7 or octave < 2):
            return -1
        note = self.noteNames[randint(0, len(self.noteNames) - 1)]
        note = "{}{}".format(note, octave)
        return note

    #Converts a given integer to a pitch class in a random octave (ex C#6)
    def numToNote(self, num):
        '''
        Converts a given integer to a chromatic pitch in a random octave (ex C#6)
        '''
        if(num > len(self.noteNames) or num < 0):
            return -1
        octave = randint(2, 6)
        newNote = self.noteNames[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote  

    #Converts a given integer to a pitch class in a specified octave (ex C#6)
    def numToANote(self, num, octave):
        '''
        Converts a given integer to a pitch class in a specified octave (ex C#6)
        '''
        if(num > len(self.noteNames) - 1):
            return -1
        if(octave < 2):
            return -1
        newNote = self.noteNames[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote

    #Converts a given integer to a pitch class from the chromatic scale (using sharps only)
    def numToChromNote(self, num, octave):
        '''
        Converts a given integer to a pitch class from the chromatic scale
        '''
        if(num > len(self.chromaticScaleSharps) - 1):
            return -1
        if(octave < 2):
            return -1
        newNote = self.chromaticScaleSharps[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote

    #Generates list of chromatic notes in various octaves(C#5, E2, Bb7, etc)
    def newRandNotes(self, total):
        '''
        Generates list of "randomly" chromatic notes in 
        various octaves (i.e. C#5, E2, Bb7, etc...)
        '''
        if(not total):
            return -1
        newNotes = []
        print("\nGenerating random assortment of notes...")
        while(len(newNotes) < total):
            newNotes.append(self.numToNote(randint(0, 16)))
        #Test outputs
        if(not newNotes):
            print("...Unable to generate notes!")
            return -1
        print("New notes: ", newNotes)
        return newNotes
    
    '''
    Note - create a version of notes() that takes the notes of a given MIDI file and uses those
    to generate more notes instead of randomly chosen chromatic notes. 
    '''
    # Picks which key (scale) to use. 
    def pickKey(self):
        '''
        Picks which key (scale) to use. 
        Returns a list of pitch classes without specified octaves.

        For minor scales, feed the output of this into convertToMinor()
        '''
        scale = []
        scale = self.scales[randint(1, 12)]
        return scale

    #Generate new notes for a new melody
    def newNotes(self, total):
        
        '''
        Generate lists of n number notes to be used as a 
        melody/ostinato/riff/whatever, where n is supplied from elsewhere. 
        Uses infrequent repetition.

        Algorithm:
            1. Pick pattern length (l) 
            2. Pick note.
            3. Repeat note or pick another?
                3.1. If repeat, how many times (where r < l)?
                3.2. If not, repeat steps 2-3 while duration total < l.
        '''
        notes = []

        print("\nGenerating", total, "notes...")

        while(len(notes) < total):
            # Pick note + add to list    
            note = self.noteNames[randint(0, len(self.noteNames) - 1)]
            # Repeat this note (1) or not (2)?
            repChoice = randint(1, 2) 
            if(repChoice == 1):
                # Limit reps to no more than 1/3 of the total # of notes
                limit = math.floor(len(notes)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit) 
                for i in range(reps):
                    notes.append(note)
                    if(len(notes) == total):
                        break
            # Dont repeat    
            else:
                if(note not in notes):
                    notes.append(notes)

        if(not notes):
            print("...Unable to generate pattern!")
            return -1

        return notes
    # Generate a series of notes based off an inputted array of integers
    def newNotesFromInts(self, data, isMinor):
        '''
        Generate a series of notes based on inputted data (an array of integers)
        This randomly picks the key and the starting octave! 

        NOTE:
            Long data sets will have the same note associated with different 
            values elsewhere in the array. 
            
            If we ascend through the available octaves we can pick a new 
            key/scale and cycle through the octaves again. This will allow for 
            some cool chromaticism to emerge rather "organiclly" while minimizing
            the amount of repeated notes associated with different elements in 
            the data array (unless we get the same scale chosen again, or there's
            a lot of common tones between the scales that are picked) .  
        '''
        if(len(data) == 0):
            print("ERROR: no data inputted!")
            return -1

        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        octStart = octave

        # Pick initial root/starting scale
        root = self.scales[randint(1, 12)]

        # Will this be a minor scale?
        if(isMinor == True):
            root = self.convertToMinor(root)

        #Display choices
        if(isMinor == True):
            print("\nGenerating", len(data), "notes starting in the key of", root[0], "minor")
        else:
            print("\nGenerating", len(data), "notes starting in the key of", root[0], "major")

        # Scale individual data set integers such that i = i < len(dataSet) -1
        '''
        This will eventually be moved to newMelody() so that
        incoming data will already be scaled by the time it reaches newNotes()
        '''
        data = self.scaleTheScale(data)
        '''
        Note generation algorithm:

            1. Total notes is equivalent to number of notes in data set.
                1b. Maybe if data-sets exceed a certain length, we can 
                    create a subset of available notes that is divisible
                    by the total number elements in the data set
            2. Generate a starting key/scale, and a starting octave.
            3. Cycle through this scale appending each note to a list
               of available notes until we reach the last note in the scale
               in octave 8.
            4. If we reach this note, reset octave to starting point, and 
               pick a new starting scale at random.
            5. Repeat steps 3-4 until we reach the end of the supplied data set.
        '''    
        # Generate notes to pick from
        n = 0
        notes = []
        scale = []
        for i in range(len(data)):
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            # If we've reached the end of the root scale,
            # increment the octave (until octave 8)
            # Ideally trigger this condition every
            # 6 iterations. 
            if(i % 6 == 0):
                octave += 1
                # If we reach highest octave (8), reset
                # to original starting point/octave 
                # and pick a new scale to chose from
                if(octave > 8):
                    octave = octStart
                    root = self.scales[randint(1, 12)]
                    # Re-decide if we're using minor (1) or major (2) again
                    if(randint(1, 2) == 1):
                        isMinor = True
                        print("Switching to a major key!")
                    else:
                        isMinor = False
                        print("Staying in a minor key!")
                    if(isMinor == True):
                        root = self.convertToMinor(root)
                        print("Key-change! Now using", root[0], "minor")
                    else:
                        print("Key-change! Now using", root[0], "major")
                n = 0
        # Pick notes according to integers in data array
        for i in range(len(data) - 1):
            notes.append(scale[data[i]])
        # Check results
        if(len(notes) == 0):
            print("ERROR: Unable to generate notes!")
            return -1
        return notes

        
    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#


    #Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        return rhythm

    #Pick a fast duration
    def newRhythmFast(self):
        '''
        Generate a single new fast rhythm
        '''
        rhythm = self.rhythmsFast[randint(0, len(self.rhythmsFast) - 1)]
        return rhythm
    
    #Pick a slow duration
    def newRhythmSlow(self):
        '''
        Generate a single new slow rhythm
        '''
        rhythm = self.rhythmsSlow[randint(0, len(self.rhythmsSlow) - 1)]
        return rhythm

    #Generate list of a single repeated rhythm
    def newRhythmRep(self, total):
        '''
        Generate list of a SINGLE repeating rhythm n times, where
        n is supplied from elsewhere.

        Algorithm:
            1. Pick duration.
            2. Pick n repetitions.
            3. Copy into list[i] n times.
        '''
        rhythms = []
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            rhythms.append(rhythm)
        return rhythms

    #Generate list of non-repeating durations
    def newRhythmsNonRep(self, total):
        '''
        Generate list non-repeating rhythms of n length, where
        n is supplied from elsewhere.
        '''
        newDurations = []
        print("\nGenerating", total, "non-repeating rhythms...")
        while(len(newDurations) < total):
            newDurations.append(self.newRhythm())
        if(not newDurations):
            print("...Unable to generate durations!")
            return -1
        return newDurations

    #Generate a list containing a rhythmic pattern
    def newRhythms(self, total):
        '''
        Generate lists of 2-20 rhythms to be used as a 
        melody/ostinato/riff/whatever. Uses infrequent repetition.

        Algorithm:
            1. Pick pattern length (l) 
            2. Pick duration.
            3. Repeat duration or pick another?
                3.1. If repeat, how many times (r < l)?
                3.2. If not, repeat steps 2-3 while duration total < l.
        '''
        i = 0
        rhythms = []
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            #Pick rhythm + add to list    
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            #Repeat this rhythm or not? 1 = yes, 2 = no
            repChoice = randint(1, 2) 
            if(repChoice == 1):
                #Limit reps to no more than 1/3 of the total no. of rhythms
                limit = math.floor(len(rhythms)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 1
                reps = randint(1, limit) 
                while(i < reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == total):
                        break
                    i += 1
            else:
                if(rhythm not in rhythms):
                    rhythms.append(rhythm)

            print("Total:", len(rhythms))

        if(not rhythms):
            print("...Unable to generate pattern!")
            return -1
        return rhythms

    #Generate list of rhythmic patterns
    def newRhythmList(self):
        '''
        Generate a list of rhythmic patterns (2 - 10 total)

        Algorithm:
            1. Pick list length
            2. Generate patterns until no of patterns reaches 
               inputted length.
        '''
        patterns = []
        total = randint(2, 10)
        while(len(patterns) < total):
            patterns.append(self.newRhythms())
        return patterns

    #Generate list of repeated rhythms
    def newRepeatedRhythms(self):
        '''
        Generates a list of 5-21 immediately repeated rhythms
        ex: [1, 1, 0.25, 0.25., 0.25, 0.125, 0.125, 0.125, 0.125...n] etc...
        '''
        i = 0
        rhythms = []
        total = randint(5, 21)
        while(i < total):
            j = 0
            reps = randint(1, 9)
            rhythm = self.newRhythm()
            while(j < reps):
                rhythms.append(rhythm)
                if(len(rhythms) == total):
                    break
                j += 1
            i += 1
        return rhythms
    #Generate list of short non-repeating rhythms
    def newRhythmsFast(self):
        '''
        Generates a list of 5-17 *fast* rhythms w/sporadic repetition
        '''
        i = 0
        rhythms = []
        #5-17 rhythms
        lenTotal = randint(5, 17)
        print("\nGenerating fast rhythms...")
        while(len(rhythms) < lenTotal):    
            rhythm = self.rhythmsFast[randint(0, 8)]
            #Repeat this rhythm or not? 1 = yes, 2 = no
            repChoice = randint(1, 2)
            if(repChoice == 1):
                limit = math.floor(len(rhythms)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale w/larger lists'''
                reps = randint(1, limit)
                while(i < reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == lenTotal):
                        break
                    i += 1
            else:
                rhythms.append(rhythm)

        if(not rhythms):
            print("...Unable to generate pattern!")
            return -1
        print("Total rhythms:", len(rhythms))
        print("Rhythms:", rhythms)
        return rhythms


    #Generate a randomized version of list of patterns
    '''
    1. Input list of n length.
    2. Pick from each indice of list randomly without
       repeating any selection (or pick less than previous
       total) and copy to new list until each indice 
       has been selected.
       2.1 Randomize all y/n?
       2.2 If not all, which subset will we randomize?
    '''


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    #Generate a single dynamic (to be used such that a passage doesn't have consistenly
    #changing dynamics)
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        dynamic = self.dynamics[randint(0, len(self.dynamics) - 1)]
        return dynamic

    #Generate a soft dynamic
    def newDynamicSoft(self):
        '''
        Generates a single soft dynamic
        '''
        dynamic = self.dynamicsSoft[randint(0, len(self.dynamicsSoft) - 1)]
        return dynamic

    #Generate a medium dynamic
    def newDynamicMed(self):
        '''
        Generates a single medium dynamic
        '''
        dynamic = self.dynamicsMed[randint(0, len(self.dynamicsMed) - 1)]
        return dynamic

    #Generate a loud dynamic.
    def newDynamicLoud(self):
        '''
        Generates a single loud dynamic
        '''
        dynamic = self.dynamicsLoud[randint(0, len(self.dynamicsLoud) - 1)]
        return dynamic

    #Generates a list containing a single dynamic repeated n times
    def newDynamicsRep(self, total):
        '''
        Generates a list containing a single dynamic repeated n times, where
        n is supplied from elsewhere.
        '''
        dynamics = []
        dynamic = self.newDynamic()
        print("\nGenerating", total, "dynamics:", dynamic)
        while(len(dynamics) < total):
            dynamics.append(dynamic)
        return dynamics 

    #Generate list of non-repeating velocities/dynamics
    def newDynamicsNonRep(self, total):
        '''
        Generates a list of non-repeating velocities/dynamics. Total is
        supplied from elsewhere.
        '''
        dynamics = []
        print("\nGenerating", total, "non-repeating dynamics...")
        while(len(dynamics) < total):
            dynamics.append(self.newDynamic())
        return dynamics

    #Generate a list of dynamics. 
    def newDynamics(self, total):
        '''
        Generates a list of dynamics (MIDI velocites). Total supplied from elsewhere.
        Uses infrequent repetition. Returns -1 if unable to generate a list.
        '''
        i = 0
        dynamics = []
        print("\nGenerating", total, "semi-reapeating dynamics...")
        while(len(dynamics) < total):
            #Pick dynamic    
            dynamic = self.dynamics[randint(0, 9)]
            #Repeat this dynamic or not? 1 = yes, 2 = no
            repChoice = randint(1, 2) 
            if(repChoice == 1):
                #Limit reps to no more than 1/3 of the supplied total
                limit = math.floor(total/3)
                '''Note: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 1
                reps = randint(1, limit) 
                while(i < reps):
                    dynamics.append(dynamic)
                    if(len(dynamics) == total):
                        break
                    i += 1
            else:
                if(dynamic not in dynamics):
                    dynamics.append(dynamic)
        if(not dynamics):
            print("...Unable to generate pattern!")
            return -1
        return dynamics

    #Generate list of velocities/dynamics to be used by the variations class.
    def newDynamicsMod(self, totalModify):
        '''
        Generate list of velocities/dynamics to be used by the variations class. Bases
        total off totalModify.
        '''
        if(not totalModify):
            return -1
        print("\nGenerating dynamics...")
        dynamics = []
        while(len(dynamics) < totalModify):
            dynamics.append(self.newDynamic())
        if(not dynamics):
            print("...Unable to generate dynamics!")
            return -1
        return dynamics

    #Generate crecendo (list of gradual velocity value additions)

    #Generate decendo (list of gradual velocity value subtractions)



    #-----------------------------------------------------------------------------------#
    #-------------------------------------Scales----------------------------------------#
    #-----------------------------------------------------------------------------------#


    #Generate a new scale (list of sorted integers between 0 - 11)
    def newScale(self):
        '''
        Generates a new scale. Returns a list of sorted integers between 0-11.

            Let n = starting note (0)
            Let i = randomly chosen interval (1-3)
            Let nn = each subsequent note

            nn | n, nn = nn - 1 + i
        '''
        note = 0
        scale = []
        print("\nGenerating scale...")
        while(len(scale) < 11):
            scale.append(note)
            note += randint(1, 3)
            #Maintain octave equivalence 
            while(note > 11):
                note -= 12
        #Remove duplicates
        scale = list(set(scale))  
        #Sort in ascending order
        scale.sort() 
        if(not scale):
            print("...Unable to generate scale!")
            return -1
        print("New scale:", scale)
        return scale

    #Convert a PC/integer scale to a scale with pitch names (in octave 4)
    def convertScale(self, scale):
        '''
        Convert a PC/integer scale to a scale with pitch names (in octave 4)
        '''
        if(not scale):
            return -1
        i = 0
        octave = 4
        newScale = []
        while(i < len(scale)):
            note = self.numToANote(scale[i], octave)
            newScale.append(note)
            i += 1
        if(not newScale):
            return -1
        return newScale

    #Generate a new scale with pitch classes.
    def newScalePitches(self):
        '''
        Generate a new scale with pitch classes with enharmonic spellings
        in the middle octave (4)
        '''
        i = 0
        scale = []
        octave = 4
        pcScale = self.newScale()
        print("\nGenerating scale with pitch classes...")
        while(len(scale) < len(pcScale)):
            note = self.chromaticScaleSharps[pcScale[i]]
            note = "{}{}".format(note, octave)
            scale.append(note)
            i += 1
        #Test output
        if(not scale):
            print("...Unable to generate scale!")
            return -1
        print("New scale:", scale)
        return scale

    #Generate derivative scales based on each note in a given scale.
    def deriveScales(self, scale):
        '''
        Generate derivative scales based on each note in a given scale.
        
        Algorithm:
            1. Start with first note in prime scale.
            2. Derive each subsequent note by adding a 
            randomly chosen interval. Ex; 0 + 2 = 2,
            2 + 1 = 3, 3 + 2 = 5, creating [2, 3, 5,...] etc.
            3. Repeat step 2 with next note in prime scale
            up to end of scale.            
        '''
        if(not scale):
            return -1 
        i = 0
        variants = []
        print("\nGenerating derived scales...")
        while (i < len(scale)):
            #Retrieve note from prime scale
            note = scale[i]
            scaleVariant = []
            while(len(scaleVariant) < len(scale)):
                note += randint(1, 3)
                if(note > 11):
                    note = self.octaveEquiv(note)
                scaleVariant.append(note)
                #scaleVariant = list(set(scaleVariant)) #Remove duplicates
                #scaleVariant.sort() #Sort new derived scale 
            variants.append(scaleVariant) #Add to list of derived scales.
            i += 1
        if(not variants):
            print("...Unable to generate derived scales!")
            return -1
        print("\nTotal derivisions:", len(scaleVariant))
        print("Derivitions:", variants)
        return variants

    #Generate a 12-tone row.
    def newTwelveToneRow(self):
        '''
        Generate a 12-tone row.
        '''
        print("\nGenerating new 12-tone row...")
        row = []
        while(len(row) < 11):
            pc = randint(0, 11)
            note = self.numToANote(pc, 4)
            if(note not in row):
                row.append(note)
        #Test outputs
        if(not row):
            print("...No row generated!")
            return -1
        print("New row:", row)
        return row

    #Keeps a single pitch within span of an octave (0 - 11)
    def octaveEquiv(self, pitch):
        '''
        Keeps a single pitch within span of an octave (0 - 11). 
        '''
        while(pitch > 12):
            pitch -= 12
        return pitch 

    #Keeps pitches within span of one octave for entire row(utility function)
    def octaveEquivRow(self, row):
        '''
        Keeps pitches within span of one octave for entire row(utility function)
        '''
        if(not row):
            print("...No row recieved!")
            return -1
        i = 0
        while(i < len(row)):
            while(row[i] > 12):
                row[i] -= 12
            i += 1
        return row

    #New major scale off a given root
    def newMajorScale(self, root):
        '''
        Generates a major scale off a given root. Returns
        a list of strings/note names.

        NOTE - maybe use the given root as a distance to transpose
        the default major scale stored in resource data? If the supplied 
        root is 2, then increment all values in the scale by this number,
        while maintaining octave equivalence.
        '''
        if (root < 0):
            print("\nNote integer value below 0!")
            return -1
        print("\nGenerating new major scale off given root...")
        i = 0
        octave = 4
        length = 8
        newScale = []
        #Generate PC integers & convert to note name/string
        while(len(newScale) < length):
            root += self.major[i]
            if(root > 11):
                root = self.octaveEquiv(root)
            newNote = self.numToChromNote(root, octave)
            newScale.append(newNote)
            i += 1
        if(not newScale):
            print("\n...Unable to generate new major scale off given root!")
            return -1
        print("\nNew major scale:", newScale)
        return newScale

    #New natural minor scale off a given root

    #New melodic minor off a given root

    #New harmonic minor off a given root


    #--------------------------------------------------------------------------------#
    #--------------------------------------Chords------------------------------------#
    #--------------------------------------------------------------------------------#


    #Generate a pitch class triad set
    def newPCTriad(self):
        '''
        Generate a pitch class triad set in prime form.
        '''
        print("\nGenerating new PC triad...")
        triad = []
        while(len(triad) < 3):
            note = randint(0, 11)
            if(note not in triad):
                triad.append(note)
        triad.sort()
        if(not triad):
            print("...No PC triad generated!")
            return -1
        print("New PC triad:", triad)
        return triad

    #Generates a series of pitch class sets
    def newPCChords(self):
        '''
        Generates a series of pitch class sets
    
        Note:
            Select from structures class - decide on what chord to use. 
            add ability to select chord, and when translating the integers to
            note names, randomly assign octChoice to each note name. Adds possibility
            of unusual voicings.
        '''
        print("\nGenerating chord progression...")
        i = 0
        newChords = []
        #3-10 chords
        totalChords = randint(3, 10)
        if(not totalChords):
            print("...No amount decided!")
        print("Total new PC chords:", totalChords)
        #Are we generating tertian(1), symmetrical(2), or mixed chord3?
        chordChoice = randint(1, 3)
        if(not chordChoice):
            print("...No chord type decision!")
        #If we're using triads
        if(chordChoice == 1):
            while(i < totalChords):
                newChords.append(self.triads[randint(1, 4)])
                i += 1
        #If we're using symmetrical chords
        elif(chordChoice == 2):
            while(i < totalChords):
                newChords.append(self.symChords[randint(1, 4)])
                i += 1
        #If we're using both
        elif(chordChoice == 3):
            thisChoice = 0
            while(i < totalChords):
                thisChoice = randint(1, 2)
                if(thisChoice == 1):
                    newChords.append(self.triads[randint(1, 4)])
                newChords.append(self.symChords[randint(1, 4)])
                i += 1
        if(not newChords):
            print("...No progression generated!")
            return -1
        print("New progression:", newChords)
        return newChords      

    #Generate 3 random pitches in random octaves to form a triad
    def newPitchTriad(self):
        '''
        Generate 3 random pitches in random octaves to form a triad (i.e. C3, Ab7, Db2, etc.)
        '''
        print("\nGenerating new pitch triad...")
        triad = []
        while(len(triad) < 3):
            note = self.note()
            if(note not in triad):
                triad.append(note)
        if(not triad):
            print("...Unable to generate pitch triad!")
            return -1
        print("New pitch triad:", triad)
        return triad


    #Generates a chromatic chord with 2-9 notes in random octaves
    def newChord(self):
        '''
        Generates a chromatic chord with 2-9 notes in 
        random octaves. Returns -1 if new chord is None/null.
        '''
        chord = []
        totalNotes = randint(2, 9)
        while(len(chord) < totalNotes):
            note = self.note()
            if(note not in chord):
                chord.append(note)
        if(not chord):
            return -1
        return chord

    '''
    Note:
        Create function that generates chords and repeats each one individually
        n number of times.

        ALGORITHM: 
            1. Generate chord.
            2. Repeat this chord?
                2.1. If so, how many times in a row?
                2.2. If not, go back to 1. 
    '''

    #Generates a series of random chromatic chords 
    def newChords(self):
        '''
        Generates 3-10 non-repeating chromatic chords in
        various octaves and spellings. Returns -1 if newChords
        is None/null.
        '''
        print("\nGenerating random chord progression...")
        chord = []
        newChords = []
        #3-10 chords
        totalChords = randint(3, 10)
        while(len(newChords) < totalChords): 
            chord = self.newChord()
            if(chord not in newChords):
                newChords.append(chord)
        if(not newChords):
            print("...No progression generated!")
            return -1
        print("Total chords:", totalChords)
        print("New progression:", newChords)
        return newChords

    #Generates a progression from the notes of a given scale
    def newChordsFromScale(self, scale):
        '''
        Generates a progression from the notes of a given scale.
        Returns 0 if recieving bad input, and -1 if generation was unsuccessfull. 
        '''
        if(scale is None):
            return 0
        print("\nGenerating chords from a given scale...")
        print("Given scale:", scale)
        #How many chords?
        chords = []
        total = randint(3, 10)
        print("\nGenerating", total, "chords...")
        #Pick notes
        while(len(chords) < total):
            chord = []
            #How many notes in this chord?
            totalNotes = randint(2, 9)
            while(len(chord) < totalNotes):
                note = scale[randint(0, len(scale) - 1)]
                if(note not in chord):
                    chord.append(note)
                elif(note in chord and len(chord) > 2):
                    break
            chords.append(chord)
        if(not chords):
            print("...Unable to generate chords!")
            return -1
        print("\nTotal chords:", len(chords))
        print("Chords:", chords)
        return chords



    #--------------------------------------------------------------------------------------#
    #-------------------------Generate Chords Off Fixed Intervals--------------------------#
    #--------------------------------------------------------------------------------------#

    #Generate a chord off a given interval i (between 1 and 6) to total notes for the chord n
    #starting with root r (integer)
    def newSymTriad(self, r, i, n):
        '''
        Generates an intervallicly symmetrical chord of n length 
        based off a given root (r) and interval (i). Returns a 
        list of integers between 0 - 11 of n length. Does not specify
        octave of the notes! Only pitch classes. 
        
        Returns -1 if given interval is invalid.
        '''
        if(i > 6 or i < 1):
            return -1
        chord = []
        while(len(chord) < n):
            chord.append(r)
            r += i
            if(r > 11):
                r = self.octaveEquiv(r)
        if(chord is None):
            return -1
        return chord

    #Generate a major triad off a given root
    def newMajorTriad(self, root):
        '''
        Generate a major triad off a given root
        '''
        if(not root):
            return -1
        i = 1
        j = 0
        chord = [3]
        chord[0] = root
        while(i < 3):
            chord[i] = chord[i-1] + self.majorTriad[j]
            if(chord[i] > 12):
                while(chord[i] > 12):
                    chord[i] -= 12
            i += 1
            j += 1
        return chord
    
    #Generate a minor triad off a given root
    def newMinorTriad(self, root):
        '''
        Generate a minor triad off a given root
        '''
        if(not root):
            return -1
        i = 1
        j = 0
        chord = [3]
        chord[0] = root
        while(i < 3):
            chord[i] = chord[i-1] + self.minorTriad[j]
            if(chord[i] > 11):
                chord[i] = self.octaveEquiv(chord[i])
            i += 1
            j += 1
        return chord

    #Generate a diminished triad off a given root
    def newDimTriad(self, root):
        '''
        Generate a diminished triad off a given root
        '''
        if(not root):
            return -1
        i = 1
        j = 0
        chord = [3]
        chord[0] = root
        while(i < 3):
            chord[i] = chord[i-1] + self.diminishedTriad[j]
            if(chord[i] > 11):
                chord[i] = self.octaveEquiv(chord[i])
            i += 1
            j += 1
        return chord

    #Build an augmented triad off a given root
    def newAugTriad(self, root):
        '''
        Build an augmented triad off a given root
        '''
        if(not root):
            return -1
        i = 1
        j = 0
        chord = [3]
        chord[0] = root
        while(i < 3):
            chord[i] = chord[i-1] + self.augmentedTriad[j]
            if(chord[i] > 11):
                chord[i] = self.octaveEquiv(chord[i])
            i += 1
            j += 1
        return chord

    '''
    Note:
    
        Find way to combine tertian/quartal/quintal functions? 
        Generate a symmetrical chord?
    '''

    #Generate a tertian chord of n length off a given root (integer, 0 - 16) of varying m3/M3 intervals
    def newTertian(self, root):
        '''
        Generate a tertian chord of n length off a given root (integer, 0 - 16) 
        of varying m3/M3 intervals
        '''
        if (root > 16):
            return -1

        print("\nGenerating new tertian chord...")
        octave = 4
        newTertian = []
        #Number of notes in the chord.
        size = randint(2, 9)
        note = self.numToChromNote(root, octave)
        #Add root
        newTertian.append(note)  

        while(len(newTertian) < size):
            #Alter the value of root to generate next note
            root += randint(3, 4)
            if(root > 11):
                root = self.octaveEquiv(root)
            #If there's more than three notes in the chord, move to next octave up
            '''
            if(len(newTertian) % 3 == 0): 
                octave += 1
                if(octave > 7):
                    break
            '''
            #Add next note
            note = self.numToChromNote(root, octave) #Pick next note
            newTertian.append(note)

        if(not newTertian):
            print("...Unable to generate new tertian chord!")
            return -1
        print("Total notes:", len(newTertian))
        print("New tertian chord:", newTertian)
        return newTertian

    #Generate a quartal chord off a given root
    def newQuartal(self, root):
        '''
        Generate a quartal chord of n length off a given root (integer, 0 - 16) 
        '''
        if (root > 16):
            return -1
        print("\nGenerating new quartal chord...")
        octave = 4
        #Number of notes in the chord.
        size = randint(2, 9)
        #Add root
        newQuartal = []
        note = self.numToChromNote(root, octave)
        newQuartal.append(note)  

        while(len(newQuartal) < size):
            #Alter the value of root to generate next note
            root += 5
            if(root > 11):
                root = self.octaveEquiv(root)
            #If there's more than three notes in the chord, move to next octave up
            '''
            if(len(newQuartal) % 3 == 0): 
                octave += 1
                if(octave > 7):
                    break
            '''
            #Add next note
            note = self.numToChromNote(root, octave) #Pick next note
            newQuartal.append(note)

        if(not newQuartal):
            print("...Unable to generate new quartal chord!")
            return -1
        print("Total notes:", len(newQuartal))
        print("New quartal chord:", newQuartal)
        return newQuartal

    #Generate a quintal chord off a given root
    def newQuintal(self, root):
        '''
        Generate a quintal chord of n length off a given root (integer, 0 - 16) 
        '''
        if (root > 16):
            return None
        
        print("\nGenerating new quintal chord...")
        octave = 4
        #Number of notes in the chord.
        size = randint(2, 9)
        #Add root
        newQuintal = []
        note = self.numToChromNote(root, octave)
        newQuintal.append(note)  

        while(len(newQuintal) < size):
            #Alter the value of root to generate next note
            root += 7
            if(root > 11):
                root = self.octaveEquiv(root)
            #If there's more than three notes in the chord, move to next octave up
            '''
            if(len(newQuartal) % 3 == 0): 
                octave += 1
                if(octave > 7):
                    break
            '''
            #Add next note
            note = self.numToChromNote(root, octave) #Pick next note
            newQuintal.append(note)

        if(not newQuintal):
            print("...Unable to generate new quartal chord!")
            return -1
        print("Total notes:", len(newQuintal))
        print("New quartal chord:", newQuintal)
        return newQuintal
    
    #Generate chords off a major scale (maj, min, min, maj, maj, min, dim)

    #Generate chords off a natural minor scale (min, dim, maj, min, min, maj, maj)

    #Generate chords off a harmonic minor scale (min, dim, maj, min, maj, maj, dim)

    #Generate chords off a melodic minor scale (min, dim, maj, maj, maj, dim, dim)



    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    #Generate a melody. 
    def newMelody(self):
        '''
        Picks a new tempo, rhythmic pattern, set of dynamics (or single dynamic), and
        notes. Notes are determined through a series of choices involving their range and 
        whether the melody will be tonal or atonal.

        Appends to pretty_midi object and returns new MIDI object. Also exports a MIDI file.

        NOTE: May need to modify some decision making sequences. For example, try implementing:
              1. Generate a rhythm/note/dynamic set of n length.
              2. Decide to create x number of note events (2 - however many)
              3. For each note event, randomly pick from set n. 
                 ex: note = noteSet[randint(0, len(noteSet) - 1)]

              This could allow for the creation of rhythms/melodies/dynamics with 
              very limited ranges, but for wide variety of other parameters. 

        TODO: Modify this to use a variable number of arguments! Allow user to supply
        the list of rhythms, list of dynamics, and the tempo! If some or none of these
        are supplied, then the function should decide whether to create its own. 

        ALGORITHM:
            1. Pick tempo.
            2. Generate n number of rhythms
            3. Generate n number of dymanics (n = len(rhythms))
                While generating, decide whether to:
                3.1 Use single dynamic
                3.2 Use varing dynamics
                3.3 Alternate between repeating a single dynamic
                    and adding randomly chosen dynamics
            4. Generate n number of notes (n = len(rhythms))
                While generating, decide whether to:
                4.1 Use single octave
                4.2 Use randomly chosen octaves
                4.3 Use fixed range of octaves that are randomly chosen
                4.4 Alter between randomly chosen octaves and a fixed
                    range of octaves thats randomly chosen from.
        '''

        # Melody container object
        newMelody = melody()

        print("\nGenerating melody...")

        #---------------------Initial choices---------------------#

        # Pick tempo
        newMelody.tempo = self.newTempo()

        # Choose paramters
        '''
        choices indices:
            0 = total elements (number of notes, rhythms, and dynamics)
            1 = rhythm choice (1 - 3)
            2 = dynamics choice (1 - 2)
            3 = tonality choice (1 - 2) NOTE: not used yet!
            4 = melodic range choice (1 - 4)
            5 = which single octave to use, if chosen (single int)
        '''
        choices = choice.melodyChoices(self)
        if(choices is None):
            return -1

        # Rhythm
        if(choices[1] == 1):
            # Non-repeating (returns 2-20 rhythms)
            print("\n...Using non-repeating rhythms!")
            newMelody.rhythms = self.newRhythmsNonRep(choices[0])
        elif(choices[1] == 2):
            # Repeating (returns 2-10 rhythms)
            print("\n...Using one repeating rhythm!")
            newMelody.rhythms = self.newRhythmRep(choices[0])
        elif(choices[1] == 3):
            # Semi-repeating (returns 2-20 rhythms)
            print("\n...Using semi-repeating rhythm!")
            newMelody.rhythms = self.newRhythms(choices[0])
        if(newMelody.rhythms is None):
            return -1

        # Dynamics
        if(choices[2] == 1):
            # Non-repeating
            newMelody.dynamics = self.newDynamicsNonRep(choices[0])
            print("\n...Using non-repeating dynamics!")
        elif(choices[2] == 2):
            # Repeating
            newMelody.dynamics = self.newDynamicsRep(choices[0])
            print("\n...Using one repeated dynamic!")
        elif(choices[2] == 3):
            # Semi-repeating
            newMelody.dynamics = self.newDynamics(choices[0])
            print("\n...Using semi-repeated dynamics!")
        if(newMelody.dynamics is None):
            return -1

        # Melodic Range
        if(choices[4] == 1):
            print("\nUsing octave", choices[5], "only!")
        elif(choices[4] == 2 or choices[4] == 3):
            octaves = []
            # How many octaves do we want (2-3 max)?
            total = randint(2, 3)
            # Which octaves do we want to use? 
            '''Choose starting octave then add 1 n (total) times'''
            octave = randint(2, 4)
            while(len(octaves) < total):
                octaves.append(octave)
                octave += 1
            if(choices[3] == 2):    
                print("\nUsing octaves:", octaves)
            elif(choices[3] == 3):
                print("\nUsing octaves:", octaves, "plus randomly chosen octaves!")
            if(octave is None or octaves is None):
                return -1
        elif(choices[4] == 4):
            print("\nUsing randomly chosen octaves!")
            
        #----------------------Generate--------------------------#

        # Pick the notes
        print("\nPicking notes...")
        while(len(newMelody.notes) < choices[0]):

            # Using single octave
            if(choices[3] == 1):
                note = self.aNote(choices[4])
            # Using limited range of octaves
            elif(choices[3] == 2):
                note = self.aNote(octaves[randint(0, len(octaves) - 1)])
            # Use random alteration between fixed range/random octaves
            elif(choices[3] == 3):
                # Random octave(1) or select from fixed range (2)?
                if(randint(1, 2) == 1):
                    note = self.note()
                else:
                    note = self.aNote(octaves[randint(0, len(octaves) - 1)])
            # Use random octaves
            elif(choices[3] == 4):
                note = self.note()

            # Repeat this note (1) or not (2)?
            if(randint(1, 2) == 1):
                # Repeat this note r times(reps)
                r = 0
                reps = 0
                # If 1 < notes < 5, repeat between 1 and 3 times 
                if(len(newMelody.notes) < 6 and len(newMelody.notes) > 0):
                    reps = randint(1, 3)
                # Otherwise scale repetitions
                else:
                    reps = choice.howManyRepetitions(self, newMelody.notes)
                while(r < reps):
                    newMelody.notes.append(note)
                    r += 1
                    if(len(newMelody.notes) == choices[0]):
                        break
            # Dont repeat
            else:
                if(note not in newMelody.notes):
                    newMelody.notes.append(note)

        # Check melody container data
        if(newMelody.hasData() == False):
            return -1

        # Add data to MIDI object and write out file.
        if(mid.saveMelody(self, newMelody) == -1):
            return -1

        # Display results
        print("\nRESULTS:")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

        return 0
    

    #Generate a single note string with varying durations and dynamics
    def newRepeatedNote(self):
        '''
        NOTE: NOT READY

        Generate a single note string with varying durations and dynamics.

        ALGORITHM:

            1. Pick note in random or preferred octave
                1.1 If random, generate number
            2. Pick duration
        '''
        # Melody container object for note data
        newNote = melody()

        print("\nGenerating single note with varying dynamics and rhythms...")

        #Tempo
        newNote.tempo = self.newTempo()
        #Pick note
        note = self.note()
        #Total times note is repeated (2-9)
        totalLen = randint(2, 9)
        
        print("\n...Note", note, "will be repeated", totalLen, "times...")

        #Generate lists of dynamics and rhythms
        for i in range(totalLen):
            #Pick dynamic
            dynamic = self.newDynamic()
            #Repeat this dynamic (1) or not (2)?
            if(randint(1, 2) == 1):
                #...How many times (1-3)?
                r = 0
                reps = randint(1, 3)
                while(r < reps):
                    newMelody.dynamics.append(dynamic)
                    if(len(dynamics) == totalLen):
                        break
                    r += 1
            else:
                newNote.dynamics.append(dynamic)

            #Pick rhythm
            rhythm = self.newRhythm()
            #Repeat this rhythm (1) or not (2)?
            if(randint(1, 2) == 1):
                #...How many times (1-3)?
                r = 0
                reps = randint(1, 3)
                while(r < reps):
                    newMelody.rhythms.append(rhythm)
                    if(len(rhythms) == totalLen):
                        break
                    r += 1
            else:
                newMelody.rhythms.append(rhythm)

        if(newMelody.dynamics is None 
            or newMelody.rhythms is None):
            return -1

        #Display results
        print("\n---Results---")
        print("\nTempo:", tempo, "bpm")
        print("\nNote:", note)
        print("\nTotal rhythms:", len(rhythms))
        print("Rhythms:", rhythms)
        print("\nTotal dynamics:", len(dynamics))
        print("Dynamics:", dynamics)

        #Append to MIDI object and export
        '''
        fileName = 'test-singlenote.mid'
        print("Exporting as", fileName)
        if(note is not None and rhythms is not None and rhythms is not None):
            newString = mid.noteMIDI(self, fileName, newNote, rhythms, dynamics, tempo)
        else:
            return False
        '''

    #Generate short, fast pattern
    def newTwinkles(self):
        '''
        NOTE: NOT READY
        
        Generate short to mid length string of notes, fast rhythms, soft dynamics, 
        then repeat n times. Returns pretty_midi object.  
        '''
        i = 0
        newNotes = []
        newRhythms = []
        newDynamics = []

        #New tempo
        tempo = self.newTempo()
        #Which octave?
        octave = randint(5, 8)
        #Total times note/rhythm pattern is repeated (4-7)
        totalReps = randint(4, 7)
        #Pick rhythms. This row is also the limit for generating
        #note and dynamics lists. 
        newRhythms = self.newRhythmsFast()

        print("\nGenerating *twinkly* pattern...")

        #Generate pattern
        while(i < len(newRhythms)):
            note = self.aNote(octave)
            dynamic = self.newDynamicSoft()

            #Repeat this note(1) or not(2)?
            noteRep = randint(1, 2)
            if(noteRep == 1):
                #If yes, how many times (1-5)?
                r = 0
                reps = randint(1, 5)
                while(r < reps):
                    newNotes.append(note)
                    r += 1
                    if(len(newNotes) == len(newRhythms)):
                        break
            else:
                newNotes.append(note)

            #Repeat this dynamic(1) or not(2)?
            DynRep = randint(1, 2)
            if(DynRep == 1):
                #If yes, how many times (1 -5)
                r = 0
                reps = randint(1, 5)
                while(r < reps):
                    newDynamics.append(dynamic)
                    r += 1
                    if(len(newDynamics) == len(newRhythms)):
                        break
            else:
                newDynamics.append(dynamic)

            #End if we somehow get there earlier than expected
            #if(self.isMax3Rows(newRhythms, newDynamics, newNotes, len(newRhythms))):
                break
            i += 1

        #Display results
        print("\n----Pattern----")
        print("\nTempo:", tempo)
        print("\nTotal notes:", len(newNotes))
        print("Notes:", newNotes)
        print("\nTotal rhythms:", len(newRhythms))
        print("Rhythms:", newRhythms)
        print("\nTotal dynamics:", len(newDynamics))
        print("\nTotal repetitions:", totalReps)    

        #Iterate all data n times (totalReps)
        finalNotes = []
        finalRhythms = []
        finalDynamics = []
        '''
        Notes:

            Still need to figure out how to copy newMaterial into finalMaterial n times. 
            Don't want a list of three lists, I want one list copied three times into another list.

            L = list(itertools.repeat("a", 20)) # 20 copies of "a"
            L = list(itertools.repeat(10, 20))  # 20 copies of 10
            L = list(itertools.repeat(['x','y'], 20)) # 20 copies of ['x','y']

            Currently getting "index out of range" error messages with the loops below.

        i = 0
        while(i < totalReps):
            k = 0
            while(k < len(newRhythms)):
                finalNotes[k].append(newNotes[k])
                finalRhythms[k].append(newRhythms[k])
                finalDynamics[k].append(newDynamics[k])
                k += 1
            i += 1  
        '''

        #Write out data to MIDI object and export
        #newTwinkles = mid.append(self, finalNotes, finalRhythms, finalDynamics, tempo)

        return 0
        

    #Generate arpeggio
    '''
    Generate an arpeggio between 1 and 3 octChoice in range, and with n number of notes

    ALGORITHM:

        1. What's the starting note?
        2. How many notes will the arpeggio have? 2 - 10?
        3. What is the range of the arpeggio? One octave? Two?
            3.1 If one, which one?
            3.1 If two, which two? Pick one then either pick the octave above or below
        4. Does it start by going up or down?
        5. Will it be modal or atonal?
            5.1 If modal
                5.1.1 Triadic? Scalar?
        6. If atonal
            6.1 Does it use the same interval? (i.e, an arpeggio of stacked 4ths)
            6.2 If yes
                    6.2.1 Min 2nd?
                    6.2.2 Min 3rd?
                    6.2.3 Per 4th/5th?
                    6.2.4 Tritone?
            6.3 Else
                6.3.1 Which intervals?
    '''

    #Generate a palindromic melody off a given MIDI object.
    '''
    Generate a palindromic melody off a given MIDI object.
    Should work with either a motive or full melody.

    ALGORITHM:

        1. Import MIDI object

        2. Create temp MIDI object

        3. Extract note data to temp object in reverse order (start at end of list and proceed
           to the front. Get len(object.notes())) and subtract counter value with this integer until it's zero.

        4. Append data in temp object to supplied MIDI object.

        5. Return original MIDI object with appended note data.

    '''

    #Generate a drone 
    '''
    Generate a drone of variying length and shape

    ALGORITHM:

        1. Single note, or multiple notes?

        2. If single
            2.1 Which one?
            2.2 Dynamic? (Likely ppp - p)
            2.3 Cresc/dec towards front/end/middle/random segment of n length?
                2.3.1 If yes, where does it start/end?
                2.3.2 How much does it rise/fall by?
                2.3.3 Divide difference by cres/desc
                        duration (d) and apply result (r+r)
                        to indice of dynamics list of len(d)
                2.n ____

        3. Else if multiple:
            3.1 How many?
            3.2 Which ones?
                3.2.1 Pick note, pick interval(s) and apply
                    to chosen note. Repeat interval steps
                    (which one? up/down?) n times on each
                    subsequent note until limit reached.
                    let n = starting pitch, 
                    i = chosen interval 
                    (same for every iteration? or change every time?), 
                    and nn = next note
                    sequence: nn | n, n2 = n + i, n3 = n2 + i, etc...
                3.2.2 Dynamic? (ppp - p)
                3.2.3 Cresc/dec towards front/end/middle/random segment of n length?
                    3.2.3.1 If yes, where does it start/end?
                    3.2.3.2 How much does it rise/fall by?
                    3.2.3.3 Divide difference by cres/desc
                            duration (d) and apply result (r+r)
                            to indice of dynamics list of len(d)

        4. Duration? (min 20 seconds or...????)
    '''