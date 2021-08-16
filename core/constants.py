'''
A module for managing all constants used throughout the program. 
'''

# The alphabet. 
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


# Tempos
TEMPOS = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0,  # 1-9 (0-8)
          60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, # 10-18 (9-17)
          92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
          126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, # 28-36 (27-35)
          184.0, 200.0, 208.0]  # 37-39 (36-38)


# Dynamics (MIDI velocities: 0 - 127)
'''NOTE: use indicies 0-8 for soft dynamics only. 9-17 for med, and
         8-26 for loud dynamics'''
DYNAMICS = [20, 24, 28, 32, 36, 40, 44, 48, 52,
            56, 60, 64, 68, 72, 76, 80, 84, 88,
            92, 96, 100, 104, 108, 112, 116, 120, 
            124]


# Base rhythms in seconds at 60bpm (or q = 60). 
# Convert to currect tempo using tempoConvert() when necessary.
'''
Durations in seconds (1 sec = quarter note @ 60bpm)

Current range is from a whole note to 32nd note,
though other values will be added eventually.

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
RHYTHMS = [4.0, 3.0, 2.0, 1.5, 1.0, 
           0.75, 0.5, 0.375, 0.25, 0.125]


# Pitch class integers
PITCH_CLASSES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


'''
NOTE: Spellings were arbitrarily chosen. 
      Probably won't matter much from a MIDI file's POV... maybe
'''
# Chromatic scale
CHROMATIC_SCALE = ["C", "C#", "D", "Eb", "E", "F", 
                   "F#", "G", "G#", "A", "Bb", "B"]


# Notes in all (reasonable) harmonic spellings for 12tet notation
# indicies 0 - 17. To be used specifically by randint()
# when trying to "randomly" pick a note.
NOTES = ["C", "C#", "Db", "D", "D#", "Eb", "E", 
         "F", "F#", "Gb", "G", "G#", "Ab", "A", 
         "A#", "Bb", "B"]



# All 12 major scales
MAJOR_SCALES = {1: ["C", "D", "E", "F", "G", "A", "B"],
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


# All 12 relative/natural minor scales
MINOR_SCALES = {1: ["A", "B", "C", "D", "E", "F", "G"],
                2: ["Bb", "C","Db", "Eb", "F", "Gb", "Ab"],
                3: ["B", "C#", "D", "E", "F#", "G", "A"],
                4: ["C", "D","Eb", "F", "G", "Ab", "Bb"],
                5: ["C#", "D#","E", "F#", "G#", "A", "B"],
                6: ["D", "E", "F", "G", "A", "Bb", "C"],
                7: ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
                8: ["E", "F#", "G", "A", "B", "C", "D"],
                9: ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
                10: ["F#", "G#", "A", "B", "C#", "D", "E"],
                11: ["G", "A", "Bb", "C", "D", "Eb", "F"],
                12: ["G#", "A#", "B", "C#", "D#", "E", "F#"]}


# Interval list/dictonary
'''
Use values to build scales and chords off of. 

ex: build a major scale off note using array values at
    each key value

    note = 0
    scale = []
    intervals = c.INTERVALS[2]
    for i in range(whatever):
        note += intervals[i]
        if note > 11:
            note = self.octEquiv(note)
        scale.append(note)
    return scale

NOTE: Develop interval sets that begin with 2 and end with 2,
      making the next cycle of intervals begin on a tone a half
      step higher than originally.

      "Self-transposing interval sets"

      ex. 
        c, d, e, f#, g, a, bb, c,
        db, eb, f, g, ab, bB, cb, db,
        d, e, f#, g#, a, b, c, d ...ect.  
'''
INTERVALS = {
        # Transposition distances in semi-tones
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        # Major
        2: [2, 2, 1, 2, 2, 2, 1],
        # Natural minor
        3: [2, 1, 2, 2, 1, 2, 2],
        # Melodic minor
        4: [2, 1, 2, 2, 2, 2, 1],
        # Harmonic minor
        5: [2, 1, 2, 2, 1, 3],
        # Whole tone
        6: [2, 2, 2, 2, 2],
        # Octatonic
        7: [2, 1, 2, 1, 2, 1, 2],
        # Major triad
        8: [4, 3],
        # Minor triad
        9: [3, 4],
        # Diminished triad
        10: [3, 3],
        # Augmented triad
        11: [4, 4]
}


'''
A rather large dictionary containing all of Allen Forte's 5 to 9 
note prime form pitch class sets. A corresponding list called FORTE_NUMBERS 
is used with randint() to pick a prime form from the dictionary in pickScale().
The choice using FORTE_NUMBERS can be used to save which number was used for analytical
purposes.

