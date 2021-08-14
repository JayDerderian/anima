'''
This module/class handles all generative methods. 
'''

'''
----------------------------------------------------NOTES-------------------------------------------------------


    GENERAL NOTES:

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

        newScale()
            
            Maybe try just randomly picking from c.CHROMATIC_SCALE n times,
            then trying to sort the strings as ascending pitches? Might be tougher
            but we'll see. 


----------------------------------------------------------------------------------------------------------------
'''

# IMPORTS
import math
import array
import midi as m
import numpy as np
import urllib.request
import constants as c
from random import randint
from random import sample
from utils.toabc import abc
from utils.save import saveInfo
from containers.chord import chord
from containers.melody import melody
from datetime import datetime as date

# Generative functions
class Generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.
    '''

    # Constructor
    def __init__(self):
        self.alive = True
        '''
        NOTE: Develop a way to store session info here? Need a way to justify all these
              methods as a class. 
        '''

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
    def newMidiFileName(self, title):
        '''
        Generates a title/file name by picking two random words
        then attaching the composition type (solo, duo, ensemble, etc..),
        followed by the date.

        Format: "<words> - <ensemble> - <date: d-m-y hh:mm:ss>"
        '''
        # get date and time.
        d = date.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = d.strftime("%d-%b-%y %H:%M:%S")
        # combine name, ensemble, and date, plus add file extension
        fileName = '{}{}.mid'.format(title, dateStr)
        return fileName

    # Converts a list of pitch class integers to note strings (with or without an octave)
    def toStr(self, pcs, octave=None):
        '''
        Converts a list of pitch class integers to note name strings, with or without 
        a supplied octave. Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
        '''
        scale = []
        if octave is not None:
            for i in range(len(pcs)):
                note = "{}{}".format(c.CHROMATIC_SCALE[pcs[i]], octave)
                scale.append(note)
        else:
            for i in range(len(pcs)):
                scale.append(c.CHROMATIC_SCALE[pcs[i]])
        return scale


    #-----------------------------------------------------------------------------------------#
    #----------------------------------Conversion Functions-----------------------------------#
    #-----------------------------------------------------------------------------------------#


    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''
        Converts an array of floats to an array of ints
        '''
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
        # scale it
        for i in range(len(data)):
            # Repeat this subtraction until we're under our threshold.
            while data[i] > len(data) - 1:
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

        Thanks to Eric Dale for getting this method in better shape.
        '''
        # convert inputted str to list of str's
        letters = list(letters)
        # make all uppercase characters lowercase
        for i in range(len(letters) - 1):
            if letters[i].isupper() == True:
                letters[i] = letters[i].lower()
        numbers = []
        for char in letters:
            if char.isnumeric():
                # if it's already a number, add it's *index* since it might be out of range'
                # numbers.append(int(char))
                numbers.append(c.ALPHABET.index(char))
        return numbers

    # Convert a hex number representing a color to an array of integers
    def hexToIntList(self, hex):
        '''
        Converts a prefixed hex number to an array of integers.
        '''
        # convert to int
        hexStr = int(hex, 0)
        # convert to array of ints (ie. 132 -> [1, 3, 2])
        hexList = [int(x) for x in str(hexStr)]
        return hexList

    # Convert base rhythms to values in a specified tempo
    def tempoConvert(self, tempo, rhythms):
        '''
        A rhythm converter function to translate durations in self.rhythms (list)
        or self.rhythm (float) to actual value in seconds for a specified tempo. 
        
        ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

        60/72 = .83 - The result becomes the converter value to multiply all supplied
        durations against to get the new tempo-accurate durations.

        '''
        diff = 60/tempo
        # is this a single float?
        if type(rhythms) == float:
            rhythms *= diff
        # or a list of floats?
        elif type(rhythms) == list:
            for i in range(len(rhythms) - 1):
                rhythms[i] *= diff
                '''NOTE: Truncate float a bit here??? Might help
                         with sheet music generation'''
        return rhythms

    # Transpose
    def transpose(self, pcs, i):
        '''
        Transpose a pitch class set using a supplied interval i, or list of 
        intervals i.
        
        Returns a modified pcs (list[int])
        '''
        # modify with a single interval across all pitch-classes
        if type(i) == int:
            for note in range(len(pcs)):
                pcs[note] += i
                if pcs[note] > 11 or pcs[note] < 0:
                    pcs[note] = self.octaveEquiv(pcs[note])
        # modify with a list of intervals across all pitch-classes. 
        # this allows for each pitch-class to be transposed by a unique
        # distance, allowing for rapid variation generation.
        elif type(i) == list:
            for note in range(len(pcs)):
                pcs[note] += i[note]
                if pcs[note] > 11 or pcs[note] < 0:
                    pcs[note] = self.octaveEquiv(pcs[note])
        return pcs
        

    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo (float) between 40-208bpm.
        '''
        return c.TEMPOS[randint(0, len(c.TEMPOS) - 1)]


    #--------------------------------------------------------------------------------#
    #----------------------------------Instruments-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks an instrument
    def newInstrument(self):
        '''
        Randomly picks a melodic/harmonic instrument from a given list. Returns a string.
        Does NOT pick a percussion instrument!
        '''
        return c.INSTRUMENTS[randint(0, 110)]

    # Picks a collection of instruments of n length.
    def newInstruments(self, total):
        '''
        Generates a list of instruments of n length, where n is supplied from elsewhere.
        Returns a list.
        '''
        instruments = []
        while len(instruments) < total:
            instruments.append(self.newInstrument())
        return instruments


    #--------------------------------------------------------------------------------#
    #-------------------------------------Pitch--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Converts a given integer to a pitch in a specified octave (ex C#6)
    def newNote(self, i=None, octave=None):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6), 
        or randomly picks a note between octaves 2 to 5. Returns a single 
        string (i.e. "C#4"), or -1 on failure.

        NOTE: use randint(0, 11) and randint(2, 5) for num/octave args to get a 
              randomly chosen note, or leave arg fields empty
        '''
        if i is None:
            note = c.CHROMATIC_SCALE[randint(0, len(c.CHROMATIC_SCALE) - 1)]
        elif type(i) == int and i > -1 and i < len(c.CHROMATIC_SCALE):
            note = c.CHROMATIC_SCALE[i]
        else:
            return -1
        if octave is None:
            octave = randint(2, 5)
        note = "{}{}".format(note, octave)
        return note
            

    # Generate a series of notes based off an inputted array of integers
    def newNotes(self, data=None):
        '''
        Generates a set of notes to be used as a melody based on inputted data (an array of integers). 
        Can also return a list of notes without any data input. If this is the case,
        then newNotes() will decide how many to generate (between 3 and 50).

        A supplied data list (list[int]) is used as index numbers to select notes from this series 
        in order to generate a melody.

        Returns a tuple: notes list to be used as a melody (list[str]), 
        a list of forte_numbers (list[str]), and the original source scale (list[str])
        '''           

        # Generate seed scale
        # Save forte numbers and/or pitch class sets
        meta_data = []
        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        # Pick a root scale or generate a new root
        if randint(1, 2) == 1:
            root, fn = self.pickScale()
            meta_data.append(fn)
        else:
            root, pcs = self.newScale()
            meta_data.append(pcs)
        # Pick total: 3 - 50 if we're generating random notes
        if data == None:
            # Note that the main loop uses total + 1!
            total = randint(2, 49)
        # Or the largest value of the supplied data set
        else:
            total = max(data)
        
        #Generate source scale
        n = 0
        scale = []
        for i in range(total + 1):
            # Pick note and add to list
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            # when we get to the end of the root scale...   
            if n == len(root):
                # Increment octave
                octave += 1
                # Have we reached the octave limit?
                if octave > 5:
                    # Reset starting octave
                    octave = randint(2, 3)
                    # Generate another new root scale & starting octave + save forte number, if applicable
                    root, fn = self.pickScale()
                    meta_data.append(fn)
                # Reset n to stay within len(root)
                n = 0

        # Randomly pick notes from the generated source scale to 
        # create an arhythmic melody.
        notes = []
        if data == None:
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

        return notes, meta_data, scale

    # Picks either a prime form pitch-class set, or a major or minor scale.
    def pickScale(self, octave=None):
        '''
        Picks either 1 of 12 major or minor scales for a tonal flavor, 
        or a 5 to 9 note Forte pitch class prime form for an atonal flavor.

        Returns tuple with a list of note name strings with or without an 
        assigned octave, plus the forte number of the chosen scale.
        '''
        scale = []
        # use a major or minor scale(1), or pick a prime form(2)?
        if randint(1, 2) == 1:
            '''NOTE: find forte number for minor scale since thats the 
                     number for both maj/min scales'''
            # pick major
            if randint(1, 2) == 1:
                scale = c.MAJOR_SCALES[randint(1, len(c.MAJOR_SCALES) - 1)]
                fn = "{}{}{}".format('None - ', scale[0], ' major')
            # pick minor
            else:
                scale = c.MINOR_SCALES[randint(1, len(c.MINOR_SCALES) - 1)]
                fn = "{}{}{}".format('None - ', scale[0], ' minor')
        else:
            # pick prime form pitch-class set
            fn = c.FORTE_NUMBERS[randint(1, len(c.FORTE_NUMBERS) - 1)]
            pcs = c.SCALES[fn]
            # convert pcs to a list of note names / strings
            for i in range(len(pcs)):
                scale.append(c.CHROMATIC_SCALE[pcs[i]])
        # append octave, if necessary
        if octave is not None:
            _scale = []
            for i in range(len(scale)):
                note = "{}{}".format(scale[i], octave) 
                _scale.append(note)
            # return whichever scale/list we end up needing
            return _scale, fn
        else:
            return scale, fn     


    # Generate a new scale to function as a "root"
    def newScale(self, octave=None):
        '''
        Returns a randomly generated 4 to 9 note scale with or without an octave 
        to be used as a 'root'. Can take an int as a starting octave 
        (between 2 and 5), or not.  
        
        Returns a list of note name strings and the original pitch class set.
        '''
        pcs = []
        total = randint(5, 9)
        while len(pcs) < total:
            # pick pitch class integer
            n = randint(0, 11)
            if n not in pcs:
                pcs.append(n)
        # sort in ascending order
        pcs.sort()
        # convert to strings (with or without supplied octave)
        scale = []
        if octave==None:
            for i in range(len(pcs)):
                scale.append(c.CHROMATIC_SCALE[pcs[i]])
        else:
            for i in range(len(pcs)):
                note = "{}{}".format(c.CHROMATIC_SCALE[pcs[i]], octave)
                scale.append(note)
        return scale, pcs   


    # Generate derivative scales based on each note in a given scale.
    def deriveScales(self, pcs):
        '''
        Generate derivative scales based on each note in a given scale.
        Requires a pitch class set (pcs) list[int] who's values are 
        between 0 - 11, and returns a dictionary of variants (list[int]).

        variants = {
            1: list[int],
            2: list[int]
            etc...
        } 
        
        Algorithm:
            1. Start with first note in prime scale.
            2. Derive each subsequent note by adding a 
               randomly chosen interval. Ex; 0 + 2 = 2,
               2 + 1 = 3, 3 + 2 = 5, creating [2, 3, 5,...] etc.
            3. Repeat step 2 with next note in prime scale
               up to end of scale.        
        '''
        variants = {}
        for i in range(len(pcs)):
            # Retrieve note from prime scale
            sv = []
            note = pcs[i]
            while len(sv) < len(pcs):
                # add note with random interval value (1-3)
                note += randint(1, 3)
                if note > 11:
                    note = self.octaveEquiv(note)
                sv.append(note)
            #scaleVariant = list(set(scaleVariant)) # Remove duplicates
            #scaleVariant.sort() #Sort new derived scale 
            variants[i] = sv
        
        # convert to strings and append octaves here???

        return variants

    # Generate a 12-tone row.
    def newTwelveToneRow(self):
        '''
        Generates a 12-tone row. 

        Returns a tuple: a list[str] of notes in octave 4, 
        and the original pitch class set (list[int]).
        '''
        pcs = sample(c.PITCH_CLASSES, len(c.PITCH_CLASSES))
        row = self.toStr(pcs, octave=4)
        return row, pcs

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
    def printMatrix(self, m):
        '''
        Display a twelve-tone matrix (2D list)
        '''
        for x in m:
            for y in x:
                print(y,end = " ")
            print()
        print()

    # generate a list of 11 intervals to transpose a 12-tone row by to generate
    # a matrix
    def newIntervals(self):
        intervals = []
        while len(intervals) < 11:
            n = randint(1, 11)
            if n not in intervals:
                intervals.append(intervals)
        return intervals

    # Keeps a single pitch within span of an octave (0 - 11)
    def octaveEquiv(self, pitch):
        '''
        Keeps a single pitch within span of an octave (0 - 11). 
        '''
        if type(pitch) != int:
            print("\noctaveEquiv() - ERROR: pitch not an int!")
            return -1
        if pitch > 11:
            while pitch > 11:
                pitch -= 11
        elif pitch < 0:
            while pitch < 0:
                pitch += 11
        return pitch 


    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#


    # Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        return c.RHYTHMS[randint(0, len(c.RHYTHMS) - 1)]

    # Generate a list containing a rhythmic pattern
    def newRhythms(self, total=None, tempo=None):
        '''
        Generates a series of rhythms of n length, where n is supplied
        from elsewhere. Can also decide to pick 3 and 30 rhythms
        if no desired total is supplied. Will convert raw rhythm values
        to a given tempo, if provided. Otherwise it'll just return an
        unaltered float list.
        
        Uses infrequent repetition.

        NOTE: Supply a smaller value for 'total' if a shorter pattern 
              is needed. 'total' can be used to sync up with a given list or 
              be hard-coded.
        '''
        rhythms = []
        if total is None:
            total = randint(3, 30)
        while len(rhythms) < total:
            # Pick rhythm and add to list
            rhythm = self.newRhythm()
            # Repeat this rhythm or not? 1 = yes, 2 = no
            if randint(1, 2) == 1:
                # Limit reps to no more than roughly 1/3 of the supplied total
                limit = math.floor(total * 0.333333333333)
                '''NOTE: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if limit == 0:
                    limit += 2
                reps = randint(1, limit)
                for i in range(reps):
                    rhythms.append(rhythm)
                    if len(rhythms) == total:
                        break
            else:
                if rhythm not in rhythms:
                    rhythms.append(rhythm)
        # convert to given tempo, if provided.
        if tempo is not None and tempo != 60.0:
            rhythms = self.tempoConvert(tempo, rhythms)
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
        return c.DYNAMICS[randint(0, len(c.DYNAMICS) - 1)]

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
        if total is None:
            total = randint(3, 30)
        while len(dynamics) < total:
            # Pick dynamic (medium range for now)
            dynamic = self.newDynamic()
            # Repeat this dynamic or not? 1 = yes, 2 = no
            if randint(1, 2) == 1:
                # Limit reps to no more than roughly 1/3 of the supplied total
                limit = math.floor(total * 0.333333333333)
                '''NOTE: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if limit == 0:
                    limit += 2
                reps = randint(1, limit)
                for i in range(reps):
                    dynamics.append(dynamic)
                    if len(dynamics) == total:
                        break
            else:
                if dynamic not in dynamics:
                    dynamics.append(dynamic)
        return dynamics


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
        '''
        # New chord() object
        newchord = chord()

        # Pick or generate a new scale if we don't get one supplied
        if scale is None:
            # pick a scale (1) or create a new one (2)?
            if randint(1, 2) == 1:
                # Pick scale and save forte number/scale info
                scale, newchord.fn = self.pickScale(octave=randint(2, 5))
                newchord.sourceNotes = scale
            else:
                # Create a scale and save original pitch class set
                scale, newchord.pcs = self.newScale(octave=randint(2, 5))
                newchord.sourceNotes = scale

        # Add tempo if one isn't supplied
        if tempo is None:
            newchord.tempo = 60.0
        else:
            newchord.tempo = tempo

        # How many notes in this chord? 2 to 9 (for now)
        total = randint(2, 9)
        # Pick notes and add to list
        '''NOTE: this allows for dublings!'''
        while len(newchord.notes) < total:
            newchord.notes.append(scale[randint(0, len(scale) - 1)])

        # Remove duplicate notes/doublings
        '''NOTE: This is avoids getting the while loop stuck
                 if there's a lot of repeated notes in the melody '''
        newchord.notes = list(dict.fromkeys(newchord.notes))

        # Pick a rhythm & scale to tempo if needed
        rhythm = self.newRhythm()
        if newchord.tempo != 60.0:
            newchord.rhythm = self.tempoConvert(newchord.tempo, rhythm)
        else:
            newchord.rhythm = rhythm

        # Pick a dynamic (randomize for each note? probably)
        dynamic = self.newDynamic()
        while len(newchord.dynamics) < len(newchord.notes):
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
        if scale is None:
            scale, data, source = self.newNotes()
        elif total is None:
            total = randint(math.floor(len(scale) * 0.3), len(scale))
            if total == 0:
                total += 2
        elif tempo is None:   
            tempo = self.newTempo()
        elif total is not None and scale is not None:
            # Error check
            if type(scale) == list:
                if(len(scale) == 0):
                    print("\nnewChordsfromScale() - ERROR: no scale inputted!")
                    return -1
            # Picks total equivalent to between 30-100% of total elements in the scale
            total = randint(math.floor(len(scale) * 0.3), len(scale))
            if total == 0:
                total = randint(1, len(scale))

        # Pick chords
        while len(chords) < total:
            newchord = self.newChord(tempo, scale)
            chords.append(newchord)
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
        if i > 6 or i < 1:
            return -1
        if n < 0:
            return -1
        if r > 11:
            r = self.octaveEquiv(r)
        chord = []
        while len(chord) < n:
            chord.append(r)
            r += i
            if r > 11:
                r = self.octaveEquiv(r)
        return chord


    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    # Display newMelody() object data
    def displayMelody(self, newMelody):
        '''
        Displays newMelody() object data
        '''
        print("\n-----------MELODY Data:------------")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nInstrument:", newMelody.instrument)
        print("\n\nSource data:", newMelody.sourceData)
        print("\nSource scale:", newMelody.sourceScale)
        print("\nForte Numbers:", newMelody.fn)
        print("\n\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

    # Generate a melody from an array of integers (or not).
    def newMelody(self, tempo=None, data=None, dataType=None):
        '''
        Picks tempo, notes, rhythms, and dynamics, with or without a 
        supplied list from the user. It can process a list of ints (dataType == 1),
        floats(2), single char strings/letters(3), or a hex number, 
        represented as a single string(4)

        If no data is supplied, then it will generate a melody anyways. 

        Returns a melody() object if successfull, -1 on failure.

        NOTE: Instrument is not picked! 
        '''

        #----------------Process any incoming data---------------#

        # Melody container object
        newMelody = melody()

        if dataType is not None and data is not None:
            print("\nProcessing incoming data...")
            # If ints, scale as necessary
            if dataType == 1:
                # Save original source data
                newMelody.sourceData = data
                data = self.scaleTheScale(data)

            # If floats then convert to ints and scale
            elif dataType == 2:
                # Save original source data
                newMelody.sourceData = data
                data = self.floatToInt(data)
                data = self.scaleTheScale(data)

            # If letters/chars then match letters to their corresponding index numbers.
            elif dataType == 3:
                # Save original source data
                newMelody.sourceData = data
                data = self.mapLettersToNumbers(data)

            # If hex convert to array of ints and scale
            elif dataType == 4:
                # Converts hex number to string, then saves
                # that as the first item of a list. It's silly, I know.
                data = str(data)
                # Save original source data
                newMelody.sourceData.append(data)
                data = self.hexToIntList(data)
            else:
                print("\nnewMelody() - ERROR: dataType value out of range!")
                return -1
        else:
            # Otherwise just add single string to list
            newMelody.sourceData.append('None Inputted')

        #-----------------------Generate!------------------------#

        # Pick tempo
        if tempo == None:
            newMelody.tempo = self.newTempo()
        else:
            newMelody.tempo = tempo
        # Pick notes    
        if data is None:
            newMelody.notes, newMelody.fn, newMelody.sourceScale = self.newNotes()
            if newMelody.notes == -1:
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1
        else:
            newMelody.notes, newMelody.fn, newMelody.sourceScale = self.newNotes(data)
        # Pick rhythms
        newMelody.rhythms = self.newRhythms(len(newMelody.notes), newMelody.tempo)
        # Pick dynamics
        newMelody.dynamics = self.newDynamics(len(newMelody.notes))

        return newMelody


    #-------------------------------------------------------------------------------------#
    #-------------------------------COMPOSITION GENERATION--------------------------------#
    #-------------------------------------------------------------------------------------#


    # Wrapper for newMelody() method. 
    # Exports MIDI file + generates title + .txt data file
    def aNewMelody(self, data=None, dataType=None):
        '''
        Wrapper for the newMelody() method. 
        Exports MIDI file + generates title + .txt data file. 
        Returns 0 on succcess, -1 on failure.
        '''
        # apply data and dataType as necessary
        if data is not None and dataType is not None:
            tempo = c.TEMPOS[randint(0, len(c.TEMPOS) - 1)]
            newTune = self.newMelody(tempo, data, dataType)
        else:
            tempo = c.TEMPOS[randint(0, len(c.TEMPOS) - 1)]
            newTune = self.newMelody(tempo=tempo)
        # Pick instrument
        newTune.instrument = self.newInstrument()
        # Generate title
        title = self.newTitle()
        # Create MIDI file name
        title1 = title + '.mid'
        # Save to MIDI file
        if m.saveMelody(self, title1, newTune) != -1:
            print('')  
        else:
            print("\n\naNewMelody() - ERROR: Unable to export piece to MIDI file!")
            return -1
        # Save composition data to a .txt file (fileName)
        fileName = "{}{}".format(title, '.txt')
        title2 = "{}{}{}{}".format(title, ' for ', newTune.instrument, ' and piano')
        print("\nNew melody title:", title2)
        saveInfo(title2, data, fileName, newTune)
        return 0

    # Wrapper for newChords(). Outputs chords as a MIDI file and
    # exports a .txt file with relevant data
    def newProgression(self, total=None, tempo=None, sourceScale=None):
        '''
        Wrapper for newChords(). Outputs chords as a MIDI file and
        exports a .txt file with relevant data. 
        
        Needs *ALL* required data or none. No in-between at the moment.
        
        Returns a list of chord() objects
        '''
        if total is None:
            total = randint(3, 15)
        elif tempo is None:
            tempo = self.newTempo()
        elif sourceScale is None:
            sourceScale = self.newNotes()
        chords = self.newChords(total, tempo, sourceScale)
        # generate title
        title = self.newTitle()
        # create MIDI file name
        title1 = title + '.mid'
        # save to MIDI file
        if m.saveChords(self, title, chords) != -1:
            print("\nMIDI file saved as:", title1)
        else:
            print("\nnewProgression() - ERROR: unable to save MIDI file!")
            return -1
        # export to .txt file
        saveInfo(name=title, data=sourceScale, fileName=title1, newChords=chords)
        return chords

    # Outputs a single melody with chords in a MIDI file
    def newComposition(self, data=None, dataType=None):
        '''
        Takes an 0x-xxxxxx hex humber representing a color, or 
        an array of ints, floats or chars of any length as arguments, 
        plus the data type represented by a int 
        (int (1), float (2), char (3), or hex number (4)). Or nothing at all!

        Outputs a single melody with chords in a MIDI file, as
        well as a .txt file with the compositions title, inputted data, 
        auto-generated title, a random instrumentation, with the date and time
        of generation. Also contains melody and harmony data.
        '''

        # Generate a melody
        if data is not None and dataType is not None:
            newTune = self.newMelody(data, dataType)
            if newTune == -1:
                print("newComposition() - ERROR: unable to generate melody!")
                return -1
            newTune.instrument = self.newInstrument()

        else:
            newTune = self.newMelody()
            if newTune == -1:
                print("newComposition() - ERROR: unable to generate melody!")
                return -1
            newTune.instrument = self.newInstrument()

        # Generate harmonies from this melody
        newChords = self.newChords(len(newTune.notes), newTune.tempo, newTune.notes)
        if newChords == -1:
            print("\nnewComposition() - ERROR: unable to generate harmonies!")
            return -1
        
        # Expot MIDI file
        title = self.newTitle()
        title1 = title + '.mid'
        if m.saveComposition(self, newTune, newChords, title1) != -1:
            print("\nMIDI file saved as:", title1)
        else:
            print("\nnewComposition() - ERROR: Unable to export piece to MIDI file!")
            return -1

        #Save composition data to a .txt file (fileName)-
        fileName = "{}{}".format(title, '.txt')
        print("\nText file saved as:", fileName)
        title2 = "{}{}{}{}".format(title, ' for ', newTune.instrument, ' and piano')
        print("\nTitle:", title2)
        saveInfo(title, newTune.sourceData, fileName, newTune, newChords)

        return abc(title, newTune.tempo, newTune, newChords)