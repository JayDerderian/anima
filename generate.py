#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions. 

    NOTE:
        Long data sets will have the same note associated with different 
        values elsewhere in the array. 
        
        If we ascend through the available octaves we can pick a new 
        key/scale and cycle through the octaves again. This will allow for 
        some cool chromaticism to emerge rather "organiclly" while minimizing
        the amount of repeated notes associated with different elements in 
        the data array (unless we get the same scale chosen again, or there's
        a lot of common tones between the scales that are picked) .

----------------------------------------------------------------------------------------------------------------
'''

# IMPORTS
import math
import toabc
import datetime
import instruments
import urllib.request
from random import randint
from midi import midiStuff as mid
from containers.melody import melody
from containers.chord import chord
from containers.composition import composition

# Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.
    '''

    # Constructor
    def __init__(self):

        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#

        # ----------------------------Letters---------------------------------#
        '''
        Used to search against and return an integer representing an 
        array index. 
        '''
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u',
                         'v', 'w', 'x', 'y', 'z']

        #----------------------------Tempo-----------------------------------#

        # Tempos (indices: 0-38)
        self.tempos = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0,  # 1-9 (0-8)
                       # 10-18 (9-17)
                       60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0,
                       # 19-27 (18-26)
                       92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0,
                       # 28-36 (27-35)
                       126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0,
                       184.0, 200.0, 208.0]  # 37-39 (36-38)

        #-----------------------Instrumentation------------------------------#

        # Ensemble size
        self.size = {1: 'solo',
                     2: 'duo',
                     3: 'trio',
                     4: 'quartet',
                     5: 'quintet',
                     6: 'sextet',
                     7: 'septet',
                     8: 'octet',
                     9: 'nonet',
                     10: 'decet',
                     11: 'large ensemble',
                     12: 'open instrumentation'}

        # Instrument list
        self.instruments = instruments.INSTRUMENT_MAP

        #-----------------------Notes and Scales------------------------------#

        # Enharmonically spelled note names starting on A. Indicies: 0-16.
        '''
        Interval mappings for enhamonicly spelled chromatic scale array starting on C
            0 - 0        = unison
            0 - 1 or 2   = half-step
            0 - 3        = whole-step
            0 - 4        = minor third
            0 - 5 or 6   = major third
            0 - 7        = perfect 4th
            0 - 8 or 9   = tritone
            0 - 10       = perfect 5th
            0 - 11       = minor 6th
            0 - 12 or 13 = major 6th/dim 7th
            0 - 14       = minor 7th
            0 - 15 or 16 = major 7th
        '''
        self.notes = ["C ", "C#", "Db", "D ",
                      "D#", "Eb", "E ", "F ",
                      "F#", "Gb", "G ", "G#",
                      "Ab", "A ", "A#", "Bb", "B "]

        # Chormatic scale (using all sharps). Indicies 0 - 11.
        self.chromaticScaleSharps = ["C", "C#", "D", "D#", "E", "F",
                                     "F#", "G", "G#", "A", "A#", "B"]

        # Chormatic scale (using all flats). Indicies 0 - 11.
        self.chromaticScaleFlats = ["C", "Db", "D", "Eb", "E", "F",
                                    "Gb", "G", "Ab", "A", "Bb", "B"]

        # Major Scales
        self.scales = {1: ["C", "D", "E", "F", "G", "A", "B"],
                       2: ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
                       3: ["D", "E", "F#", "G", "A", "B", "C#"],
                       4: ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
                       5: ["E", "F#", "G#", "A", "B", "C#", "D#"],
                       6: ["F", "G", "A", "Bb", "C", "D", "E"],
                       7: ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
                       8: ["G", "A", "B", "C", "D", "E", "F#"],
                       9: ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
                       10: ["A", "B", "C#", "D", "E", "F#", "G#"],
                       11: ["Bb", "C", "D", "Eb", "F", "G", "A"],
                       12: ["B", "C#", "D#", "E", "F#", "G#", "A#"]}

        # Major scale in PC notation.
        self.majorScale = [0, 2, 4, 5, 7, 9, 11]

        # Natural minor scale in PC notation
        self.minorScale = [0, 2, 3, 5, 7, 8, 10]

        # Harmonic minor scale in PC notation
        self.harMinScale = [0, 2, 3, 5, 7, 8, 11]

        # Melodic minor scalale in PC notation
        self.melMinorScale = [0, 2, 3, 5, 7, 9, 11]

        #---------------------------Interval Lists---------------------------#
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

        # Major
        self.major = [2, 2, 1, 2, 2, 2, 1]

        # Natural minor
        self.natMinor = [2, 1, 2, 2, 1, 2, 2]

        # Melodic minor
        self.melMinor = [2, 1, 2, 2, 2, 2, 1]

        # Harmonic minor
        self.harMinor = [2, 1, 2, 2, 1, 3]

        # Whole tone
        self.wholeTone = [2, 2, 2, 2, 2]

        # Octatonic
        self.octatonic = [2, 1, 2, 1, 2, 1, 2]

        # Triads
        self.majorTriad = [4, 3]
        self.minorTriad = [3, 4]
        self.diminishedTriad = [3, 3]
        self.augmentedTriad = [4, 4]

        #---------------------------Chords-----------------------------------#

        # Major, minor, augmented, and diminished triads
        self.triads = {1: [0,4,7], 2: [0,3,7], 
                       3: [0,4,8], 4: [0,3,6]}
        
        # Diminished, augmented, quartal, quintal chords
        self.symChords = {1: [0,3,6], 2: [0,4,8],
                          3: [0,5,10], 4: [0,2,7]}

        #---------------------------Rhythm-----------------------------------#

        '''
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
        '''
        # Rhythms (0-9)
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5,
                        0.375, 0.25, 0.125]

        # Fast rhythms (0-8)
        self.rhythmsFast = [0.375, 0.28125, 0.25, 0.1875, 0.125, 0.09375,
                            0.0625, 0.046875, 0.03125]

        # Slow rhythms (0-7) - [n2 = n1 + (n1/2)]
        self.rhythmsSlow = [8.0, 12.0, 18.0, 27.0,
                            40.5, 60.75, 91.125, 136.6875]


        #--------------------------Dynamics---------------------------------#

        '''
        MIDI velocity/dynamics range: 0 - 127
        '''

        # Dynamics (0-26)
        self.dynamics = [20, 24, 28, 32, 36, 40, 44, 48, 52,
                         56, 60, 64, 68, 72, 76, 80, 84, 88,
                         92, 96, 100, 104, 108, 112, 116, 120, 124]

        # Soft dynamics (0-8)
        self.dynamicsSoft = [20, 24, 28, 32, 36, 40, 44, 48, 52]

        # Medium dynamics (0-8)
        self.dynamicsMed = [56, 60, 64, 68, 72, 76, 80, 84, 88]

        # Loud dynamics (0-8)
        self.dynamicsLoud = [92, 96, 100, 104, 108, 112, 116, 120, 124]

    #-----------------------------------------------------------------------------------------#
    #-----------------------------------Utility Functions-------------------------------------#
    #-----------------------------------------------------------------------------------------#

    # Auto generate a composition title from two random words
    def newTitle(self):
        '''
        Generate a composition title from 1-4 random words.

        Random word generation technique from:
        https://stackoverflow.com/questions/18834636/random-word-generator-python
        '''
        try:
            # get word list
            url = "https://www.mit.edu/~ecprice/wordlist.10000"
            # response = requests.get(url)
            response = urllib.request.urlopen(url)
            # decode data to text string
            text = response.read().decode()
            # separate words into list
            words = text.splitlines()
            # pick 1 to 4 random words
            t = 0
            total = randint(1, 3)
            name = words[randint(0, len(words) - 1)]
            while(t < total):
                name = name + ' ' + words[randint(0, len(words) - 1)]
                t += 1
        except urllib.error.URLError:
            print("\nnewTitle() - ERROR: Unable to retrieve word list!")
            name = 'untitled - '
        return name

    # Auto generate a file/composition name (type - date:time)
    def newFileName(self, title):
        '''
        Generates a title/file name by picking two random words
        then attaching the composition type (solo, duo, ensemble, etc..),
        followed by the date.

        Format: "<words> - <ensemble> - <date: d-m-y hh:mm:ss>"
        '''
        # get date and time.
        date = datetime.datetime.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = date.strftime("%d-%b-%y %H:%M:%S")
        # combine name, ensemble, and date, plus add file extension
        fileName = '{}{}.mid'.format(title, dateStr)
        return fileName

    # Generates a new .txt file to save a new composition's meta-data to
    def saveInfo(self, name, data=None, fileName=None, newMelody=None, newChords=None, newMusic=None):
        '''
        Generates a new .txt file to save a new composition's data and meta-data to.

        NOTE: Should take a music() object containing all data currently required by
              this method:
              -Source data
              -File name
              -Title
              -Melody/melodies
              -Chord/chords 
        '''
        # Create a new file opening object thing
        try:
            f = open(fileName, 'w')
        except PermissionError:
            name = name + '.txt'
            f = open(name, 'w')

        # Generate a header
        header = '\n\n*****************************************************************'
        f.write(header)
        header = '\n--------------------------NEW COMPOSITION------------------------'
        f.write(header)
        header = '\n*****************************************************************'
        f.write(header)

        # ------------------------------Add Meta-Data---------------------------#

        # Add title, instrument(s), and save inputted data
        if(name is not None and newMelody is not None):
            # Generate full title
            title = '\n\n\nTITLE: ' + name
            f.write(title)

            # Add instrument
            instrument = '\n\nInstrument(s): ' + \
                newMelody.instrument + ' and piano'
            f.write(instrument)

            # Add date and time.
            date = datetime.datetime.now()
            # convert to str d-m-y hh:mm:ss
            dateStr = date.strftime("%d-%b-%y %H:%M:%S")
            dateStr = '\n\nDate: ' + dateStr
            f.write(dateStr)

        elif(name is not None):
            # Generate title
            title = '\n\n\nTITLE: ' + name
            f.write(title)

            # Add date and time.
            date = datetime.datetime.now()
            # convert to str d-m-y hh:mm:ss
            dateStr = date.strftime("%d-%b-%y %H:%M:%S")
            dateStr = '\n\nDate: ' + dateStr
            f.write(dateStr)

        # Add original source data
        if(data is not None):
            dataStr = ''.join([str(i) for i in data])
            dataInfo = '\n\nInputted data: ' + dataStr
            f.write(dataInfo)
        else:
            dataInfo = '\n\nInputted data: None'
            f.write(dataInfo)

        #-------------------------Add Melody and Harmony Info--------------------#

        # Save melody info
        if(newMelody is not None):
            header = "\n\n\n----------------MELODY INFO-------------------"
            f.write(header)

            tempo = '\n\nTempo: ' + str(newMelody.tempo) + 'bpm'
            f.write(tempo)

            # Get totals and input
            totalNotes = '\n\nTotal Notes: ' + str(len(newMelody.notes))
            f.write(totalNotes)

            noteStr = ', '.join(newMelody.notes)
            notes = '\nNotes: ' + noteStr
            f.write(notes)

            totalRhythms = '\n\nTotal rhythms:' + str(len(newMelody.rhythms))
            f.write(totalRhythms)

            rhythmStr = ', '.join([str(i) for i in newMelody.rhythms])
            rhythms = '\nRhythms: ' + rhythmStr
            f.write(rhythms)

            totalDynamics = '\n\nTotal dynamics:' + \
                str(len(newMelody.dynamics))
            f.write(totalDynamics)

            dynamicStr = ', '.join([str(i) for i in newMelody.dynamics])
            dynamics = '\nDynamics:' + dynamicStr
            f.write(dynamics)

        if(newChords is not None):
            # Save harmony data
            header = "\n\n\n----------------HARMONY INFO-------------------"
            f.write(header)

            # Get totals
            totalChords = '\n\nTotal chords:' + str(len(newChords))
            f.write(totalChords)

            for j in range(len(newChords)):
                noteStr = ', '.join([str(i) for i in newChords[j].notes])
                notes = '\n\nNotes: ' + noteStr
                f.write(notes)

                rhythm = '\nRhythm: ' + str(newChords[j].rhythm)
                f.write(rhythm)

                dynamicsStr = ', '.join([str(i)
                                        for i in newChords[j].dynamics])
                dynamics = '\nDynamics: ' + dynamicsStr
                f.write(dynamics)

        '''
        NOTE: Use this loop when composition() objects are functional
        '''
        # Input all
        if(newMusic is not None):
            # Save composition data
            header = "\n\n\n----------------COMPOSITION INFO-------------------"
            f.write(header)

            # Save global tempo
            tempo = '\n\nTempo: ' + str(newMusic.tempo) + 'bpm'
            f.write(tempo)

            # Add melodies and harmonies
            for j in range(len(newMusic.melodies)):
                instStr = ', '.join(newMusic.instruments[j])
                inst = '\n\nInstruments: ' + instStr
                f.write(inst)

                noteStr = ', '.join(newMusic.melodies[j].notes)
                notes = '\n\nNotes: ' + noteStr
                f.write(notes)

                rhythmStr = ', '.join([str(i)
                                      for i in newMusic.melodies[j].rhythms])
                rhythms = '\n\nRhythms: ' + rhythmStr
                f.write(rhythms)

                dynamicStr = ', '.join([str(i)
                                       for i in newMusic.melodies[j].dynamics])
                dynamics = '\n\nDynamics:' + dynamicStr
                f.write(dynamics)

        # Close instance
        f.close()
        return 0

    #-----------------------------------------------------------------------------------------#
    #----------------------------------Conversion Functions-----------------------------------#
    #-----------------------------------------------------------------------------------------#

    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''
        Converts an array of floats to an array of ints
        '''
        # print("\nConverting floats to ints...")
        if(type(data) != list):
            print("floatToInt() - ERROR: wrong data type inputted!")
            return -1
        if(len(data) == 0):
            print("floatToInt() - ERROR: no data inputted!")
            return -1
        result = []
        for i in range(len(data)):
            result.append(int(data[i]))
        return result

    # Scale individual data set integers such that i = i < len(dataSet) - 1
    def scaleTheScale(self, data):
        '''
        Returns no. of times data[i] is divisible by the total number of elements 
        in the structure it's in. This will keep the newly inputted data array's 
        values within the bounds of the scale array. These values function as a 
        collection of index numbers to randomly chose from in order to pick note 
        strings from the scale array.

        NOTE: Current method introduces a bias towards the notes in the lower indices
              of the total array (at least the first third). 
        '''
        # print("\nScaling input...")
        if(len(data) == 0):
            print("ERROR: no data inputted")
            return -1
        for i in range(len(data)):
            if(data[i] > len(data) - 1):
                # Which scaling method should we use?
                s = randint(1, 3)
                # Divide data[i] by len(data) - 1
                if(s == 1):
                    data[i] = math.floor(data[i] / len(data) - 1)
                # Subtract by len(data) - 1
                elif(s == 2):
                    while(data[i] > len(data) - 1):
                        data[i] -= len(data) - 1
                # Subtract by 1
                else:
                    while(data[i] > len(data) - 1):
                        data[i] -= 1
        return data

    # Maps letters to index numbers
    def mapLettersToNumbers(self, letters):
        '''
        Takes a string of any length as an argument, 
        then maps the letters to index numbers, which will then be 
        translated into notes (strings). Accounts for number chars 
        as well
        '''
        # print("\nMapping letters to index numbers...")
        # Convert given string to array of chars
        letters = list(letters)
        # Make all uppercase characters lowercase
        for i in range(len(letters) - 1):
            if(letters[i].isupper() == True):
                letters[i] = letters[i].lower()
        numbers = []
        for char in letters:
            # Check if each character is a letter
            if char.isalpha():
                # Add its index to the numbers list
                numbers.append(self.alphabet.index(char))
            elif char.isnumeric():
                # If it's already a number, add it as an int
                numbers.append(int(char))
        if(len(numbers) == 0):
            print("ERROR: no index numbers found!")
            return -1
        return numbers

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
        

    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo between 40-208bpm.
        Returns a float upon success, 60.0 if fail.
        '''
        # print("\nPicking tempo...")
        tempo = 0.0
        tempo = self.tempos[randint(0, len(self.tempos) - 1)]
        if(tempo == 0.0):
            return 60.0
        return tempo


    #--------------------------------------------------------------------------------#
    #----------------------------------Instruments-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks an instrument
    def newInstrument(self):
        '''
        Randomly picks an instrument from a given list. Returns a string.
        '''
        instrument = self.instruments[randint(0, 110)]
        return instrument

    # Picks a collection of instruments of n length.
    def newInstruments(self, total):
        '''
        Generates a list of instruments of n length, where n is supplied from elsewhere.
        Returns a list.
        '''
        instruments = []
        while(len(instruments) < total):
            instruments.append(self.newInstrument())
        return instruments


    #--------------------------------------------------------------------------------#
    #-------------------------------------Pitch--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Converts a given integer to a pitch in a specified octave (ex C#6)
    def newNote(self, num=None, octave=None):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6).
        Requires an integer and the required octave. Returns a single string.

        NOTE: use randint(0, 11) and randint(2, 5) for num/octave args to get a 
              randomly chosen note, or leave arg fields empty
        '''
        # If we get *all* supplied data, pick note
        if(num is not None and octave is not None):
            if(num < 0 or num > 11 or
               octave > 6 or octave < 0):
                return -1
            # Sharps (1) or flats (2)
            if(randint(1, 2) == 1):
                note = self.chromaticScaleSharps[num]
            else:
                note = self.chromaticScaleFlats[num]
        # Otherwise, pick a random note
        else:
            # Pick octave (3 - 5)
            octave = randint(3, 5)
            # Sharps (1) or flats (2)
            if(randint(1, 2) == 1):
                note = self.chromaticScaleSharps[randint(0, 11)]
            else:
                note = self.chromaticScaleFlats[randint(0, 11)]
        # Add octave
        note = "{}{}".format(note, octave)
        return note

    # Generate a series of notes based off an inputted array of integers
    def newNotes(self, data=None):
        '''
        Generates a set of notes based on inputted data (an array of integers).
        Data is used as index numbers to select notes from this series in order
        to generate a melody.

        Note generation algorithm:

            1. Total notes is equivalent to *highest single integer* in supplied data set.
            2. Generate a starting key/scale, and a starting octave.
            3. Cycle through this scale appending each note to a list
                of available notes until we reach the last note in the scale
                in octave 5.
            4. If we reach this note, reset octave to a new starting point, and 
                pick a new starting scale at random.
            5. Repeat steps 3-4 until we have as many notes as the highest single
                integer from the supplied data set.
        '''
        # Check incoming data
        if(data is not None):
            if(type(data) != list):
                # print("\nnewNotes() - ERROR: wrong data type inputted!")
                return -1
            elif(type(data) == list and type(data[0]) != int):
                # print("\nnewNotes() - ERROR: list does not contain integers!")
                return -1

        # Pick starting octave (2 or 3)
        octave = randint(2, 3)

        # Pick initial root/starting scale (major or minor)
        root = self.scales[randint(1, len(self.scales) - 1)]
        # Will this be a minor scale (0 = no, 1 = yes)?
        if(randint(0, 1) == 1):
            root = self.convertToMinor(root)

        '''
        NOTE: replace above lines from octave assignment to convertToMinor() with block
        below once newScale()'s mido bug is resolved.

        if(randint(1, 2) == 1):
            root = self.scales[randint(1, len(self.scales) - 1)]
            if(randint(1, 2) == 1):
                root = self.convertToMinor(root)
        else:
            root = self.newScale(octave)
        '''

        # Use either the max value of the supplied data set...
        if(data is not None):
            total = max(data)
        # ...Or 3 - 50 if we're generating random notes
        else:
            # Note that the main loop uses total + 1!
            total = randint(2, 49)
        
        # Main loop
        n = 0
        scale = []
        for i in range(total + 1):
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            '''NOTE: At most, the alphabet will map to 4 1/3 octaves.
                     Still didn't want to exceed octave 6'''
            if(i % 7 == 0):
                octave += 1
                # Have we reached the octave limit?
                if(octave > 5):
                    # Reset starting octave
                    octave = randint(2, 3)
                    # Generate another new scale, if that's what we want
                    root = self.scales[randint(1, len(self.scales) - 1)]
                    # Re-decide if we're using minor (1) or major (2) again
                    if(randint(1, 2) == 1):
                        root = self.convertToMinor(root)
                # Reset n to stay within len(root)
                n = 0

        # Pick notes according to integers in data array
        notes = []
        if(data is not None):
            # Total number of notes is equivalent to the 
            # number of elements in the data set
            for i in range(len(data)):
                notes.append(scale[data[i]])
        # Randomly pick notes from the generated scale
        else:
            # Total notes in melody will be between 3 and 
            # however many notes are in the source scale
            total = randint(3, len(scale))
            for i in range(total):
                notes.append(scale[randint(0, len(scale) - 1)])

        # Check results
        if(len(notes) == 0):
            print("ERROR: Unable to generate notes!")
            return -1
        return notes

    # Generate a new scale to function as a "root"
    def newScale(self, octave=None):
        '''
        Requires a starting octave. Returns a randomly generated scale 
        within one octave to be used as a 'root'. Returns -1 on failure.

        NOTE: There is an error being raised by the mido library whenever
              I try to use this. This gets the exception error saying the data_byte
              is outside the bounds 0...127. Maybe something gets weird when going
              from ints to chars. 
        '''
        # print("\nGenerating new root scale...")
        if(octave is not None):
            if(octave < 1 or octave > 6):
                print("\nERROR: octave out of range!")
                return -1
        elif(octave is None):
            octave = 4
        pcs = []
        # Use sharps (1) or flats (2)?
        sof = randint(1, 2)
        # generate an ascending set of 7 integers/note array indices
        while(len(pcs) < 7):
            # pick note
            n = randint(0, 11)
            if(n not in pcs):
                pcs.append(n)
        # sort in ascending order
        pcs.sort()
        # convert to strings
        scale = []
        for i in range(len(pcs)):
            if(sof == 1):
                note = "{}{}".format(self.chromaticScaleSharps[pcs[i]], octave)
            else:
                note = "{}{}".format(self.chromaticScaleFlats[pcs[i]], octave)
            scale.append(note)
        if(len(scale) == 0):
            print("newScale() - ERROR: unable to generate scale!")
            return -1
        # print("new scale:", scale, "\n")
        return scale

    # Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        # print("\nConverting major scale to relative minor...")
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

    # Generate derivative scales based on each note in a given scale.
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
        variants = []
        print("\nGenerating derived scales...")
        for i in range(len(scale) - 1):
            #Retrieve note from prime scale
            note = scale[i]
            scaleVariant = []
            while(len(scaleVariant) < len(scale)):
                # add note with random interval value
                note += randint(1, 3)
                if(note > 11):
                    note = self.octaveEquiv(note)
                scaleVariant.append(note)
                #scaleVariant = list(set(scaleVariant)) #Remove duplicates
                #scaleVariant.sort() #Sort new derived scale 
            variants.append(scaleVariant) #Add to list of derived scales.
        if(not variants):
            print("...Unable to generate derived scales!")
            return -1
        # print("\nTotal derivisions:", len(scaleVariant))
        # print("Derivitions:", variants)
        return variants

    # Generate a 12-tone row.
    def newTwelveToneRow(self):
        '''
        Generate a 12-tone row.
        '''
        print("\nGenerating new 12-tone row...")
        row = []
        while(len(row) < 11):
            note = self.newNote(randint(0, 11), 4)
            if(note not in row):
                row.append(note)
        #Test outputs
        if(len(row) == 0):
            print("...No row generated!")
            return -1
        # print("New row:", row)
        return row

    # Keeps a single pitch within span of an octave (0 - 11)
    def octaveEquiv(self, pitch):
        '''
        Keeps a single pitch within span of an octave (0 - 11). 
        '''
        while(pitch > 12):
            pitch -= 12
        return pitch 

    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#


    # Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        return rhythm

    # Generate a list containing a rhythmic pattern
    def newRhythms(self, total=None):
        '''
        Generates a series of rhythms of n length, where n is supplied
        from elsewhere. Can also decide to pick 3 and 30 rhythms
        if no desired total is supplied. 
        
        Uses infrequent repetition.

        NOTE: Supply a smaller value for 'total' if a shorter pattern 
              is needed. 'total' can be used to sync up with a given list or 
              be hard-coded.
        '''
        rhythms = []
        if(total is None):
            total = randint(3, 30)
        # print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            # Pick rhythm and add to list
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            # Repeat this rhythm or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                # Limit reps to no more than roughly 1/3 of the supplied total
                limit = math.floor(total * 0.333333333333)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit)
                for i in range(reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == total):
                        break
            else:
                if(rhythm not in rhythms):
                    rhythms.append(rhythm)
        if(len(rhythms) == 0):
            print("newRhythms() - ERROR: Unable to generate pattern!")
            return -1
        return rhythms

    # Generate list of a single repeated rhythm
    def newSingleRhythmRep(self, total):
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
        # print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            rhythms.append(rhythm)
        return rhythms

    # Generate list of immediatly repeated rhythms
    def newRepeatedRhythms(self):
        '''
        Generates a list of 5-21 immediately repeated rhythms
        ex: [1, 1, 0.25, 0.25., 0.25, 0.125, 0.125, 0.125, 0.125...n] etc...
        '''
        rhythms = []
        total = randint(5, 21)
        for i in range(total):
            reps = randint(1, total - len(rhythms))
            rhythm = self.newRhythm()
            for j in range(reps):
                rhythms.append(rhythm)
                if(len(rhythms) == total):
                    break
        return rhythms

    # Generate list of non-repeating durations
    def newRhythmsNonRep(self, total=None):
        '''
        Generate list non-repeating rhythms of n length, where
        n could be inputted or self-determined.
        '''
        if(total is None):
            total = randint(5, 31)
        newDurations = []
        print("\nGenerating", total, "non-repeating rhythms...")
        while(len(newDurations) < total):
            rhythm = self.newRhythm()
            if(rhythm not in newDurations):
                newDurations.append(newDurations)
        if(len(newDurations) == 0):
            print("newRhythmsNonRep() - ERROR: Unable to generate durations!")
            return -1
        return newDurations


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Generate a single dynamic (to be used such that a passage doesn't have consistenly
    # changing dynamics)
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        dynamic = self.dynamics[randint(0, len(self.dynamics) - 1)]
        return dynamic

    # Generate a list of dynamics.
    def newDynamics(self, total=None):
        '''
        Generates a list of dynamics (MIDI velocites) of n length, 
        where n is supplied from elsewhere. Uses infrequent repetition.
        Can also pick between 3 and 30 rhythms if no total is supplied.

        Uses infrequent repetition.

        NOTE: Supply a smaller value for 'total' if a shorter pattern 
              is needed. 'total' can be used to sync up with a given list or 
              be hard-coded.
        '''
        dynamics = []
        if(total is None):
            total = randint(3, 30)
        # print("\nGenerating", total, "dynamics...")
        while(len(dynamics) < total):
            # Pick dynamic (medium range for now)
            dynamic = self.dynamics[randint(0, 8)]
            # Repeat this dynamic or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                # Limit reps to no more than roughly 1/3 of the supplied total
                limit = math.floor(total * 0.333333333333)
                '''Note: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit)
                for i in range(reps):
                    dynamics.append(dynamic)
                    if(len(dynamics) == total):
                        break
            else:
                if(dynamic not in dynamics):
                    dynamics.append(dynamic)
        if(len(dynamics) == 0):
            print("ERROR: Unable to generate pattern!")
            return -1
        return dynamics


    #--------------------------------------------------------------------------------#
    #---------------------------------Rhythm/Dynamics--------------------------------#
    #--------------------------------------------------------------------------------#


    # Generate a list containing either a rhythmic pattern or series of dynamics
    def newElements(self, dataType, total=None):
        '''
        Generates a series of rhythms or dynamics of n length, where n is supplied
        from elsewhere. Can also generate 3-30 rhythms or dynamics if no total is 
        supplied. dataType (int - 1 or 2) determines which data set to use.

        Uses infrequent repetition.
        '''
        # Check input
        if(total is None):
            total = randint(3, 30)
        # if(dataType == 1):
        #     print("\nGenerating", total, "rhythms...")
        # else:
        #     print("\nGenerating", total, "dynamics...")
        # Main loop
        elements = []
        while(len(elements) < total):
            # Pick rhythm (1) or dynamic(2)?
            if(dataType == 1):
                item = self.rhythms[randint(0, len(self.rhythms) - 1)]
            else:
                item = self.dynamics[randint(0, len(self.dynamics) - 1)]
            # Repeat this rhythm or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                # Limit reps to no more than  approx 1/3 of the total no. of rhythms
                limit = math.floor(len(elements) * 0.3333333333333)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit)
                for i in range(reps):
                    elements.append(item)
                    if(len(elements) == total):
                        break
            else:
                if(item not in elements):
                    elements.append(item)
        if(len(elements) == 0):
            print("\nnewElements() - ERROR: Unable rhythms or dynamics!")
            return -1
        return elements


    #--------------------------------------------------------------------------------#
    #--------------------------------------Chords------------------------------------#
    #--------------------------------------------------------------------------------#


    # Display single chord
    def displayChord(self, chord):
        print("\n------------Chord:-------------")
        print("\nnotes:", chord.notes)
        print("rhythm:", chord.rhythm)
        print("dynamics:", chord.dynamics)

    # Display a list of chords
    def displayChords(self, chords):
        print("\n----------------HARMONY DATA:-------------------")
        for i in range(len(chords)):
            print('\n', i + 1, ': ', 'Notes:', chords[i].notes)
            print('      Rhythm:', chords[i].rhythm)
            print('      Dynamics:', chords[i].dynamics)

    # Generates a chord with randomly chosen notes
    def newChord(self, tempo=None, scale=None):
        '''
        Generates a chord with randomly chosen notes, rhythm, and dynamic.  
        Returns a chord() object.

        NOTE: Will eventually replace newChordFromScale()
        '''
        # Error check
        if(scale is not None):
            if(len(scale) == 0):
                print("ERROR: no input!")
                return -1
        # New chord() object
        newchord = chord()
        # If we dont get a source scale
        if(scale is None):
            '''NOTE: See notes for newScale()! '''
            scale = self.newScale()
        # How many notes in this chord? 2 to 9 (for now)
        total = randint(2, 9)
        while(len(newchord.notes) < total):
            # Pick note and add to list
            note = scale[randint(0, len(scale) - 1)]
            newchord.notes.append(note)
        # Error check
        if(len(newchord.notes) == 0):
            print("\nERROR: no chord generated!")
            return -1
        # Remove duplicate notes/doublings
        '''NOTE: This is avoids getting the while loop stuck
                 if there's a lot of repeated notes in the melody '''
        newchord.notes = list(dict.fromkeys(newchord.notes))
        if(tempo is None):
            newchord.tempo = 60.0
        else:
            newchord.tempo = tempo
        # Pick a rhythm
        newchord.rhythm = self.newRhythm()
        # Pick a dynamic (randomize for each note? probably)
        dynamic = self.newDynamic()
        while(len(newchord.dynamics) < len(newchord.notes)):
            newchord.dynamics.append(dynamic)
        return newchord

    # Generates a series of random chromatic chords 
    def newChords(self, total=None, tempo=None, scale=None):
        '''
        Generates a progression from the notes of a given scale.
        Returns a list of chord() objects.

        NOTE: Chords will be derived from the given scale ONLY! Could possibly
              add more randomly inserted chromatic tones to give progressions more
              variance and color. 
        '''
        chords = []
        # Is there a total, tempo, and scale provided?
        if(total is None):
            total = randint(3, 10)
        elif(scale is None):
            scale = self.newScale()
        elif(tempo is None):   
            tempo = self.newTempo()
        elif(total is not None and scale is not None):
            # Error check
            if(len(scale) == 0):
                print("newChordsfromScale() - ERROR: no scale inputted!")
                return -1
            # Picks total equivalent to between 30-100% of total elements in the scale
            total = randint(math.floor(len(scale) * 0.3), len(scale))
            if(total == 0):
                total = randint(1, len(scale))
        # Display total chords
        # print("\nGenerating", total, "chords...")
        # Pick notes
        while(len(chords) < total):
            newchord = self.newChord(tempo, scale)
            chords.append(newchord)
        if(len(chords) == 0):
            print("newChordsfromScale() - ERROR: Unable to generate chords!")
            return -1
        # Display chords
        # self.displayChords(chords)
        return chords

    # Generates a single chord from a given scale
    def newChordFromScale(self, scale, tempo=None):
        '''
        Generates a single new chord from the notes in a given scale and
        rhythm returns a chord() object. Does not double/repeat notes!
        '''
        if(len(scale) == 0):
            print("ERROR: no input!")
            return -1
        # New chord() object
        newchord = chord()
        # If we dont get any data...
        if(tempo is None):
            # scale = self.newScale()
            tempo = self.newTempo()
        # How many notes in this chord? 2 to 9 (for now)
        total = randint(2, 9)
        while(len(newchord.notes) < total):
            # Pick note and add to list
            note = scale[randint(0, len(scale) - 1)]
            newchord.notes.append(note)
        if(len(newchord.notes) == 0):
            print("\nERROR: no chord generated!")
            return -1
        # Remove duplicate notes/doublings
        '''NOTE: This is avoids getting the while loop stuck
                 if there's a lot of repeated notes in the melody '''
        newchord.notes = list(dict.fromkeys(newchord.notes))
        # Use inputted tempo
        newchord.tempo = tempo
        # Pick a rhythm
        newchord.rhythm = self.newRhythm()
        # Pick a dynamic (randomize for each note? probably)
        dynamic = self.newDynamic()
        while(len(newchord.dynamics) < len(newchord.notes)):
            newchord.dynamics.append(dynamic)
        return newchord

    # Generates a chord progression from the notes of a given scale
    def newChordsFromScale(self, scale, tempo):
        '''
        Generates a progression from the notes of a given scale.
        Returns a list of chord() objects.

        NOTE: Chords will be derived from the given scale ONLY! Could possibly
              add more randomly inserted chromatic tones to give progressions more
              variance and color. 
        '''
        if(len(scale) == 0):
            print("newChordsfromScale() - ERROR: no scale inputted!")
            return -1
        # How many chords?
        chords = []
        # Picks total equivalent to between 30-100% of total elements in the scale
        total = randint(math.floor(len(scale) * 0.3), len(scale))
        if(total == 0):
            total = randint(1, len(scale))
        # Display total chords
        # print("\nGenerating", total, "chords...")
        # Pick notes
        while(len(chords) < total):
            newchord = self.newChordFromScale(scale, tempo)
            chords.append(newchord)
        if(len(chords) == 0):
            print("newChordsfromScale() - ERROR: Unable to generate chords!")
            return -1
        # Display chords
        # self.displayChords(chords)
        return chords

   # Generate a chord off a given interval i (between 1 and 6) to total notes for the chord n
    # starting with root r (integer)
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
        if(len(chord) == 0):
            return -1
        return chord

    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    # Display newMelody() object data
    def displayMelody(self, newMelody):
        '''
        Displays newMelody() object data
        '''
        if(newMelody.hasData() == False):
            print("ERROR: no melody data!")
            return -1

        # Display data
        print("\n-----------MELODY Data:------------")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)
        return 0

    # Generate a melody from an array of integers.
    def newMelody(self, data=None, dataType=None):
        '''
        Picks a tempo, notes, rhythms, and dynamics. Rhythms and dynamics are picked randomly (total
        for each is len(data), notes come from user. Should (ideally) handle either a character
        array for a person's name (or any random set of characters), or an array of 
        either floats or integers of n length.

        If no data is supplied, then it will generate a melody anyways. 

        Appends to newMelody() object and exports a MIDI file. Returns a newMelody() object.
        '''
        # Melody container object
        newMelody = melody()

        #----------------Process any incoming data---------------#

        if(dataType is not None and data is not None):
            print("\nProcessing incoming data...")
            # If ints, scale as necessary
            if(dataType == 1):
                # Save original source data
                newMelody.sourceData = data
                data = self.scaleTheScale(data)

            # If floats then convert to ints and scale
            elif(dataType == 2):
                # Save original source data
                newMelody.sourceData = data
                data = self.floatToInt(data)
                data = self.scaleTheScale(data)

            # If letters/chars then match letters to their corresponding index numbers.
            elif(dataType == 3):
                # Save original source data
                newMelody.sourceData = data
                data = self.mapLettersToNumbers(data)

            # If hex convert to array of ints and scale
            elif(dataType == 4):
                # Converts hex number to string, then saves
                # that as the first item of a list. It's silly, I know.
                data = str(data)
                # Save original source data
                newMelody.sourceData.append(data)
                data = self.hexToIntArray(data)
            else:
                print("\nnewMelody() - ERROR: dataType value out of range!")
                return -1
        else:
            # Otherwise just add single string to list
            data = 'None Inputted'
            newMelody.sourceData.append(data)

        #-----------------------Generate!------------------------#

        print("\nGenerating melody...")
        # Pick tempo
        newMelody.tempo = self.newTempo()
        # Pick instrument
        newMelody.instrument = self.newInstrument()
        '''NOTE: this calls the ability to generate new root scale'''
        # Pick notes
        # if(data is not None):
        #     # Use existing scale (0) or generate a new one (1)?
        #     if(randint(0, 1) == 0):
        #         newMelody.notes = self.newNotes(data)
        #     else:
        #         newMelody.notes = self.newNotes(data, newScale=True)
        # else:
        #     # Use existing scale (0) or generate a new one (1)?
        #     if(randint(0, 1) == 0):
        #         newMelody.notes = self.newNotes()
        #     else:
        #         newMelody.notes = self.newNotes(newScale=True)
        if(data is not None):
            newMelody.notes = self.newNotes(data)
        else:
            newMelody.notes = self.newNotes()
        # Pick rhythms
        newMelody.rhythms = self.newRhythms(len(newMelody.notes))
        # Pick dynamics
        newMelody.dynamics = self.newDynamics(len(newMelody.notes))
        

        #------------Check data, display, and export-------------#

        # Make sure all data was inputted
        if(newMelody.hasData() == False):
            print("\nnewMelody() - ERROR: missing melody data!")
            return -1

        # Display results
        # self.displayMelody(newMelody)

        return newMelody

    #-------------------------------------------------------------------------------------#
    #-------------------------------COMPOSITION GENERATION--------------------------------#
    #-------------------------------------------------------------------------------------#

    # Wrapper for newMelody() function. 
    # Exports MIDI file + generates title + .txt data file
    def aNewMelody(self, data=None, dataType=None):
        '''
        Wrapper for newMelody() function. 
        Exports MIDI file + generates title + .txt data file. 
        Returns 0 on succcess, -1 on failure.
        '''
        if(data is not None and len(data) == 0):
            print("\nnewMelody() - ERROR: no data inputted!")
            return -1
        if(dataType is not None and 
           dataType > 4 or dataType < 1):
            print("\nnewMelody() - ERROR")
            return -1

        # Generate melody
        if(data is not None and dataType is not None):
            newTune = self.newMelody(data, dataType)
        else:
            newTune = self.newMelody()

        # If successfull, export
        if(newTune.hasData() == True):
            # Generate title
            title = self.newTitle()
            # Create MIDI file name
            title1 = title + '.mid'

            # Save to MIDI file
            if(mid.saveMelody(self, title1, newTune) != -1):
                print('')  # print("\nMIDI file saved as:", title1)
            else:
                print("\nERROR:Unable to export piece to MIDI file!")
                return -1

            # Save composition data to a .txt file (fileName)
            fileName = "{}{}".format(title, '.txt')
            # print("\nText file saved as:", fileName)
            title2 = "{}{}{}{}".format(
                title, ' for ', newTune.instrument, ' and piano')
            # Export composition data
            print("\nTitle:", title2)
            self.saveInfo(title2, data, fileName, newTune)

            return 0
        else:
            print("\naNewMelody() - ERROR: unable to generate melody!")
            return -1

    # Outputs a single melody with chords in a MIDI file
    def newComposition(self, data=None, dataType=None):
        '''
        Takes an 0x-xxxxxx hex humber representing a color, or 
        an array of ints, floats or chars of any length as arguments, 
        plus the data type represented by a int 
        (int (1), float (2), char (3), or hex number (4)).

        Outputs a single melody with chords in a MIDI file, as
        well as a .txt file with the compositions title, inputted data, 
        auto-generated title, a random instrumentation, with the date and time
        of generation. Also contains melody and harmony data.

        NOTE: Will eventaully return a music() object containing lists of 
              melody() and chord() objects.
        '''
        # New composition() object
        # music = composition()


        #--------------------Check incoming data------------------------#
        if(data is not None and len(data) == 0):
            print("\nnewComposition() - ERROR: no data inputted!")
            return -1
        if(dataType is not None):
            if(dataType < 1 or dataType > 4):
                print("\nnewComposition() - ERROR: bad data type!")
                return -1
            # else:
            #     print("\nnewComposition() - ERROR: wrong type for dataType variable!")
        

        '''NOTE: append at start or end of lists???'''
        #----------------------Generate melody--------------------------#
        if(data is not None and dataType is not None):
            newTune = self.newMelody(data, dataType)
            # music.melodies.append(newTune)
        else:
            newTune = self.newMelody()
            # music.melodies.append(newTune)


        #---------------------Generate harmonies------------------------#
        # newChords = self.newChordsFromScale(newTune.notes, newTune.tempo)
        newChords = self.newChords(None, newTune.tempo, newTune.notes)
        # music.chords.append(newChords)


        #------------------------Check data-----------------------------#
        if(newTune.hasData() == False or len(newChords) == 0):
            print("\nnewComposition() - ERROR: No composition data created")
            return -1
        # if(len(music.melodies) == 0 or len(music.chords) == 0):
        #     print("\ERROR: unable to create music() object")
        #     return -1

        #-------Generate title, .txt file, and save to MIDI file--------#
        title = self.newTitle()
        # Create MIDI file name
        title1 = title + '.mid'
        # Save to MIDI file
        if(mid.saveComposition(self, newTune, newChords, title1) != -1):
            print("\nMIDI file saved as:", title1)
        else:
            print("\nnewComposition() - ERROR:Unable to export piece to MIDI file!")
            return -1

        #---------Save composition data to a .txt file (fileName)--------#
        fileName = "{}{}".format(title, '.txt')
        print("\nText file saved as:", fileName)
        title2 = "{}{}{}{}".format(title, ' for ', newTune.instrument, ' and piano')
        print("\nTitle:", title2)
        self.saveInfo(title, newTune.sourceData, fileName, newTune, newChords)

        return title1, toabc.abc(title, newTune.tempo, newTune, newChords)