Each integer/pitch class functions as an index number against CHROMATIC_SCALE to 
generate a scale represented by a list of strings (i.e. ["C#4", "D5"... etc]).

Info taken from here: 
https://en.wikipedia.org/wiki/List_of_pitch-class_sets'''

SCALES = {    
    # 5-note sets
    "5-1":      [0,1,2,3,4],
    "5-2A":	    [0,1,2,3,5],
    "5-2B":	    [0,2,3,4,5],
    "5-3A":	    [0,1,2,4,5],
    "5-3B":	    [0,1,3,4,5],
    "5-4A":	    [0,1,2,3,6],
    "5-4B":	    [0,3,4,5,6],
    "5-5A":	    [0,1,2,3,7],
    "5-5B":	    [0,4,5,6,7],
    "5-6A":	    [0,1,2,5,6],
    "5-6B":	    [0,1,4,5,6],
    "5-7A":	    [0,1,2,6,7],
    "5-7B":	    [0,1,5,6,7],
    "5-8":	    [0,2,3,4,6],
    "5-9A":	    [0,1,2,4,6],
    "5-9B":	    [0,2,4,5,6],
    "5-10A":    [0,1,3,4,6],
    "5-10B":    [0,2,3,5,6],
    "5-11A":    [0,2,3,4,7],
    "5-11B":    [0,3,4,5,7],
    "5-z12":    [0,1,3,5,6],
    "5-13A":    [0,1,2,4,8],
    "5-13B":    [0,2,3,4,8],
    "5-14A":    [0,1,2,5,7],
    "5-14B":    [0,2,5,6,7],
    "5-15":	    [0,1,2,6,8],
    "5-16A":    [0,1,3,4,7],
    "5-16B":    [0,3,4,6,7],
    "5-z17":    [0,1,3,4,8],
    "5-z18A":   [0,1,4,5,7],
    "5-z18B":   [0,2,3,6,7],
    "5-19A":    [0,1,3,6,7],
    "5-19B":    [0,1,4,6,7],
    "5-20A":    [0,1,5,6,8],
    "5-20B":    [0,2,3,7,8],
    "5-21A":    [0,1,4,5,8],
    "5-21B":    [0,3,4,7,8],
    "5-22":	    [0,1,4,7,8],
    "5-23A":    [0,2,3,5,7],
    "5-23B":    [0,2,4,5,7],
    "5-24A":    [0,1,3,5,7],
    "5-25A":    [0,2,3,5,8],
    "5-25B":    [0,3,5,6,8],
    "5-26A":    [0,2,4,5,8],
    "5-26B":    [0,3,4,6,8],
    "5-27A":    [0,1,3,5,8],
    "5-27B":    [0,3,5,7,8],
    "5-28A":    [0,2,3,6,8],
    "5-28B":    [0,2,5,6,8],
    "5-29A":    [0,1,3,6,8],
    "5-29B":    [0,2,5,7,8],
    "5-30A":    [0,1,4,6,8],
    "5-30B":    [0,2,4,7,8],
    "5-31A":    [0,1,3,6,9],
    "5-31B":    [0,2,3,6,9],
    "5-32A":    [0,1,4,6,9],
    "5-32B":    [0,3,5,8,9],
    "5-33":	    [0,2,4,6,8],
    "5-34":	    [0,2,4,6,9],
    "5-35":	    [0,2,4,7,9],
    "5-z36A":   [0,1,2,4,7],
    "5-z36B":   [0,3,5,6,7],
    "5-z37":    [0,3,4,5,8],
    "5-z38A":   [0,1,2,5,8],
    "5-z38B":   [0,3,6,7,8],
    # 6-note sets
    "6-1":	    [0,1,2,3,4,5],
    "6-2A":	    [0,1,2,3,4,6],
    "6-2B":	    [0,2,3,4,5,6],
    "6-z3A":    [0,1,2,3,5,6],
    "6-z3B":    [0,1,3,4,5,6],
    "6-z4":	    [0,1,2,4,5,6],
    "6-5A":	    [0,1,2,3,6,7],
    "6-5B":	    [0,1,4,5,6,7],
    "6-z6":	    [0,1,2,5,6,7],
    "6-7":	    [0,1,2,6,7,8],
    "6-8":	    [0,2,3,4,5,7],
    "6-9A":	    [0,1,2,3,5,7],
    "6-9B":	    [0,2,4,5,6,7],
    "6-z10A":   [0,1,3,4,5,7],
    "6-z10B":   [0,2,3,4,6,7],
    "6-z11A":   [0,1,2,4,5,7],
    "6-z11B":   [0,2,3,5,6,7],
    "6-z12A":   [0,1,2,4,6,7],
    "6-z12B":   [0,1,3,5,6,7],
    "6-z13":    [0,1,3,4,6,7],
    "6-14A":    [0,1,3,4,5,8],
    "6-14B":    [0,3,4,5,7,8],
    "6-15A":    [0,1,2,4,5,8],
    "6-15B":    [0,3,4,6,7,8],
    "6-16A":    [0,1,4,5,6,8],
    "6-16B":    [0,2,3,4,7,8],
    "6-z17A":   [0,1,2,4,7,8],
    "6-z17B":   [0,1,4,6,7,8],
    "6-18A":    [0,1,2,5,7,8],
    "6-18B":    [0,1,3,6,7,8],
    "6-z19A":   [0,1,3,4,7,8],
    "6-z19B":   [0,1,4,5,7,8],
    "6-20":	    [0,1,4,5,8,9],
    "6-21A":    [0,2,3,4,6,8],
    "6-21B":    [0,2,4,5,6,8],
    "6-22A":    [0,1,2,4,6,8],
    "6-22B":    [0,2,4,6,7,8],
    "6-z23":    [0,2,3,5,6,8],
    "6-z24A":   [0,1,3,4,6,8],
    "6-z24B":	[0,2,4,5,7,8],
    "6-z25A":	[0,1,3,5,6,8],
    "6-z25B":	[0,2,3,5,7,8],
    "6-z26":	[0,1,3,5,7,8],
    "6-27A":	[0,1,3,4,6,9],
    "6-27B":	[0,3,5,6,8,9],
    "6-z28":	[0,1,3,5,6,9],
    "6-z29":	[0,2,3,6,7,9],
    "6-30A":	[0,1,3,6,7,9],
    "6-30B":	[0,2,3,6,8,9],
    "6-31A":	[0,1,4,5,7,9],
    "6-31B":	[0,2,4,5,8,9],
    "6-32":	    [0,2,4,5,7,9],
    "6-33A":	[0,2,3,5,7,9],
    "6-33B":	[0,2,4,6,7,9],
    "6-34A":	[0,1,3,5,7,9],
    "6-34B":	[0,2,4,6,8,9],
    "6-35":	    [0,2,4,6,8,10], # whole-tone scale
    "6-z36B":	[0,3,4,5,6,7],
    "6-z36A":	[0,1,2,3,4,7],
    "6-z37":	[0,1,2,3,4,8],
    "6-z38":	[0,1,2,3,7,8],
    "6-z39B":	[0,3,4,5,6,8],
    "6-z39A":	[0,2,3,4,5,8],
    "6-z40B":	[0,3,5,6,7,8],
    "6-z40A":	[0,1,2,3,5,8],
    "6-z41B":	[0,2,5,6,7,8],
    "6-z41A":	[0,1,2,3,6,8],
    "6-z42":	[0,1,2,3,6,9],
    "6-z43B":	[0,2,3,6,7,8],
    "6-z43A":	[0,1,2,5,6,8],
    "6-z44B":	[0,3,4,7,8,9],
    "6-z44A":	[0,1,2,5,6,9],
    "6-z45":	[0,2,3,4,6,9],
    "6-z46B":	[0,3,5,7,8,9],
    "6-z46A":	[0,1,2,4,6,9],
    "6-z47B":	[0,2,5,7,8,9],
    "6-z47A":	[0,1,2,4,7,9],
    "6-z48":	[0,1,2,5,7,9],
    "6-z49":	[0,1,3,4,7,9],
    "6-z50":	[0,1,4,6,7,9],
    # 7-note sets
    "7-1": 	    [0,1,2,3,4,5,6],
    "7-2B": 	[0,2,3,4,5,6,7],
    "7-2A": 	[0,1,2,3,4,5,7],
    "7-3B":	    [0,3,4,5,6,7,8],
    "7-3A":	    [0,1,2,3,4,5,8],
    "7-4B":	    [0,1,3,4,5,6,7],
    "7-4A":	    [0,1,2,3,4,6,7],
    "7-5B":	    [0,1,2,4,5,6,7],
    "7-5A":	    [0,1,2,3,5,6,7],
    "7-6B":	    [0,1,4,5,6,7,8],
    "7-6A":	    [0,1,2,3,4,7,8],
    "7-7B":	    [0,1,2,5,6,7,8],
    "7-7A":	    [0,1,2,3,6,7,8],
    "7-8":	    [0,2,3,4,5,6,8],
    "7-9B":	    [0,2,4,5,6,7,8],
    "7-9A":	    [0,1,2,3,4,6,8],
    "7-10B":	[0,2,3,4,5,6,9],
    "7-10A":    [0,1,2,3,4,6,9],
    "7-11B":	[0,2,3,4,5,7,8],
    "7-11A":	[0,1,3,4,5,6,8],
    "7-z12":	[0,1,2,3,4,7,9],
    "7-13B":	[0,2,3,4,6,7,8],
    "7-13A":	[0,1,2,4,5,6,8],
    "7-14B":	[0,1,3,5,6,7,8],
    "7-14A":	[0,1,2,3,5,7,8],
    "7-15":	    [0,1,2,4,6,7,8],
    "7-16B":	[0,1,3,4,5,6,9],
    "7-16A":	[0,1,2,3,5,6,9],
    "7-z17":	[0,1,2,4,5,6,9],
    "7-z18A":	[0,1,4,5,6,7,9],
    "7-z18B":	[0,1,4,6,7,8,9],
    "7-19B":	[0,1,2,3,6,8,9],
    "7-19A":	[0,1,2,3,6,7,9],
    "7-20B":	[0,1,2,5,7,8,9],
    "7-20A":	[0,1,2,5,6,7,9],
    "7-21B":	[0,1,3,4,5,8,9],
    "7-21A":	[0,1,2,4,5,8,9],
    "7-22":	    [0,1,2,5,6,8,9],
    "7-23B":	[0,2,4,5,6,7,9],
    "7-23A":	[0,2,3,4,5,7,9],
    "7-24B":	[0,2,4,6,7,8,9],
    "7-24A":	[0,1,2,3,5,7,9],
    "7-25B":	[0,2,3,5,6,7,9],
    "7-25A":	[0,2,3,4,6,7,9],
    "7-26A":	[0,1,3,4,5,7,9],
    "7-26B":	[0,2,4,5,6,8,9],
    "7-27B":	[0,2,4,5,7,8,9],
    "7-27A":	[0,1,2,4,5,7,9],
    "7-28A":	[0,1,3,5,6,7,9],
    "7-28B":	[0,2,3,4,6,8,9],
    "7-29B":	[0,2,3,5,7,8,9],
    "7-29A":	[0,1,2,4,6,7,9],
    "7-30B":	[0,1,3,5,7,8,9],
    "7-30A":	[0,1,2,4,6,8,9],
    "7-31B":	[0,2,3,5,6,8,9], # octatonic scale
    "7-31A":	[0,1,3,4,6,7,9],
    "7-32B":	[0,1,3,5,6,8,9],
    "7-32A":	[0,1,3,4,6,8,9],
    "7-33":	    [0,1,2,4,6,8,10],
    "7-34":	    [0,1,3,4,6,8,10],
    '''
    NOTE: 7-35 is the prime form of major and minor scales
    c maj would ordinarily be [0, 2, 4, 5, 7, 9, 11],
    but when you put it with the lowest interval at 
    the left at it's most "compact," it becomes 
    [11, 0, 2, 4, 5, 7, 9]. 7-35 is the prime form
    of this new arrangement. add 1 to each int in the 
    [11, 0,...] set and you get 7-35!
    '''
    "7-35":	    [0,1,3,5,6,8,10], # maj/min prime form
    "7-z36B":	[0,2,3,5,6,7,8],
    "7-z36A":	[0,1,2,3,5,6,8],
    "7-z37":	[0,1,3,4,5,7,8],
    "7-z38B":	[0,1,3,4,6,7,8],
    "7-z38A":	[0,1,2,4,5,7,8],
    # 8-note sets
    "8-1":	    [0,1,2,3,4,5,6,7],
    "8-2B":	    [0,2,3,4,5,6,7,8],
    "8-2A": 	[0,1,2,3,4,5,6,8],
    "8-3":  	[0,1,2,3,4,5,6,9],
    "8-4B":	    [0,1,3,4,5,6,7,8],
    "8-4A":	    [0,1,2,3,4,5,7,8],
    "8-5B":	    [0,1,2,4,5,6,7,8],
    "8-5A":	    [0,1,2,3,4,6,7,8],
    "8-6":  	[0,1,2,3,5,6,7,8],
    "8-7":	    [0,1,2,3,4,5,8,9],
    "8-8":	    [0,1,2,3,4,7,8,9],
    "8-9":  	[0,1,2,3,6,7,8,9],
    "8-10":	    [0,2,3,4,5,6,7,9],
    "8-11B":	[0,2,4,5,6,7,8,9],
    "8-11A":	[0,1,2,3,4,5,7,9],
    "8-12A":	[0,1,3,4,5,6,7,9],
    "8-12B":	[0,2,3,4,5,6,8,9],
    "8-13B":	[0,2,3,5,6,7,8,9],
    "8-13A":	[0,1,2,3,4,6,7,9],
    "8-14A":	[0,1,2,4,5,6,7,9],
    "8-14B":	[0,2,3,4,5,7,8,9],
    "8-z15B":	[0,1,3,5,6,7,8,9], # all interval tetrachord!
    "8-z15A":	[0,1,2,3,4,6,8,9],
    "8-16B":	[0,1,2,4,6,7,8,9],
    "8-16A":	[0,1,2,3,5,7,8,9],
    "8-17": 	[0,1,3,4,5,6,8,9],
    "8-18B":	[0,1,3,4,6,7,8,9],
    "8-18A":	[0,1,2,3,5,6,8,9],
    "8-19B":	[0,1,3,4,5,7,8,9],
    "8-19A":	[0,1,2,4,5,6,8,9],
    "8-20":	    [0,1,2,4,5,7,8,9],
    "8-21":	    [0,1,2,3,4,6,8,10],
    "8-22B":	[0,1,2,3,5,7,9,10],
    "8-22A":	[0,1,2,3,5,6,8,10],
    "8-23": 	[0,1,2,3,5,7,8,10],
    "8-24": 	[0,1,2,4,5,6,8,10],
    "8-25":	    [0,1,2,4,6,7,8,10],
    "8-26":	    [0,1,3,4,5,7,8,10],
    "8-27B":	[0,1,2,4,6,7,9,10],
    "8-27A":	[0,1,2,4,5,7,8,10],
    "8-28":	    [0,1,3,4,6,7,9,10],
    "8-z29B":	[0,2,3,4,6,7,8,9],
    "8-z29A":	[0,1,2,3,5,6,7,9],
    # 9-note sets
    "9-1":	    [0,1,2,3,4,5,6,7,8],
    "9-2A":	    [0,1,2,3,4,5,6,7,9],
    "9-2B":	    [0,2,3,4,5,6,7,8,9],
    "9-3B":	    [0,1,3,4,5,6,7,8,9],
    "9-3A":	    [0,1,2,3,4,5,6,8,9],
    "9-4B":	    [0,1,2,4,5,6,7,8,9],
    "9-4A":	    [0,1,2,3,4,5,7,8,9],
    "9-5B":	    [0,1,2,3,5,6,7,8,9],
    "9-5A":	    [0,1,2,3,4,6,7,8,9],
    "9-6":	    [0,1,2,3,4,5,6,8,10],
    "9-7B":	    [0,1,2,3,4,5,7,9,10],
    "9-7A":	    [0,1,2,3,4,5,7,8,10],
    "9-8B":	    [0,1,2,3,4,6,8,9,10],
    "9-8A":	    [0,1,2,3,4,6,7,8,10],
    "9-9":	    [0,1,2,3,5,6,7,8,10],
    "9-10":	    [0,1,2,3,4,6,7,9,10],
    "9-11B":	[0,1,2,3,5,6,8,9,10],
    "9-11A":	[0,1,2,3,5,6,7,9,10],
    "9-12":	    [0,1,2,4,5,6,8,9,10]
}


