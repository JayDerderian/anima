#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions. 

    
    TODO: Replace self.scales with 5-9 note forte prime forms. These
    will be used as index numbers against either sharps or flats spellings
    of the chormatic scale in pickScale(). Ideally pickScale() will be used
    wherever a new "root" needs to be generated. 
    
    TODO: Create separate file for forte pitch class sets to be imported and called
    in pickScale(). Create a constant called SCALES (a dictionary) of all the 
    5-9 note sets (for now, may add more later). 

    TODO: Implement alternative ways of generating ascending scales that 
    should probably be stand-alone functions that are called at random in 
    newNotes().

    1.  Random interval selection with each note. 
        This will necessitate using PC notation and should use PC numbers 
        as index numbers to pick from a single scale. Each set of interval 
        selections should comprise a 5 to 7 note scale within the span of 
        one octave. Each scale will be daisychained up to a certain octave, 
        afterwhich the cycle will continue like above. 

    2.  Calling newScale() n times (removing random extrainious notes after 
        n cycles to stay within a specified threshold, if necessary)

    3.  Symmetrical intervals (see modes of limit transposition, stacking in 
        alternating 2nds, 3rds, 4ths (per or aug), 5ths (per or aug)

    4.  Calling newNote() n times with only ascending octave supplied as an arg.

    Each will need to return an accurate array of strings (i.e. "C#4") representing
    the process applied to them. Single harmonic spellings (only sharps or flats) 
    will probably be used to maintain simplicity.


    GENERAL NOTES:

        Move all the hard coded "resource data" to a stand-alone file?
        Maybe try to find ways to increase modularity instead of cramming
        everything into one monster generate() class. 

        Long data sets will have the same note associated with different 
        values elsewhere in the array. 
        
        If we ascend through the available octaves we can pick a new 
        key/scale and cycle through the octaves again. This will allow for 
        some cool chromaticism to emerge rather "organiclly" while minimizing
        the amount of repeated notes associated with different elements in 
        the data array (unless we get the same scale chosen again, or there's
        a lot of common tones between the scales that are picked) .


    METHOD NOTES:

        newNotes()
        
            Algorithm:

            1.  Total notes is equivalent to *highest single integer* in supplied data set.
            2.  Generate a starting key/scale, and a starting octave.
            3.  Cycle through this scale appending each note to a list
                of available notes until we reach the last note in the scale
                in octave 5.
               
                NOTE: 
                Add option to randomly modify root scale a little bit? Maybe pick 1 - 3
                notes to augment or diminish by a half-step or something. 
                Basically an option to slowly introduce some chromaticism randomly?

            4.  If we reach this note, reset octave to a new starting point, and 
                pick a new starting scale at random.
            5.  Repeat steps 3-4 until we have as many notes as the highest single
                integer from the supplied data set.
   
           
        scaleTheScale()

            The goal is to generate a modified integer array such that any int
            whose value is greater than len(data) - 1  be modified to adhere to this
            limit. Ideally only to i = len(data) - 1, no less. This would provide the
            greatest possible range of index values and maximize the usage of our source
            scale.
    
            Currently need a different way to reduce any data[i] > len(data) - 1 other than 
            by subtracting by 1 x no. of times. This gets us the highest possible index
            (exactly len(data) - 1) but with the most potential to run longest (especially
            with data sets where there might be one extremely high number among a set that's
            within a limitied-ish range).  

            subtract by len(data) - 1 n times? 

            divide data[i] by len(data) - 1 n times? Might introduce a bias towards
            loward end of source scale? Maybe? I don't know. 


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

        #------------------------------Add Meta-Data---------------------------#

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
            notes = '\n\nNotes: ' + noteStr
            f.write(notes)

            totalRhythms = '\n\nTotal rhythms:' + str(len(newMelody.rhythms))
            f.write(totalRhythms)

            rhythmStr = ', '.join([str(i) for i in newMelody.rhythms])
            rhythms = '\nRhythms: ' + rhythmStr
            f.write(rhythms)

            totalDynamics = '\n\nTotal dynamics: ' + \
                str(len(newMelody.dynamics))
            f.write(totalDynamics)

            dynamicStr = ', '.join([str(i) for i in newMelody.dynamics])
            dynamics = '\nDynamics: ' + dynamicStr
            f.write(dynamics)

        if(newChords is not None):
            # Save harmony data
            header = "\n\n\n----------------HARMONY INFO-------------------"
            f.write(header)

            # Get totals
            totalChords = '\n\nTotal chords: ' + str(len(newChords))
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
        Returns inputted integer array with any ints i > len(data) - 1 altered to 
        adhere to this limit. This will keep the newly inputted data array's 
        values within the bounds of the scale array. These values function as a 
        collection of index numbers to sequentially map to a new source
        scale to generate melodic ideas. 
        '''
        # print("\nScaling input...")
        if(type(data) != list):
            print("\nscaleTheScale() - ERROR: wrong data type inputted!")
            return -1
        # did we get a list of ints??
        if(type(data) == list):
            for i in range(len(data)):
                if(type(data[i]) != int):
                    print("\nscaleTheScale() - ERROR: not a list of ints!")
                    return -1
        # is this list empty?
        if(len(data) == 0):
            print("\nscaleTheScale() - ERROR: no data inputted")
            return -1
        # scale it
        for i in range(len(data)):
            # Repeat this subtraction until we're under our threshold.
            while(data[i] > len(data) - 1):
                data[i] -= 1
                # data[i] = math.floor(data[i] / len(data) - 1)
        return data

    # Maps letters to index numbers
    def mapLettersToNumbers(self, letters):
        '''
        Takes a string of any length as an argument, 
        then maps the letters to index numbers, which will then be 
        translated into notes (strings). Accounts for number chars 
        as well

        Thank you to Eric Dale for getting this method in better shape.
        '''
        # print("\nMapping letters to index numbers...")
        # Convert given string to array of chars
        if(type(letters) != str):
            print("\nmapLettersToNumbers() - ERROR: wrong data type inputted!")
            return -1
        # convert to list of str's
        letters = list(letters)
        # make all uppercase characters lowercase
        for i in range(len(letters) - 1):
            if(letters[i].isupper() == True):
                letters[i] = letters[i].lower()
        numbers = []
        for char in letters:
            # check if each character is a letter
            if char.isalpha():
                # add its index to the numbers list
                numbers.append(self.alphabet.index(char))
            elif char.isnumeric():
                # if it's already a number, add it as an int
                numbers.append(int(char))
        if(len(numbers) == 0):
            print("ERROR: no index numbers found!")
            return -1
        return numbers

    # Convert a hex number representing a color to an array of integers
    def hexToIntArray(self, hex):
        '''
        Converts a prefixed hex number to an array of integers.
        '''
        # error check
        if(type(hex) != str):
            print("\nhexToIntoArray() - ERROR: wront type inputted!")
            return -1
        # convert to int
        hexStr = int(hex, 0)
        # convert to array of ints (ie. 132 -> [1, 3, 2])
        numArr = [int(x) for x in str(hexStr)]
        return numArr

    # Convert base rhythms to values in a specified tempo
    def tempoConvert(self, tempo, rhythms):
        '''
        A rhythm converter function to translate durations in self.rhythms (list)
        or self.rhythm (float) to actual value in seconds for a specified tempo. 
        
        ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

        60/72 = .83 - The result becomes the converter value to multiply all supplied
        durations against to get the new tempo-accurate durations.

        '''
        if(type(tempo) != float or type(tempo) != int):
            print("\ntempoConvert() - ERROR: tempo needs to be a float or int!")
            return -1
        diff = 60/tempo
        # is this a single float?
        if(type(rhythms) == float):
            rhythms *= diff
        # or a list of floats?
        elif(type(rhythms) == list):
            for i in range(len(rhythms) - 1):
                rhythms[i] *= diff
                '''NOTE: Truncate float a bit here??? Might help
                         with sheet music generation'''
        else:
            print("\ntempoConvert() - ERROR: wrong type inputted!")
            return -1
        return rhythms
        

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
        '''

        #-------------------Error checks----------------------#

        # Did we get a list?
        if(data is not None and type(data) != list):
            print("\nnewNotes() - ERROR: data inutted is type: ", type(data))
            return -1
        # And is this a list of *ints*??
        # if(data is not None):
        if(data is not None and type(data) == list):
            for i in range(len(data)):
                if(type(data[i]) != int):
                    print("\nnewNotes() - ERROR: data is list but with wrong element type: ", type(data[i]))
                    return -1             

        #-----------------Generate seed scale------------------#

        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        # Pick initial root/starting scale (major or minor)
        root = self.scales[randint(1, len(self.scales) - 1)]
        # # Will this be a minor scale (0 = no, 1 = yes)?
        if(randint(0, 1) == 1):
             root = self.convertToMinor(root)
     
        '''
        NOTE: replace above lines from octave assignment to convertToMinor() with block
        below once newScale()'s mido bug is resolved.
        '''
        # # Pick starting octave (2 or 3)
        # octave = randint(2, 3)
        # # Pick from dictionary
        # if(randint(1, 2) == 1):
        #     root = self.scales[randint(1, len(self.scales) - 1)]
        #     # Convert to relative minor randomly
        #     if(randint(1, 2) == 1):
        #         root = self.convertToMinor(root)
        # # OR generate a new one
        # else:
        #     root = self.newScale(octave)

        # Pick total: 3 - 50 if we're generating random notes
        if(data is None):
            # Note that the main loop uses total + 1!
            total = randint(2, 49)
        # Or the max value of the supplied data set
        else:
            total = max(data)
        
        #-----------------Generate source scale-----------------#

        n = 0
        scale = []
        for i in range(total + 1):
            # Pick note and add to list
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            # Every 7th iteration
            '''
            NOTE: 7 might need to be replaced with however many
            notes in the root scale in a randomly generated one are.
            '''
            if(i % 7 == 0):
                # Increment octave
                octave += 1
                # Have we reached the octave limit?
                if(octave > 5):
                    # Reset starting octave
                    octave = randint(2, 3)
                    # Generate another new scale
                    root = self.scales[randint(1, len(self.scales) - 1)]
                    # Re-decide if we're using minor (1) or major (2) again
                    if(randint(1, 2) == 1):
                        root = self.convertToMinor(root)
                # Reset n to stay within len(root)
                n = 0

        # Randomly pick notes from the generated source scale
        notes = []
        if(data is None):
            # Total notes in melody will be between 3 and 
            # however many notes are in the source scale
            total = randint(3, len(scale))
            for i in range(total):
                notes.append(scale[randint(0, len(scale) - 1)])

        # ...Or pick notes according to integers in data array
        else:
            # Total number of notes is equivalent to the 
            # number of elements in the data set
            for i in range(len(data)):
                notes.append(scale[data[i]])

        return notes

    # Pick a forte prime form from self.scales, then convert to 
    # list of strings
    def pickScale(self, octave=None):
        '''
        Picks a 5 to 9 note Forte pitch class prime form, then
        converts to a string of note names (i.e. ["C#","D#",...etc])

        Returns a list of note name strings.

        NOTE: NOT READY. Need to create a prime form dictionary first! Yay...
        '''
        # pick forte pcs/index values
        scale= []
        # use sharps or flats?
        sof = randint(1, 2)
        # pick prime form
        # pcs = self.scales[randint(0, len(self.scales) - 1)]
        pcs = [0, 2, 4, 5, 7, 9, 11]
        # pick octave if necessary
        if(octave is None):
            octave = randint(2, 3)
        # convert accordingly
        for i in range(len(pcs)):
            if(sof == 1):
                note = "{}{}".format(self.chromaticScaleSharps[pcs[i]], octave)
                scale.append(note)
            else:
                note = "{}{}".format(self.chromaticScaleFlats[pcs[i]], octave)
                scale.append(note)
        return scale


    # Generate a new scale to function as a "root"
    def newScale(self, octave=None):
        '''
        Requires a starting octave. Returns a randomly generated scale 
        within one octave to be used as a 'root'. Returns -1 on failure.

        NOTE: There is an error being raised by the mido library whenever
              I try to use this. This gets the exception error saying the data_byte
              is outside the bounds 0...127. Maybe something gets weird when going
              from ints to chars.

              May try just randomly picking from either self.chromaticScale____ n times,
              then trying to sort the strings as ascending pitches? 
        '''
        # print("\nGenerating new root scale...")
        if(octave is not None):
            if(type(octave) != int):
                print("\nnewScale() - ERROR: octave wasn't an int!")
                return -1
            elif(octave < 1 or octave > 6):
                print("\nnewScale() - ERROR: octave out of range!")
                return -1
        elif(octave is None):
            octave = 4
        pcs = []
        # Use sharps (1) or flats (2)?
        sof = randint(1, 2)
        # generate an ascending set of 5-9 integers/note array indices
        total = randint(5, 9)
        while(len(pcs) < total):
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
            print("\nnewScale() - ERROR: unable to generate scale!")
            return -1
        # print("new scale:", scale, "\n")
        return scale

    # Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        # print("\nConverting major scale to relative minor...")
        if(len(scale) == 0):
            print("\nconvertToMinor() - ERROR: no scale inputted!")
            return -1
        k = 5
        minorScale = []
        for i in range(len(scale)):
            minorScale.append(scale[k])
            k += 1
            if(k > len(scale) - 1):
                k = 0
        if(len(minorScale) == 0):
            print("\nconvertToMinor() - ERROR: unable to generate minor scale!")
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

        NOTE: Modify to return a dictionary of variants, rather
              than an list of lists. It'll hopefully make access syntax
              cleaner.            
        '''
        if(not scale):
            return -1 
        variants = []
        for i in range(len(scale)):
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
        # Did we get anything?
        if(len(variants) == 0):
            print("\nderiveScales() - ERROR: Unable to generate derived scales!")
            return -1
        # print("\nTotal derivisions:", len(scaleVariant))
        # print("Derivitions:", variants)
        return variants

    # Generate a 12-tone row.
    def newTwelveToneRow(self):
        '''
        Generate a 12-tone row. 
        Returns a list of ints/pitch classes/index numbers.
        '''
        # print("\nGenerating new 12-tone row...")
        row = []
        while(len(row) < 11):
            note = self.newNote(randint(0, 11), 4)
            if(note not in row):
                row.append(note)
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
            print("\nnewRhythms() - ERROR: Unable to generate pattern!")
            return -1
        return rhythms


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
            print("\nnewDynamics() - ERROR: Unable to generate pattern!")
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
                '''NOTE: This limit will increase rep levels w/longer list lengths
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
        # If we dont get a source scale
        if(scale is None):
            '''NOTE: See notes for newScale()! '''
            # scale = self.newScale()
            scale = self.newNotes()
        # New chord() object
        newchord = chord()
        # Add tempo
        if(tempo is None):
            newchord.tempo = 60.0
        else:
            newchord.tempo = tempo
        # How many notes in this chord? 2 to 9 (for now)
        total = randint(2, 9)
        # Pick note and add to list
        '''NOTE: this allows for dublings!'''
        while(len(newchord.notes) < total):
            note = scale[randint(0, len(scale) - 1)]
            newchord.notes.append(note)
        # Remove duplicate notes/doublings
        '''NOTE: This is avoids getting the while loop stuck
                 if there's a lot of repeated notes in the melody '''
        newchord.notes = list(dict.fromkeys(newchord.notes))

        # Pick a rhythm & scale to tempo
        rhythm = self.newRhythm()
        newchord.rhythm = self.tempoConvert(newchord.tempo, rhythm)
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
        # Has a scale, tempo, and total been provided?
        if(scale is None):
            # scale = self.newScale()
            scale = self.newNotes()
        elif(total is None):
            total = randint(math.floor(len(scale) * 0.3), len(scale))
            if(total == 0):
                total += 2
        elif(tempo is None):   
            tempo = self.newTempo()
        elif(total is not None and scale is not None):
            # Error check
            if(type(scale) == list):
                if(len(scale) == 0):
                    print("\nnewChordsfromScale() - ERROR: no scale inputted!")
                    return -1
            # Picks total equivalent to between 30-100% of total elements in the scale
            total = randint(math.floor(len(scale) * 0.3), len(scale))
            if(total == 0):
                total = randint(1, len(scale))
        # print("\nGenerating harmonies...")
        # Pick chords
        while(len(chords) < total):
            newchord = self.newChord(tempo, scale)
            chords.append(newchord)
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
        if(n < 0):
            return -1
        if(r > 11):
            r = self.octaveEquiv(r)
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
        print("\nSource data:", newMelody.sourceData)
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)
        return 0

    # Generate a melody from an array of integers (or not).
    def newMelody(self, data=None, dataType=None):
        '''
        Picks tempo, notes, rhythms, and dynamics, with or without a 
        supplied list from the user. It can process a list of ints (dataType == 1),
        floats(2), single char strings/letters(3), or a hex number, represented as a single string(4)

        If no data is supplied, then it will generate a melody anyways. 

        Returns a melody() object if successfull, -1 on failure.
        '''
        # Melody container object
        newMelody = melody()

        #----------------Process any incoming data---------------#
        '''NOTE: Might be able to remove the dataType variable by
                 using type() in the body of the method instead'''
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
            nodata = 'None Inputted'
            newMelody.sourceData.append(nodata)

        #-----------------------Generate!------------------------#

        # print("\nGenerating melody...")
        # Pick tempo
        newMelody.tempo = self.newTempo()
        # Pick instrument
        newMelody.instrument = self.newInstrument()
        '''NOTE: this calls newScale()!'''
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
        '''
        NOTE: Note melody picking should happen here!! Not new newNotes(), that should only
        provide the notes to pick from, not the actually mapping moment.
        '''
        if(data is None):
            newMelody.notes = self.newNotes()
            if(newMelody.notes == -1):
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1
        else:
            newMelody.notes = self.newNotes(data)
        # Pick rhythms (in seconds/floats @ 60bpm) & scale to tempo
        rhythms = self.newRhythms(len(newMelody.notes))
        newMelody.rhythms = self.tempoConvert(newMelody.tempo, rhythms)
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
        if(data is not None):
            if(type(data) == list and len(data) == 0):
                print("\naNewMelody() - ERROR: no data inputted!")
                return -1
        if(dataType is not None): 
            if(type(dataType) == int and dataType > 4 or dataType < 1):
                print("\naNewMelody() - ERROR: dataType out of range!")
                return -1

        # Generate melody
        elif(data is not None and dataType is not None):
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
                print("\n\naNewMelody() - ERROR: Unable to export piece to MIDI file!")
                return -1

            # Save composition data to a .txt file (fileName)
            fileName = "{}{}".format(title, '.txt')
            # print("\nText file saved as:", fileName)
            title2 = "{}{}{}{}".format(
                title, ' for ', newTune.instrument, ' and piano')
            # Export composition data
            print("\nNew melody title:", title2)
            self.saveInfo(title2, data, fileName, newTune)
            return 0

        else:
            print("\naNewMelody() - ERROR: unable to generate melody!")
            return -1

    # Wrapper for newChords(). Outputs chords as a MIDI file and
    # exports a .txt file with relevant data
    def newProgression(self, total=None, tempo=None, sourceScale=None):
        '''
        Wrapper for newChords(). Outputs chords as a MIDI file and
        exports a .txt file with relevant data. 
        
        Needs *ALL* required data or none. No in-between at the moment.
        
        Returns a list of chord() objects
        '''
        if(total is None):
            total = randint(3, 15)
        elif(tempo is None):
            tempo = self.newTempo()
        elif(sourceScale is None):
            sourceScale = self.newNotes()
        chords = self.newChords(total, tempo, sourceScale)
        # generate title
        title = self.newTitle()
        # create MIDI file name
        title1 = title + '.mid'
        # save to MIDI file
        if(mid.saveChords(self, title, chords) != -1):
            print("\nMIDI file saved as:", title1)
        else:
            print("\nnewProgression() - ERROR: unable to save MIDI file!")
            return -1
        # export to .txt file
        self.saveInfo(name=title, data=sourceScale, fileName=title1, newChords=chords)
        return chords

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

        # Did we get an empty list?
        if(data is not None and len(data) == 0):
            print("\nnewComposition() - ERROR: no data inputted!")
            return -1
        if(dataType is not None):
            if(dataType < 1 or dataType > 4):
                print("\nnewComposition() - ERROR: bad data type!")
                return -1
            # else:
            #     print("\nnewComposition() - ERROR: wrong type for dataType variable!")

        #----------------------Generate melody and Harmony--------------------------#

        if(data is not None and dataType is not None):
            newTune = self.newMelody(data, dataType)
            # music.melodies.append(newTune)
        else:
            newTune = self.newMelody()
            # music.melodies.append(newTune)

        newChords = self.newChords(len(newTune.notes), newTune.tempo, newTune.notes)
        # music.chords.append(newChords)

        #------------------------Check data-----------------------------#

        if(newTune.hasData() == False or len(newChords) == 0):
            print("\nnewComposition() - ERROR: No composition data created")
            return -1
        # if(len(music.melodies) == 0 or len(music.chords) == 0):
        #     print("\ERROR: unable to create music() object")
        #     return -1

        #-------Generate title and save to MIDI file--------#
        
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