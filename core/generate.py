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
import requests
import urllib.request
import core.constants as c
import utils.midi as m
from utils.mapping import mapData
from utils.toabc import abc
from utils.save import saveInfo
from random import randint, sample
from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition
from datetime import datetime as date


# Generative functions
class Generate():
    '''
    This class handles all generative functions.
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

    # Auto generate a random composer name
    def newComposer(self):
        '''
        Generate a random composer name (1-3 names)
        '''
        try:
            # get word list
            url = "https://svnweb.freebsd.org/csrg/share/dict/propernames?revision=61766&view=co"
            # response = requests.get(url)
            response = urllib.request.urlopen(url)
            # decode data to text string
            text = response.read().decode()
            # separate names into list
            names = text.splitlines()
            # pick 1 to 3 random names
            t = 0
            total = randint(1, 3)
            name = names[randint(0, len(names) - 1)]
            while(t < total):
                name = name + ' ' + names[randint(0, len(names) - 1)]
                t += 1
        except urllib.error.URLError:
            print("\nnewTitle() - ERROR: Unable to retrieve name list!")
            name = 'Rando Calrissian'
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
        # d = date.now()
        # convert to str d-m-y hh:mm:ss
        # dateStr = date.now().strftime("%d-%b-%y %H:%M:%S")
        # combine name, ensemble, and date, plus add file extension
        fileName = '{}{}.mid'.format(title, 
            date.now().strftime("%d-%b-%y %H:%M:%S"))
        return fileName

    # Converts a list of pitch class integers to note strings (with or without an octave)
    def toStr(self, pcs, octave=None):
        '''
        Converts a list of pitch class integers to note name strings, with or without 
        a supplied octave. 
        
        Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
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

    # Transpose
    def transpose(self, pcs, t):
        '''
        Transpose a pitch class set using a supplied interval i, or list of 
        intervals i. Use a list of intervals to generate variations on a 
        given pitch-class set.
        
        Returns a modified pcs (list[int])
        '''
        # modify with a single interval across all pitch-classes
        if type(t) == int:
            for note in range(len(pcs)):
                pcs[note] += t
        # modify with a list of intervals across all pitch-classes. 
        # this allows for each pitch-class to be transposed by a unique
        # distance, allowing for rapid variation generation.
        elif type(t) == list:
            for note in range(len(pcs)):
                pcs[note] += t[note]
        # keep resulting pcs values between 0 and 11
        pcs = self.octaveEquiv(pcs)
        return pcs

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
            instruments.append(c.INSTRUMENTS[randint(0, 110)])
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
    def newNotes(self, data=None, root=None):
        '''
        Generates a set of notes to be used as a melody.

        Can also return a list of notes without any data input. If this is the case,
        then newNotes() will decide how many to generate (between 3 and 50).

        A supplied data list (list[int]) of n length functions as *index numbers* against a generated
        "source scale" to select notes in order to generate a melody. User also has the option to 
        supply a "root" scale, though only if the program is accessing this method directly!
        newMelody() and other methods that call this function don't supply a root if none is 
        chosen by the user.

        Returns a tuple: notes list to be used as a melody (list[str]), 
        a list of forte_numbers (list[str]), and the original source scale (list[str])
        '''           
        # Generate seed scale
        # Save forte numbers and/or pitch class sets
        meta_data = []
        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        # Pick a root scale if none provided
        if root==None:
            root, fn = self.pickScale()
            meta_data.append(fn)
        # Pick total: 3 - 50 if we're generating random notes
        if data == None:
            # Note that the main loop uses total + 1!
            total = randint(2, 49)
        # Or the largest value of the supplied data set
        else:
            total = max(data)
    
        # Generate source scale 
        '''NOTE: this only uses the supplied root scale once!'''
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
                    # Generate another new root scale & 
                    # starting octave + save forte number, if applicable
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

    # Picks a church mode and randomly transposes it
    def pickMode(self, transpose=False, octave=None):
        '''
        Picks a church mode, randomly transposes it (if indicated),
        and appends a specified octave (if needed). 
        
        Returns a tuple: the mode (str), mode pcs (list[int]), 
        and notes (list[str]). 
        '''
        # pick mode
        mode = c.MODE_KEYS[randint(1, len(c.MODE_KEYS) - 1)]
        mode_pcs = c.MODES[mode]
        # transpose?
        if transpose == True:
            # how far?
            t = randint(1, 11)
            mode_pcs = self.transpose(mode_pcs, t)
        # append octave, if necessary, to the final list[str]
        if octave != None:
            mode_str = self.toStr(mode_pcs, octave=octave)
        else:
            mode_str = self.toStr(mode_pcs)
        return mode, mode_pcs, mode_str

    # Picks either a prime form pitch-class set, or a major or minor scale.
    def pickScale(self, octave=None):
        '''
        Picks either 1 of 12 major or minor scales for a tonal flavor, 
        or a 5 to 9 note Forte pitch class prime form for an atonal flavor.

        Returns tuple with a list of note name strings with or without an 
        assigned octave, plus the forte number of the chosen scale.

        NOTE: Add ability to pick mode in random key? Probably.
        '''
        scale = []
        # use a major or minor scale(1), or pick a prime form(2)?
        if randint(1, 2) == 1:
            # pick major
            if randint(1, 2) == 1:
                scale = c.MAJOR_SCALES[randint(1, len(c.MAJOR_SCALES) - 1)]
                fn = "7-35 (" + scale[0] + "major)"
            # pick minor
            else:
                scale = c.MINOR_SCALES[randint(1, len(c.MINOR_SCALES) - 1)]
                fn = "7-35 (" + scale[0] + "minor)"
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
        Returns a randomly generated 5 to 9 note scale with or without an octave 
        to be used as a 'root'. Can take an int as a starting octave 
        (between 2 and 5), or not. 
        
        To be used externally from newNotes() to supply a new "root," as an option
        for the user.
        
        Returns a list of note name strings and the original pitch class set.
        '''
        pcs = []
        total = randint(5, 9)
        while len(pcs) < total:
            # pick pitch class integer
            n = randint(0, 11)
            if n not in pcs:
                pcs.append(n)
        # attempt to use list comprehension in lieu of the loop above
        '''pcs = [randint(0, 11) for x in range(total)]'''
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

    # Generates a long source scale off a given root scale 
    def newSourceScale(self, root):
        '''
        Generates a list[str] "source scale" based off a 
        supplied root (list[str]). Does not pick additional
        roots! Mostly used by external calls.

        Requires a note list (list[str]).
        Returns a list[str] with appended octaves (2-5)
        '''
        n = 0
        o = 2
        scale = []
        for i in range(28):
            note = "{}{}".format(root[n], o)
            scale.append(note)
            n += 1
            if n == 7:
                o += 1
                if o == 6:
                    o = 2
                n = 0
        return scale

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


    # generate a list of 11 intervals to transpose a 12-tone row by to generate
    # a matrix
    def new12ToneIntervals(self):
        '''
        Returns a list of 11 non-repeating intervals to generate 12-tone row
        transpositions.
        '''
        return sample(c.INTERVALS[1], len(c.INTERVALS[1]))

    # Keeps a single pitch within span of an octave (0 - 11)
    def octaveEquiv(self, pitch):
        '''
        Keeps a single pitch within span of an octave (0 - 11). 
        '''
        # check a single pitch
        if type(pitch) == int:
            pitch %= 12
        # check a whole list of pcs integers
        elif type(pitch) == list:
            for i in range(len(pitch)):
                # only modify any ints > 11 or < 0
                if pitch[i] > 11 or pitch[i] < 0:
                    pitch[i] %= 12
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
        Returns a chord() object. Does not assign an instrument!
        '''
        # New chord() object
        newchord = Chord()

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
        supplied list from the user. It can process a list of ints 
        (dataType == 1), floats(2), single char strings/letters(3), 
        or a hex number, represented as a single string(4)

        If no data is supplied, then it will generate a melody anyways. 

        Returns a melody() object if successfull, -1 on failure.

        NOTE: Instrument is *NOT* picked! Needs to be supplied externally.
        '''

        # Melody container object
        newMelody = Melody()

        # Process any incoming data
        if dataType != None and data != None:
            data, newMelody = mapData(newMelody, data, dataType)
            if data != -1 or newMelody != -1:
                print()
            else:
                print("\nnewMelody() - ERROR: unable to map data to integers!")
                return -1
        else:
            # Otherwise just add single string to list
            newMelody.sourceData.append('None Inputted')

        # Pick tempo if none is supplied
        if tempo == None:
            newMelody.tempo = self.newTempo()
        else:
            newMelody.tempo = tempo

        # Pick notes from scratch  
        if data == None:
            newMelody.notes, newMelody.fn, newMelody.sourceScale = self.newNotes()
            if newMelody.notes == -1:
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1
        # Or use supplied data
        elif data != None:
            newMelody.notes, newMelody.fn, newMelody.sourceScale = self.newNotes(data=data)
            if newMelody.notes == -1:
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1

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
            tempo = self.newTempo()
            newTune = self.newMelody(tempo=tempo, data=data, dataType=dataType)
        else:
            tempo = self.newTempo()
            newTune = self.newMelody(tempo=tempo)
        # Pick instrument
        newTune.instrument = self.newInstrument()
        # Generate title
        title = self.newTitle()
        # Create MIDI file name
        midiFileName = title + '.mid'
        # Save to MIDI file
        if m.saveMelody(midiFileName, newTune) != -1:
            print()  
        else:
            print("\n\naNewMelody() - ERROR: Unable to export piece to MIDI file!")
            return -1
        # Save composition data to a .txt file (fileName)
        txtFileName = "{}{}".format(title, '.txt')
        title_full = "{}{}{}{}".format(title, ' for ', newTune.instrument, ' and piano')
        print("\nNew melody title:", title_full)
        saveInfo(title_full, data, txtFileName, newTune)
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
        if m.saveChords(title, chords) != -1:
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
        Generates 1 melody and set of harmonies with our without
        inputted data.
        
        Takes an 0x-xxxxxx hex humber representing a color, or 
        an array of ints, floats or chars of any length as arguments, 
        plus the data type represented by a int 
        (int (1), float (2), char (3), or hex number (4)).

        Outputs a a MIDI file, a .txt file with the compositions data (title, instrumentation,
        notes, etc...). 

        Returns an incomplete Composition() object (no composer data, or ),
        and a str of the compositions's data in abc notation.
        '''
        # Store it in here
        comp = Composition()

        # Generate a melody
        if data is not None and dataType is not None:
            newTune = self.newMelody(data=data, dataType=dataType)
            if newTune == -1:
                print("\nnewComposition() - ERROR: unable to generate melody!")
                return -1
            # pick instrument for melody
            newTune.instrument = self.newInstrument()

        else:
            newTune = self.newMelody()
            if newTune == -1:
                print("\nnewComposition() - ERROR: unable to generate melody!")
                return -1
            # pick instrument for melody
            newTune.instrument = self.newInstrument()
        # Save melody info
        comp.instruments.append(newTune.instrument)
        comp.melodies.append(newTune)

        # Generate harmonies from this melody
        newChords = self.newChords(len(newTune.notes), newTune.tempo, newTune.notes)
        if newChords == -1:
            print("\nnewComposition() - ERROR: unable to generate harmonies!")
            return -1
        # picks KEYBOARD instruments for newChords
        else:
            for i in range(len(newChords)):
                newChords[i].instrument = c.INSTRUMENTS[randint(0, 8)]
        # Save harmony info (instruments + chord list)
        for i in range(len(newChords)):
            comp.instruments.append(newChords[i].instrument)
        comp.chords = newChords

        # Generate titles and file names
        comp.title = self.newTitle()
        title_full = "{}{}{}{}".format(comp.title, ' for ', 
            newTune.instrument, ' and various keyboards')
        mfn = comp.title + '.mid'
        tfn = comp.title + '.txt'
        comp.midiFileName = mfn
        comp.txtFileName = tfn

        # Save date and time of composition
        comp.date = date.now().strftime("%b-%d-%y %H:%M:%S")

        # Export
        '''NOTE: eventually replace m.saveComposition() with just m.save(comp)'''
        if m.saveComposition(newTune, newChords, mfn) != -1 and saveInfo(
            name=comp.title, data=newTune.sourceData, fileName=tfn, 
            newMelody=newTune, newChords=newChords) == 0:
            # Display results
            print("\nTitle:", title_full)
            print("\nMIDI file saved as:", mfn)
            print("\nText file saved as:", tfn)
            
            # Returns composition() object and comp data in abc notation (str)!
            return comp, abc(comp.title, newTune.tempo, newTune, newChords)

        else:
            print("\nnewComposition() - ERROR: Unable to export files!")
            return -1

        