# List of Forte numbers. Use randint() to select
# the string/key value to be used with SCALES. 
FORTE_NUMBERS = [
    "5-1",
    "5-2A",
    "5-2B",
    "5-3A",
    "5-3B",
    "5-4A",
    "5-4B",
    "5-5A",
    "5-5B",
    "5-6A",
    "5-6B",
    "5-7A",
    "5-7B",
    "5-8",
    "5-9A",
    "5-9B",
    "5-10A",
    "5-10B",
    "5-11A",
    "5-11B",
    "5-z12",
    "5-13A",
    "5-13B",
    "5-14A",
    "5-14B",
    "5-15",
    "5-16A",
    "5-16B",
    "5-z17",
    "5-z18A",
    "5-z18B",
    "5-19A",
    "5-19B",
    "5-20A",
    "5-20B",
    "5-21A",
    "5-21B",
    "5-22",
    "5-23A",
    "5-23B",
    "5-24A",
    "5-25A",
    "5-25B",
    "5-26A",
    "5-26B",
    "5-27A",
    "5-27B",
    "5-28A",
    "5-28B",
    "5-29A",
    "5-29B",
    "5-30A",
    "5-30B",
    "5-31A",
    "5-31B",
    "5-32A",
    "5-32B",
    "5-33",
    "5-34",
    "5-35",
    "5-z36A",
    "5-z36B",
    "5-z37",
    "5-z38A",
    "5-z38B",
    # 6-note sets
    "6-1",
    "6-2A",
    "6-2B",
    "6-z3A",
    "6-z3B",
    "6-z4",
    "6-5A",
    "6-5B",
    "6-z6",
    "6-7",
    "6-8",
    "6-9A",
    "6-9B",
    "6-z10A",
    "6-z10B",
    "6-z11A",
    "6-z11B",
    "6-z12A",
    "6-z12B",
    "6-z13",
    "6-14A",
    "6-14B",
    "6-15A",
    "6-15B",
    "6-16A",
    "6-16B",
    "6-z17A",
    "6-z17B",
    "6-18A",
    "6-18B",
    "6-z19A",
    "6-z19B",
    "6-20",
    "6-21A",
    "6-21B",
    "6-22A",
    "6-22B",
    "6-z23",
    "6-z24A",
    "6-z24B",
    "6-z25A",
    "6-z25B",
    "6-z26",
    "6-27A",
    "6-27B",
    "6-z28",
    "6-z29",
    "6-30A",
    "6-30B",
    "6-31A",
    "6-31B",
    "6-32",
    "6-33A",
    "6-33B",
    "6-34A",
    "6-34B",
    "6-35",
    "6-z36B",
    "6-z36A",
    "6-z37",
    "6-z38",
    "6-z39B",
    "6-z39A",
    "6-z40B",
    "6-z40A",
    "6-z41B",
    "6-z41A",
    "6-z42",
    "6-z43B",
    "6-z43A",
    "6-z44B",
    "6-z44A",
    "6-z45",
    "6-z46B",
    "6-z46A",
    "6-z47B",
    "6-z47A",
    "6-z48",
    "6-z49",
    "6-z50",
    # 7-note sets
    "7-1",
    "7-2B",	
    "7-2A",	
    "7-3B",	
    "7-3A",	
    "7-4B",	
    "7-4A",	
    "7-5B",
    "7-5A",
    "7-6B",
    "7-6A",
    "7-7B",
    "7-7A",
    "7-8",
    "7-9B",
    "7-9A",
    "7-10B",
    "7-10A",
    "7-11B",
    "7-11A",
    "7-z12",
    "7-13B",
    "7-13A",
    "7-14B",
    "7-14A",
    "7-15",
    "7-16B",
    "7-16A",
    "7-z17",
    "7-z18A",
    "7-z18B",
    "7-19B",
    "7-19A",
    "7-20B",
    "7-20A",
    "7-21B",
    "7-21A",
    "7-22",
    "7-23B",
    "7-23A",
    "7-24B",
    "7-24A",
    "7-25B",
    "7-25A",
    "7-26A",
    "7-26B",
    "7-27B",
    "7-27A",
    "7-28A",
    "7-28B",
    "7-29B",
    "7-29A",
    "7-30B",
    "7-30A",
    "7-31B",
    "7-31A",
    "7-32B",
    "7-32A",
    "7-33",
    "7-34",
    "7-35",
    "7-z36B",
    "7-z36A",
    "7-z37",
    "7-z38B",
    "7-z38A"
    # 8-note sets
    "8-1",
    "8-2B",
    "8-2A",
    "8-3",
    "8-4B",
    "8-4A",
    "8-5B",
    "8-5A",
    "8-6",
    "8-7",
    "8-8",
    "8-9",
    "8-10",
    "8-11B",
    "8-11A",
    "8-12A",
    "8-12B",
    "8-13B",
    "8-13A",
    "8-14A",
    "8-14B",
    "8-z15B",
    "8-z15A",
    "8-16B",
    "8-16A",
    "8-17",
    "8-18B",
    "8-18A",
    "8-19B",
    "8-19A",
    "8-20",
    "8-21",
    "8-22B",
    "8-22A",
    "8-23",
    "8-24",
    "8-25",
    "8-26",
    "8-27B",
    "8-27A",
    "8-28",
    "8-z29B",
    "8-z29A",
    # 9-note sets
    "9-1",
    "9-2A",
    "9-2B",
    "9-3B",
    "9-3A",	
    "9-4B",
    "9-4A",	
    "9-5B",
    "9-5A",	
    "9-6",
    "9-7B",
    "9-7A",	
    "9-8B",
    "9-8A",	
    "9-9",
    "9-10",
    "9-11B",
    "9-11A",
    "9-12"	
]


