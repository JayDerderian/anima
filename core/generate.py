'''
This module handles all generative methods. 
'''

# IMPORTS
import math
import urllib.request

from core.constants import(
    NOTES, 
    RHYTHMS, 
    DYNAMICS, 
    TEMPOS, 
    INSTRUMENTS,
    MODES,
    MODE_KEYS,
    ARPEGGIOS,
    SCALES,
    FORTE_NUMBERS,
    PITCH_CLASSES,
    INTERVALS
)

from random import randint, sample, choice
from datetime import datetime as date

from utils.mapping import mapData
from utils.toabc import abc
from utils.txtfile import saveInfo
from utils.midi import save, saveChords

from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition


# Generative functions
class Generate:
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
            # name = words[randint(0, len(words) - 1)]
            name = choice(words)
            while(t < total):
                # name = name + ' ' + words[randint(0, len(words) - 1)]
                name = name + ' ' + choice(words)
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
            # name = names[randint(0, len(names) - 1)]
            name = choice(names)
            while(t < total):
                # name = name + ' ' + names[randint(0, len(names) - 1)]
                name = name + ' ' + choice(names)
                t += 1
        except urllib.error.URLError:
            print("\nnewComposer() - ERROR: Unable to retrieve name list!")
            name = 'Rando Calrissian'
        return name


    # Converts a list of pitch class integers to note strings (with or without an octave)
    def toStr(self, pcs, octave=None, oe=True):
        '''
        Converts a list of pitch class integers to note name strings, with or without 
        a supplied octave. 
        
        Returns a list of strings representing pitches, i.e. C#, Gb or D5, Ab6, etc.
        '''
        scale = []
        if oe==True:
            if octave != None:
                for i in range(len(pcs)):
                    note = "{}{}".format(NOTES[pcs[i]], octave)
                    scale.append(note)
            else:
                for i in range(len(pcs)):
                    scale.append(NOTES[pcs[i]])
        return scale

    # Transpose
    def transpose(self, pcs, t, oe=True):
        '''
        Transpose a pitch class or list of pitch classes (list[int]) 
        using a supplied interval i, or list of intervals i. 
        
        Returns a modified pcs (list[int]) or modified pitch class (int),
        depending on input.
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
        # keep resulting pcs values between 0 and 11, if desired.
        if oe==True:
            pcs = self.oe(pcs)
        return pcs

    # Convert base rhythms to values in a specified tempo
    def scaletotempo(self, tempo, rhythms):
        '''
        A rhythm converter function to translate durations in self.rhythms (list)
        or self.rhythm (float) to actual value in seconds for a specified tempo. 
        
        ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

        60/72 = .83 - The result becomes the converter value to multiply all supplied
        durations against to get the new tempo-accurate durations in seconds.

        NOTE: the round() method keeps the results within three decimal places  
        '''
        diff = 60/tempo
        # is this a single float?
        if type(rhythms) == float:
            rhythms *= diff
            rhythms = round(rhythms, 3)
        # or a list of floats?
        elif type(rhythms) == list:
            for i in range(len(rhythms)):
                rhythms[i] *= diff
                rhythms[i] = round(rhythms[i], 3)
        return rhythms    


    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo (float) between 40-208bpm.
        '''
        return choice(TEMPOS)


    #--------------------------------------------------------------------------------#
    #----------------------------------Instruments-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks an instrument
    def newInstrument(self):
        '''
        Randomly picks a melodic/harmonic instrument from a given list. Returns a string.
        Does NOT pick a percussion instrument!
        '''
        return INSTRUMENTS[randint(0, 110)]

    # Picks a collection of instruments of n length.
    def newInstruments(self, total):
        '''
        Generates a list of instruments of n length, where n is supplied from elsewhere.
        Returns a list.
        '''
        instruments = []
        while len(instruments) < total:
            instruments.append(INSTRUMENTS[randint(0, 110)])
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
        if i==None:
            note = choice(NOTES)
        elif type(i) == int and i > -1 and i < len(NOTES):
                note = NOTES[i]
        else:
            return -1
        if octave==None:
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
            root, info = self.pickRoot(t=True, o=None)
            meta_data.append(info)
        # Pick total: 3 - 50 if we're generating random notes
        if data==None:
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
                    # pick new root
                    root, info = self.pickRoot(t=True, o=None)
                    meta_data.append(info)
                # Reset n to stay within len(root)
                n = 0

        # Randomly pick notes from the generated source scale to 
        # create an arhythmic melody.
        notes = []
        if data==None:
            # Total notes in melody will be between 3 and 
            # however many notes are in the source scale
            total = randint(3, len(scale))
            for i in range(total):
                notes.append(choice(scale))

        # ...Or pick notes according to integers in data array
        else:
            # Total number of notes is equivalent to the 
            # number of elements in the data set
            for i in range(len(data)):
                notes.append(scale[data[i]])

        return notes, meta_data, scale


    # Picks either a prime form pitch-class set, or a major or minor scale.
    def pickRoot(self, t=True, o=None):
        '''
        Picks either a randomly chosen and transposed chuch mode or a 5 to 9 
        note Forte pitch class prime form, randomly transposed as well. Set t
        to false if untransposed root is preferred.

        Returns tuple with a list[str] of note name strings, with or without an 
        assigned octave, plus info (str) about the chosen scale.
        '''
        # use mode? (1), or prime form (2)?
        if randint(1, 2) == 1:
            if t==True:
                mode, pcs, scale = self.pickMode(t=True)
                info = '{}{}'.format(scale[0], mode)
            else:
                mode, pcs, scale = self.pickMode(t=False)
                info = '{}{}'.format(scale[0], mode)
        else:
            if t==True:
                fn, pcs, scale = self.pickScale(t=True)
                info = '{} transposed to new root:{}'.format(fn, scale[0])
            else:
                fn, pcs, scale = self.pickScale(t=False)
                info = '{} untransposed, root:{}'.format(fn, scale[0])
        scale = self.toStr(pcs, octave=o)
        return scale, info     


    # Picks a church mode and randomly transposes it
    def pickMode(self, t=True, o=None):
        '''
        Picks a church mode, randomly transposes it (if indicated),
        and appends a specified octave (if needed). 
        
        Returns a tuple: the mode (str), untransposed mode pcs (list[int]), 
        and note list (list[str]) *without assigned octave by default.* 
        '''
        # pick mode
        mode = choice(MODE_KEYS)
        pcs = MODES[mode]
        if t==True:
            pcs_t = self.transpose(pcs, randint(1, 11), oe=True)
            notes = self.toStr(pcs_t, octave=o)
        else:
            notes = self.toStr(pcs, octave=o)
        return mode, pcs, notes


    # Picks a prime form pitch class set and transposes it
    # n semi-tones
    def pickScale(self, t=True, o=None):
        '''
        Selects prime form and transposes a random distance (or not)
        
        Returns a tuple: forte number/fn (str), untransposed prime form pcs (list[int]), 
        note list (list[str]) *without an assigned octave*
        '''
        # pick prime form pitch-class set
        fn = choice(FORTE_NUMBERS)
        pcs = SCALES[fn]
        if t==True:
            pcs_t = self.transpose(pcs, randint(1, 11), oe=True)
            scale = self.toStr(pcs_t, octave=o)
        else:
            scale = self.toStr(pcs, octave=o)
        return fn, pcs, scale
        

    # Generate a new scale
    def newScale(self, octave=None):
        '''
        Returns a randomly generated 5 to 9 note scale with or without an octave 
        to be used as a 'root'. Can take an int as a starting octave 
        (between 2 and 5), or not. 
        
        To be used externally from newNotes() to supply a new "root," as an option
        for the user.
        
        Returns a tuple: notes (list[str]) and the original pitch class set, (list[int]).
        '''
        pcs = []
        total = randint(5, 9)
        '''Current method. Outputs are quite interesting, though I think this
           is the least efficient way to go about this...'''
        while len(pcs) < total:
            n = randint(0, 11)
            if n not in pcs:
                pcs.append(n)
        '''Trying to create a list comprehension version of the above loop...'''
        # pcs = [randint(0,11) for x in range(total) if x not in pcs]
        # sort in ascending order
        pcs.sort()
        # convert to strings (with or without supplied octave)
        scale = self.toStr(pcs, octave)
        return scale, pcs   

    # Generates a long source scale off a given root scale 
    def newSourceScale(self, root):
        '''
        Generates a list[str] "source scale" based off a 
        supplied root (list[str]). 
        
        Does not pick additional roots! Mostly used by other methods.
        Don't call directly.

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
                    note = self.oe(note)
                sv.append(note)
            #scaleVariant = list(set(scaleVariant)) # Remove duplicates
            #scaleVariant.sort() #Sort new derived scale 
            variants[i] = sv
        
        # convert to strings and append octaves here???

        return variants

    # Pick an arpeggio scheme (within 1 octave)
    def pickArp(self, key):
        '''
        Returns a list[int] of pitch classes outlining a one-octave
        arpeggio.
        '''
        return ARPEGGIOS[key]

    # Generate a 12-tone row.
    def new12ToneRow(self, octave=None):
        '''
        Generates a 12-tone row. 

        Returns a tuple: a list[str] of notes in octave 4 by default,
        or in a specified octave (2-5), and the original pitch class set 
        (list[int]).
        '''
        pcs = sample(PITCH_CLASSES, len(PITCH_CLASSES))
        if octave==None:
            row = self.toStr(pcs, octave=4)
        else:
            row = self.toStr(pcs, octave)
        return row, pcs


    # generate a list of 11 intervals to transpose a 12-tone row by to generate
    # a matrix
    def new12ToneIntervals(self):
        '''
        Returns a list of 11 non-repeating intervals to generate 12-tone row
        transpositions.
        '''
        return sample(INTERVALS[1], len(INTERVALS[1]))

    # Keeps a single pitch within span of an octave (0 - 11)
    def oe(self, pitch):
        '''
        Octave equivalance. Handles either a single int or list[int].
        Keeps a single pitch class integer within span of an octave (0 - 11). 

        Returns either a modified int or list[int]
        '''
        # check a single pitch
        if type(pitch) == int:
            pitch %= 12
        # check a whole list of pcs integers
        elif type(pitch) == list:
            for i in range(len(pitch)):
                if pitch[i] > 11 or pitch[i] < 0:
                    pitch[i] %= 12
        return pitch

    # reverses a melody and appends to end to create a palindrome
    # of the current part
    def newPalindrome(m):
        '''
        Takes either a list of chord() objects or a single melody() 
        object, and creates a palindrome from it. 
        
        Returns either a modified list[chord()], or modified melody()'''
        # chord() list
        if type(m) == list:
            mr = m
            mr.reverse()
            m.extend(mr)
        # melody() object
        else:
            end = len(m.notes)-1
            while end > -1:
                m.notes.append(m.notes[end])
                m.rhythms.append(m.rhythms[end])
                m.dynamics.append(m.dynamics[end])
                end-=1
        return m 


    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#


    # Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm. Not scaled to current tempo!
        '''
        return choice(RHYTHMS)

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
        if total==None:
            total = randint(3, 30)
        while len(rhythms) < total:
            # Pick rhythm and add to list
            rhythm = choice(RHYTHMS)
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
                # if rhythm not in rhythms:
                    rhythms.append(rhythm)
        # convert to given tempo, if provided.
        if tempo!=None and tempo!=60.0:
            rhythms = self.scaletotempo(tempo, rhythms)
        return rhythms


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Generate a single dynamic 
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        return choice(DYNAMICS)

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
        if total==None:
            total = randint(3, 30)
        while len(dynamics) < total:
            # Pick dynamic
            dynamic = choice(DYNAMICS)
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
                # if dynamic not in dynamics:
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
        print("dynamic:", chord.dynamic)

    # Display a list of chords
    def displayChords(self, chords):
        print("\n----------------HARMONY DATA:-------------------")
        for i in range(len(chords)):
            print('\n', i + 1, ': ', 'Notes:', chords[i].notes)
            print('      Rhythm:', chords[i].rhythm)
            print('      Dynamics:', chords[i].dynamic)


    # get total duration of a list of chords
    def chordDurations(self, chords):
        '''
        Returns the total length  in seconds (float) of a series 
        of chord() objects (chord progression).
        '''
        d = 0.0
        for j in range(len(chords)):
            d += chords[j].rhythm
        return d

    # Generates a chord with randomly chosen notes
    def newChord(self, tempo=None, scale=None):
        '''
        Generates a 2-9 note chord with randomly chosen notes, rhythm, and dynamic
        from either a supplied scale or self-selected or generated one.  
        
        Returns a chord() object. Does not assign an instrument!
        '''
        # new chord() object
        newchord = Chord()
        # add tempo if one isn't supplied
        if tempo==None:
            newchord.tempo = 60.0
        else:
            newchord.tempo = tempo
        # pick or generate a new scale if we don't get one supplied
        if scale==None:
            ch = randint(1, 3)
            if ch == 1:
                scale, newchord.fn = self.pickRoot(o=randint(2,5))
            elif ch == 2:
                mode, mode_pcs, scale = self.pickMode(t=True, o=randint(2,5))
                info = scale[0] + mode
                newchord.fn = info
            else:
                scale = self.newScale(octave=randint(2,5))
        # save original scale
        newchord.sourceNotes = scale
        # how many notes in this chord?
        total = randint(2, 9)
        # pick notes and add to list (allows for doublings)
        while len(newchord.notes) < total:
            newchord.notes.append(choice(scale))
        # this is avoids getting the while loop stuck
        # if there's a lot of repeated notes in the melody
        newchord.notes = list(dict.fromkeys(newchord.notes))
        # pick a rhythm and scale if needed
        rhythm = self.newRhythm()
        if newchord.tempo != 60:
            rhythm = self.scaletotempo(newchord.tempo, rhythm)
        newchord.rhythm = rhythm
        # pick a dynamic
        newchord.dynamic = self.newDynamic()
        return newchord

    # Generates a series of random chromatic chords 
    def newChords(self, total=None, tempo=None, scale=None):
        '''
        Generates a progression from the notes of a given scale.
        Returns a list of chord() objects (5-11 if no total is 
        supplied). Each chord will have 2 to 9 notes in various 
        registers, as well as a unique dynamic and rhythm. 
        
        chord() objects *wont* have assigned instruments!

        NOTE: Chords will be derived from the given scale ONLY! 
              Could possibly add more randomly inserted chromatic 
              tones to give progressions more variance and color. 
        '''
        chords = []
        # Has a scale, tempo, and total been provided?
        if total==None:
            total = randint(5, 11)
        if tempo==None:
            tempo = self.newTempo()
        if scale==None:
            scale, data, source = self.newNotes()
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
        if r > 11 or r < 0:
            r = self.oe(r)
        chord = []
        while len(chord) < n:
            chord.append(r)
            r += i
            if r > 11:
                r = self.oe(r)
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
        m = Melody()

        # Process any incoming data
        if dataType != None and data != None:
            data, m = mapData(m, data, dataType)
            if data != -1 or m != -1:
                print()
            else:
                print("\nnewMelody() - ERROR: unable to map data to integers!")
                return -1
        else:
            # Otherwise just add single string to list
            m.sourceData ='None Inputted'

        # Pick tempo if none is supplied
        if tempo == None:
            m.tempo = self.newTempo()
        else:
            m.tempo = tempo

        # Pick notes from scratch  
        if data == None:
            m.notes, m.fn, m.sourceScale = self.newNotes()
            if m.notes == -1:
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1
        # Or use supplied data
        elif data != None:
            m.notes, m.fn, m.sourceScale = self.newNotes(data=data)
            if m.notes == -1:
                print("\nnewMelody() - ERROR: unable to generate notes!")
                return -1

        # Pick rhythms
        m.rhythms = self.newRhythms(len(m.notes), m.tempo)
        # Pick dynamics
        m.dynamics = self.newDynamics(len(m.notes))

        return m


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
        if data != None and dataType != None:
            tempo = self.newTempo()
            newTune = self.newMelody(tempo=tempo, data=data, dataType=dataType)
        else:
            tempo = self.newTempo()
            newTune = self.newMelody(tempo=tempo)
        newTune.instrument = self.newInstrument()
        title = self.newTitle()
        # midiFileName = title + '.mid'
        # m.saveMelody(midiFileName, newTune)
        # txtFileName = "{}{}".format(title, '.txt')
        title_full = "{}{}{}".format(title, ' for solo ', newTune.instrument)
        print("\nnew melody title:", title_full)
        # saveInfo(title_full, data, txtFileName, newTune)
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
        if total==None:
            total = randint(3, 15)
        elif tempo==None:
            tempo = self.newTempo()
        elif sourceScale==None:
            sourceScale = self.newNotes()
        chords = self.newChords(total, tempo, sourceScale)
        title = self.newTitle()
        print("\ntitle:", title)
        fn = title + '.mid'
        saveChords(title, chords)
        print("\nmidi file:", fn)
        tn = title + '.txt'
        saveInfo(name=title, data=sourceScale, fileName=tn, newChords=chords)
        print("text file:", tn)
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

        Returns a composition() object on success, or -1 on failure.
        '''
        # Initialize
        comp = Composition()
        comp.title = self.newTitle()
        comp.composer = self.newComposer()
        comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
        comp.ensemble = 'duet'
        comp.midiFileName = comp.title + '.mid'
        comp.txtFileName = comp.title + '.txt'
        
        # Generate a melody
        if data != None and dataType != None:
            mel = self.newMelody(data=data, dataType=dataType)
            mel.tempo = comp.tempo
            # pick instrument for melody
            mel.instrument = self.newInstrument()
            comp.instruments.append(mel.instrument)

        else:
            mel = self.newMelody()
            mel.tempo = comp.tempo
            # pick instrument for melody
            mel.instrument = self.newInstrument()
            comp.instruments.append(mel.instrument)

        # Save melody info
        comp.melodies.append(mel)

        # Generate harmonies from this melody
        ch = self.newChords(len(mel.notes), mel.tempo, mel.notes)
        for i in range(len(ch)):
            # picking only various keyboard instruments for now...
            ch[i].instrument = INSTRUMENTS[randint(0, 8)]
            comp.instruments.append(ch[i].instrument)

        # Save chords to chord dictionary
        comp.chords[0] = ch

        # Full title
        title_full = "{}{}{}{}".format(comp.title, ' for ', 
            mel.instrument, ' and various keyboards')

        # Export MIDI & text file, then display results
        if save(comp)!=-1 and saveInfo(name=comp.title, 
            fileName=comp.txtFileName, newMusic=comp)==0:
            print("\ntitle:", title_full)
            print("composer:", comp.composer)
            print("date:", comp.date)
            print("duration:", comp.duration())
            print("midi file:", comp.midiFileName)
            print("text file:", comp.txtFileName)
            return comp
        else:
            print("\nnoooooooooooooooooooooo")
            return -1