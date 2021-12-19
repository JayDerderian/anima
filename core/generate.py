'''
This module handles all generative methods. 
'''

# IMPORTS
import math
import urllib.request
from datetime import datetime as date
from random import randint, sample, choice

from core.constants import(
    NOTES,
    PITCH_CLASSES, 
    RHYTHMS, 
    REST,
    DYNAMICS, 
    TEMPOS, 
    INSTRUMENTS,
    SCALES,
    SCALE_KEYS,
    ARPEGGIOS,
    SETS,
    FORTE_NUMBERS,
    INTERVALS
)

from utils.mapping import map_data
from utils.txtfile import save_info
from utils.midi import save
from utils.tools import tostr, transpose, oe, scaletotempo

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

    #------------------------------------------------------------------------------------------#
    #-----------------------------------TITLE AND COMPOSER-------------------------------------#
    #------------------------------------------------------------------------------------------#


    # Auto generate a composition title from two random words
    def new_title(self):
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
            name = choice(words)
            while(t < total):
                name = name + ' ' + choice(words)
                t += 1
        except urllib.error.URLError:
            print("\nnew_title() - ERROR: Unable to retrieve word list!")
            name = 'untitled - '
        return name


    # Auto generate a random composer name
    def new_composer(self):
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
            # pick 1 to 4 random names
            t = 0
            total = randint(1, 3)
            name = choice(names)
            while(t < total):
                name = name + ' ' + choice(names)
                t += 1
        except urllib.error.URLError:
            print("\nnew_composer() - ERROR: Unable to retrieve name list!")
            name = 'Rando Calrissian'
        return name

    # Intialize a new composition object/form
    def init_comp(self, tempo=None, composer=None):
        '''
        Initializes a Composition() object by creating
        the title, composer name
        '''
        comp = Composition()
        comp.title = self.new_title()
        if composer==None:
            comp.composer = self.new_composer()
        else:
            comp.composer = composer
        comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
        if tempo==None:
            comp.tempo = self.new_tempo()
        elif tempo > 40.0 or tempo < 208.0:
            comp.tempo = tempo
        else:
            comp.tempo = 60.0
        comp.midi_file_name = comp.title + ".mid"
        comp.txt_file_name = comp.title + ".txt"
        return comp


    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def new_tempo(self):
        '''
        Picks tempo (float) between 40-208bpm.
        '''
        return choice(TEMPOS)


    #--------------------------------------------------------------------------------#
    #----------------------------------Instruments-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks an instrument
    def new_instrument(self):
        '''
        Randomly picks a melodic/harmonic instrument from a given list. Returns a string.
        Does NOT pick a percussion instrument!
        '''
        return INSTRUMENTS[randint(0, 110)]


    # Picks a collection of instruments of n length.
    def new_instruments(self, total):
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
    def new_note(self, i=None, octave=None):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6), 
        or randomly picks a note between octaves 2 to 5. Returns a single 
        string (i.e. "C#4"), or -1 on failure.

        NOTE: use randint(0, 11) and randint(2, 5) for num/octave args to get a 
              randomly chosen note, or leave arg fields empty 
        '''
        if i==None:
            note = choice(PITCH_CLASSES)
        elif type(i) == int and i > -1 and i < len(PITCH_CLASSES):
                note = PITCH_CLASSES[i]
        else:
            return -1
        if octave==None:
            octave = randint(2, 5)
        note = "{}{}".format(note, octave)
        return note    


    # Generate a series of notes based off an inputted array of integers
    def new_notes(self, data=None, root=None, t=None):
        '''
        NOTE: modify to accomodate a specified instrument's range!

        Generates a set of notes to be used as a melody. Can also
        use a specified root scale, and a specified note total.

        Can also return a list of notes without any input. If this is the case,
        newNotes() will decide how many to generate (between 3 and 50).

        Data that can be used: 
            A supplied data list (list[int]) of n length functions as *index numbers* 
            against a generated "source scale" to select melody notes. 
        
        User also has the option to  supply a "root" scale, though only if the program 
        is accessing this method directly! newMelody() and other methods that call this 
        function don't supply a root if none is chosen by the user.

        Returns a tuple: 
            notes list to be used as a melody (list[str]), 
            note meta data (list[str]),
            original source scale (list[str])
        '''           
        # Generate seed scale
        # Save forte numbers and/or pitch class sets
        meta_data = []
        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        # Pick a root scale if none provided
        if root==None:
            root, info = self.pick_root(t=True, o=None)
            meta_data.append(info)
        # Pick total: 3 - 30 if we're generating random notes
        if data==None:
            # Note that the main loop uses total + 1!
            if t==None:
                total = randint(2, 29)
            else:
                total = t
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
                    root, info = self.pick_root(t=True, o=None)
                    meta_data.append(info)
                # Reset n to stay within len(root)
                n = 0

        # Randomly pick notes from the generated source scale to 
        # create an arhythmic melody.
        notes = []
        if data==None:
            # Total notes in melody will be between 3 and 
            # however many notes are in the source scale
            if t == None:
                total = randint(3, len(scale))
            else:
                total = randint(t-2, t)
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
    def pick_root(self, t=True, o=None):
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
                mode, pcs, scale = self.pick_scale(t=True)
                info = '{} {}'.format(scale[0], mode)
            else:
                mode, pcs, scale = self.pick_scale(t=False)
                info = '{} {}'.format(scale[0], mode)
        else:
            if t==True:
                fn, pcs, scale = self.pick_set(t=True)
                info = '{} transposed to new root: {}'.format(fn, scale[0])
            else:
                fn, pcs, scale = self.pick_set(t=False)
                info = '{} untransposed, root: {}'.format(fn, scale[0])
        scale = tostr(pcs, octave=o)
        return scale, info     


    # Picks a scale and randomly transposes it
    def pick_scale(self, t=True, o=None):
        '''
        Picks a scale, randomly transposes it (if indicated),
        and appends a specified octave (if needed). 
        
        Returns a tuple: the scale name (str), untransposed scale pcs 
        (list[int]), and note list (list[str]) *without assigned octave by default.* 
        '''
        scale = choice(SCALE_KEYS)
        pcs = SCALES[scale]
        if t==True:
            pcs_t = transpose(pcs, randint(1, 11), octeq=False)
            notes = tostr(pcs_t, octave=o)
        else:
            notes = tostr(pcs, octave=o)
        return scale, pcs, notes


    # Picks a prime form pitch class set and transposes it
    # n semi-tones
    def pick_set(self, t=True, o=None):
        '''
        Selects prime form and transposes a random distance (or not)
        
        Returns a tuple: forte number/fn (str), untransposed prime form pcs (list[int]), 
        note list (list[str]) *without an assigned octave*
        '''
        fn = choice(FORTE_NUMBERS)
        pcs = SETS[fn]
        if t==True:
            pcs_t = transpose(pcs, randint(1, 11), octeq=False)
            scale = tostr(pcs_t, octave=o)
        else:
            scale = tostr(pcs, octave=o)
        return fn, pcs, scale
        

    # Generate a new scale
    def new_scale(self, octave=None):
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
        scale = tostr(pcs, octave)
        return scale, pcs   


    # Generates a long source scale off a given root scale 
    def new_source_scale(self, root, o=None):
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
            if n == len(root):
                o += 1
                if o == 6:
                    o = 2
                n = 0
        return scale


    # Generate derivative scales based on each note in a given scale.
    def deriveScales(self, pcs, o=None):
        '''
        Generate derivative scales based on each note in a given scale.
        Requires a pitch class set (pcs) list[int] who's values are 
        between 0 - 11, and returns a dictionary of variant scales (list[str])
        
        Each variant scale will have an assigned octave, with or without
        user input.
        
        1. Start with first note in pitch class set (pcs).
        
        2. Derive each subsequent note by adding a randomly
           chosen value to the sum of the previous

           n0+=rand(1,3), n1 = n0+=rand(1,3), n2 = n1+=rand(1,3), etc...  
        
        3. Repeat step 2 with next note in supplied pcs up to end of scale.        
        '''
        variants = {}
        for i in range(len(pcs)):
            sv = []
            note = pcs[i]
            while len(sv) < len(pcs):
                note += randint(1, 3)
                sv.append(note)
            variants[i] = sv
        # convert to strings with appended octave
        # tostr() handles whether or not o==None
        for scale in variants:
            variants[scale] = tostr(variants[scale], octave=o, octeq=False)
        return variants


    # Pick an arpeggio scheme (within 1 octave)
    def pick_arp(self, key):
        '''
        Returns a list[int] of pitch classes outlining a one-octave
        arpeggio.
        '''
        return ARPEGGIOS[key]


    # Generate a 12-tone row.
    def new_12tone_row(self):
        '''
        Generates a 12-tone row. Returns a note list[str].
        Notes don't have an assigned octave.
        '''
        return sample(PITCH_CLASSES, len(PITCH_CLASSES))


    # generate a list of 11 intervals to transpose a 12-tone row by to generate
    # a matrix
    def new_12tone_intervals(self):
        '''
        Returns a list of 11 non-repeating intervals to generate 12-tone row
        transpositions.
        '''
        return sample(INTERVALS[1], len(INTERVALS[1]))


    # reverses a melody and appends to end to create a palindrome
    # of the current part
    def new_palindrome(m):
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
    def new_rhythm(self):
        '''
        Generates a single new rhythm. Not scaled to current tempo!
        '''
        return choice(RHYTHMS)


    # Generate a list containing a rhythmic pattern
    def new_rhythms(self, total=None, tempo=None):
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
        # scale to given tempo, if provided and necessary.
        if tempo!=None and tempo!=60.0:
            rhythms = scaletotempo(tempo, rhythms)
        return rhythms


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Generate a single dynamic 
    def new_dynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        return choice(DYNAMICS)


    # Generate a list of dynamics.
    def new_dynamics(self, total=None):
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
    def display_chord(self, chord):
        print("\n------------Chord:-------------")
        print("\nnotes:", chord.notes)
        print("rhythm:", chord.rhythm)
        print("dynamic:", chord.dynamic)


    # Display a list of chords
    def display_chords(self, chords):
        print("\n----------------HARMONY DATA:-------------------")
        for i in range(len(chords)):
            print('\n', i + 1, ': ', 'Notes:', chords[i].notes)
            print('      Rhythm:', chords[i].rhythm)
            print('      Dynamics:', chords[i].dynamic)


    # get total duration of a list of chords
    def chord_durations(self, chords):
        '''
        Returns the total length  in seconds (float) of a series 
        of chord() objects (chord progression).
        '''
        d = 0.0
        for j in range(len(chords)):
            d += chords[j].rhythm
        return d


    # Generates a chord with randomly chosen notes
    def new_chord(self, tempo=None, scale=None):
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
            if randint(1, 2) == 1:
                scale, newchord.info = self.pick_root(o=randint(2,5))
            else:
                scale, newchord.info = self.new_scale(octave=randint(2,5))
        # save original scale
        newchord.source_notes = scale
        # how many notes in this chord?
        total = randint(2, 9)
        # pick notes and add to list (allows for doublings)
        while len(newchord.notes) < total:
            newchord.notes.append(choice(scale))
        # pick a rhythm and scale if needed
        rhythm = self.newRhythm()
        if newchord.tempo != 60:
            rhythm = scaletotempo(newchord.tempo, rhythm)
        newchord.rhythm = rhythm
        # pick a dynamic
        newchord.dynamic = self.new_dynamic()
        return newchord


    # Generates a series of random chromatic chords 
    def new_chords(self, total=None, tempo=None, scale=None):
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
            tempo = self.new_tempo()
        if scale==None:
            scale, data, source = self.new_notes()
        # Pick chords
        while len(chords) < total:
            newchord = self.new_chord(tempo, scale)
            chords.append(newchord)
        return chords


    # Generates a list of triads from a given scale
    def new_triads(self, scale, t=None):
        '''
        generates a list of triads of t length from a given multi-octave
        source scale. a single octave scale will only yield 3 triads since
        the third chord will pick the last element in the list..
        
        ideally a list[str] of note chars in at least two octaves will 
        be supplied.
        
        picks notes by accessing every other index three times.

        returns a list of chord() objects. if t is not supplied, then
        it will generate as many chords as it can until an IndexError 
        exception is raised.

        NOTE: chords dont have tempo or instrument assigned!'''
        triads = []
        for i in range(len(scale)):
            triad = Chord()
            try:
                triad.notes = [scale[i], scale[i+2], scale[i+4]]
            except IndexError:
                break
            triad.rhythm = 2.0
            triad.dynamic = 100
            triads.append(triad)
            if type(t) == int and len(triads) == t:
                break
        return triads


    # Generate a chord off a given interval i (between 1 and 6) to total notes for the chord n
    # starting with root r (integer)
    def new_sym_triad(self, r, i, n):
        '''
        generates an intervallicly symmetrical chord of n length 
        based off a given root (r) and interval (i). 
        
        returns a list[int] between 0 - 11 of n length. 
        
        Returns -1 if given interval is invalid.
        '''
        if i > 6 or i < 1:
            return -1
        if n < 0:
            return -1
        if r > 11 or r < 0:
            r = oe(r)
        chord = []
        while len(chord) < n:
            chord.append(r)
            r += i
            if r > 11:
                r = oe(r)
        return chord


    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    # Display newMelody() object data
    def display_melody(self, m):
        '''
        Displays newMelody() object data
        '''
        print("\n-----------MELODY Data:------------")
        print("\nTempo:", m.tempo, "bpm")
        print("\nInstrument:", m.instrument)
        print("\nSource data:", m.sourceData)
        print("\nInfo:", m.info)
        print("\nTotal Notes:", len(m.notes))
        print("Notes:", m.notes)
        print("\nTotal rhythms:", len(m.rhythms))
        print("Rhythms:", m.rhythms)
        print("\nTotal dynamics:", len(m.dynamics))
        print("Dynamics:", m.dynamics)

    # Generate a melody from an array of integers (or not).
    def new_melody(self, tempo=None, data=None, dt=None):
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
        if dt != None and data != None:
            data, m = map_data(m, data, dt)
        else:
            # Otherwise just add single string to list
            m.source_data ='None Inputted'

        # Pick tempo if none is supplied
        if tempo==None:
            m.tempo = self.new_tempo()
        else:
            m.tempo = tempo

        # Pick notes from scratch  
        if data==None:
            m.notes, m.info, m.source_scale = self.new_notes()

        # Or use supplied data
        else:
            m.notes, m.info, m.source_scale = self.new_notes(data=data)

        # Pick rhythms
        m.rhythms = self.new_rhythms(len(m.notes), m.tempo)
        # Pick dynamics
        m.dynamics = self.new_dynamics(len(m.notes))

        return m


    #-------------------------------------------------------------------------------------#
    #-------------------------------COMPOSITION GENERATION--------------------------------#
    #-------------------------------------------------------------------------------------#


    # Outputs a single melody with chords in a MIDI file
    def new_composition(self, data=None, dt=None):
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
        comp.title = self.new_title()
        comp.composer = self.new_composer()
        comp.tempo = self.new_tempo()
        comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
        comp.ensemble = 'duet'
        comp.midi_file_name = comp.title + '.mid'
        comp.txt_file_name = comp.title + '.txt'
        
        # Generate a melody
        if data != None and dt != None:
            m = self.new_melody(tempo=comp.tempo, data=data, dataType=dt)
            # pick instrument for melody
            m.instrument = self.new_instrument()
            comp.instruments.append(m.instrument)

        else:
            m = self.new_melody(tempo=comp.tempo)
            # pick instrument for melody
            m.instrument = self.new_instrument()
            comp.instruments.append(m.instrument)

        # Save melody info
        comp.melodies.append(m)

        # Generate harmonies from this melody
        ch = self.new_chords(total=len(m.notes), tempo=comp.tempo, scale=m.notes)
        # pick keyboard instrument and apply to all chord objects
        instr = INSTRUMENTS[randint(0, 8)]
        for i in range(len(ch)):
            ch[i].instrument = instr
        # save instrument to comp instr list
        comp.instruments.append(instr)
        # Save keyboard part part to chord dictionary
        comp.chords[0] = ch

        # Full title
        title_full = "{}{}{}{}".format(comp.title, ' for ', 
            m.instrument, ' and various keyboards')

        # Export MIDI & text file, then display results
        if save(comp)!=-1 and save_info(name=comp.title, 
            fileName=comp.txt_file_name, newMusic=comp)==0:
            print("\ntitle:", title_full)
            print("composer:", comp.composer)
            print("date:", comp.date)
            print("duration:", comp.duration())
            print("midi file:", comp.midi_file_name)
            print("text file:", comp.txt_file_name)
            return comp
        else:
            print("\nnoooooooooooooooooooooo!!!!")
            return -1