# Ensembles
'''NOTE: obviously not complete or comprehensive. 
just some standards that could use usefull when quick 
templates are needed.'''

ENSEMBLES = {
    "string trio": ['Violin', 'Viola', 'Cello'],
    "string quartet": ['Violin', 'Viola', 'Cello'],
    "piano trio": ['Violin', 'Cello', 'Acoustic Grand Piano'],
    "duet: pno/vn": ['Violin', 'Acoustic Grand Piano'],
    "duet: pno/va": ['Viola', 'Acoustic Grand Piano'],
    "duet: pno/vc": ['Cello', 'Acoustic Grand Piano'],
    "duet: pno/cl": ['Clarinet', 'Acoustic Grand Piano'],
}


# Keys to be used with ENSEMBLES and randint()
ENSEMBLES_KEYS = [
    "string trio",
    "string quartet",
    "piano trio",
    "duet: pno/vn",
    "duet: pno/va",
    "duet: pno/vc",
    "duet: pno/cl",
]


# Ensemble sizes
ENSEMBLE_SIZES = {1: 'solo',
                  2: 'duo',
                  3: 'trio',
                  4: 'quartet',
                  5: 'quintet',
                  6: 'sextet',
                  7: 'septet',
                  8: 'octet',
                  9: 'nonet',
                  10: 'decet',
                  11: 'large ensemble'}


# MIDI instruments list (standard)
'''NOTE:Indicies 0 - 110 are MELODIC/HARMONIC instruments!'''

INSTRUMENTS = [
    # 0-8: keyboards
    'Acoustic Grand Piano', 
    'Bright Acoustic Piano',              
    'Electric Grand Piano', 
    'Honky-tonk Piano',
    'Electric Piano 1', 
    'Electric Piano 2', 
    'Harpsichord',
    'Clavinet', 
    'Celesta',
    # 9-15: metal/wood pitched percussion  
    'Glockenspiel', 
    'Music Box',
    'Vibraphone', 
    'Marimba', 
    'Xylophone', 
    'Tubular Bells',
    'Dulcimer', 
    # 16-20: organs
    'Drawbar Organ', 
    'Percussive Organ',
    'Rock Organ', 
    'Church Organ', 
    'Reed Organ', 
    # 21-23: accordians/harmonica
    'Accordion',
    'Harmonica', 
    'Tango Accordion', 
    # 24-31: guitars
    'Acoustic Guitar (nylon)',
    'Acoustic Guitar (steel)', 
    'Electric Guitar (jazz)',
    'Electric Guitar (clean)', 
    'Electric Guitar (muted)',
    'Overdriven Guitar', 
    'Distortion Guitar',
    'Guitar Harmonics',
    # 32-39: basses 
    'Acoustic Bass',
    'Electric Bass (finger)', 
    'Electric Bass (pick)',
    'Fretless Bass', 
    'Slap Bass 1', 
    'Slap Bass 2',
    'Synth Bass 1', 
    'Synth Bass 2',
    # 40-45: strings 
    'Violin', 
    'Viola', 
    'Cello',
    'Contrabass', 
    'Tremolo Strings', 
    'Pizzicato Strings',
    # 46: harp
    'Orchestral Harp',
    # 47: timpani 
    'Timpani',
    # 48-51 : string ensembles 
    'String Ensemble 1',
    'String Ensemble 2', 
    'Synth Strings 1', 
    'Synth Strings 2',
    # 52-54: choirs
    'Choir Aahs', 
    'Voice Oohs', 
    'Synth Choir',
    # 55: orchestra hit 
    'Orchestra Hit',
    # 56-63: brass
    'Trumpet', 
    'Trombone', 
    'Tuba', 
    'Muted Trumpet',
    'French Horn', 
    'Brass Section', 
    'Synth Brass 1',
    'Synth Brass 2',
    # 64-67: saxes 
    'Soprano Sax', 
    'Alto Sax', 
    'Tenor Sax',
    'Baritone Sax',
    # 68-79: woodwinds 
    'Oboe', 
    'English Horn', 
    'Bassoon',
    'Clarinet', 
    'Piccolo', 
    'Flute', 
    'Recorder', 
    'Pan Flute',
    'Blown bottle', 
    'Shakuhachi', 
    'Whistle', 
    'Ocarina',
    # 80-95: synth leads & pads
    'Lead 1 (square)', 
    'Lead 2 (sawtooth)',
    'Lead 3 (calliope)', 
    'Lead 4 chiff', 
    'Lead 5 (charang)',
    'Lead 6 (voice)', 
    'Lead 7 (fifths)',
    'Lead 8 (bass + lead)', 
    'Pad 1 (new age)', 
    'Pad 2 (warm)',
    'Pad 3 (polysynth)', 
    'Pad 4 (choir)', 
    'Pad 5 (bowed)',
    'Pad 6 (metallic)', 
    'Pad 7 (halo)', 
    'Pad 8 (sweep)',
    # 96-103: misc FX
    'FX 1 (rain)', 
    'FX 2 (soundtrack)', 
    'FX 3 (crystal)',
    'FX 4 (atmosphere)', 
    'FX 5 (brightness)', 
    'FX 6 (goblins)',
    'FX 7 (echoes)', 
    'FX 8 (sci-fi)',
    # 104-111: other plucked string instruments 
    'Sitar', 
    'Banjo',
    'Shamisen', 
    'Koto', 
    'Kalimba', 
    'Bagpipe', 
    'Fiddle',
    'Shanai',
    # Indices 112 onward are non-pitched percussion instruments and
    # other misc. sound effects 
    'Tinkle Bell', 
    'Agogo', 
    'Steel Drums',
    'Woodblock', 
    'Taiko Drum', 
    'Melodic Tom', 
    'Synth Drum',
    'Reverse Cymbal', 
    'Guitar Fret Noise', 
    'Breath Noise',
    'Seashore', 
    'Bird Tweet', 
    'Telephone Ring', 
    'Helicopter',
    'Applause', 
    'Gunshot'
]