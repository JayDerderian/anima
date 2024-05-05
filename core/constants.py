"""
A module for managing all constants used throughout the program.
"""

from os.path import join
from pathlib import Path

# absolute path of the program itself
ROOT = Path(__file__).parent.parent

# location to write MIDI files to
MIDI_FOLDER = join(ROOT, "midi")

# The alphabet.
ALPHABET = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

# Tempos
TEMPOS = [
    40.0,
    42.0,
    44.0,
    46.0,
    50.0,
    52.0,
    54.0,
    56.0,
    58.0,  # 0 - 8
    60.0,
    63.0,
    66.0,
    69.0,
    72.0,
    76.0,
    80.0,
    84.0,
    88.0,  # 9 - 17
    92.0,
    96.0,
    100.0,
    104.0,
    108.0,
    112.0,
    116.0,
    120.0,  # 18 - 25
    126.0,
    132.0,
    138.0,
    144.0,
    152.0,
    160.0,
    168.0,
    176.0,  # 26 - 33
    184.0,
    200.0,
    208.0,
]  # 34 - 36

# The default tempo is 120 BPM for MIDI messages
# (500000 microseconds per beat (quarter note).)
DEFAULT_TEMPO = 500000
DEFAULT_TICKS_PER_BEAT = 480

# Dynamics (MIDI velocities: 0 - 127)
"""NOTE: use indices 0-8 for soft dynamics only. 
         9-17 for med, and 18-26 for loud dynamics"""
DYNAMICS = [
    20,
    24,
    28,
    32,
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    68,
    72,
    76,
    80,
    84,
    88,
    92,
    96,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
]

# Base rhythms in seconds at 60bpm (or q = 60).
# Convert to current tempo using scale_to_tempo() when necessary.
"""
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
"""
RHYTHMS = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25, 0.125]

"""
MIDI doesn't actually have rests. Instead a "rest" is just a 
completely silent note in a MIDI file, so rests need to be notated
in the sheet music accordingly and be able to recognize the constant
REST in a given composition object.

REST is actually a MIDI velocity of 0
"""
REST = 0

"""
this is mainly used by the analysis module to determine proper beat values
in a given meter. were' sticking with rational meters for the time being.
"""
BEATS = [1, 2, 4, 8, 16, 32, 64]

# Base durations in seconds for tuplets where q = 60bpm
TUPLETS = {
    "triplet quarter": 0.667,
    "quintuplet quarter": 0.4,
    "triplet eighth": 0.333,
    "quintuplet eighth": 0.2,
    "triplet sixteenth": 0.167,
    "septuplet eighth": 0.143,
    "quintuplet sixteenth": 0.1,
    "septuplet sixteenth": 0.071,
}

# List of pitch classes
"""
NOTE: the indices of each pitch class correspond to 
      its representation in integer notation!
"""
PITCH_CLASSES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

# All the notes!
# Complete piano range from bottom key to top key, octaves 0 - 8
# NOTE: enharmonic spellings of certain notes (like C# vs Db) are ignored
# for the sake of simplicity, though the resulting sounds will be the same.
# TODO: add enharmonic spellings and adjust midi.note_name_to_MIDI_num helpers
NOTES = [
    "A0",
    "Bb0",
    "B0",
    "C1",
    "C#1",
    "D1",
    "Eb1",
    "E1",
    "F1",
    "F#1",
    "G1",
    "G#1",
    "A1",
    "Bb1",
    "B1",
    "C2",
    "C#2",
    "D2",
    "Eb2",
    "E2",
    "F2",
    "F#2",
    "G2",
    "G#2",
    "A2",
    "Bb2",
    "B2",
    "C3",
    "C#3",
    "D3",
    "Eb3",
    "E3",
    "F3",
    "F#3",
    "G3",
    "G#3",
    "A3",
    "Bb3",
    "B3",
    "C4",
    "C#4",
    "D4",
    "Eb4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "Bb4",
    "B4",
    "C5",
    "C#5",
    "D5",
    "Eb5",
    "E5",
    "F5",
    "F#5",
    "G5",
    "G#5",
    "A5",
    "Bb5",
    "B5",
    "C6",
    "C#6",
    "D6",
    "Eb6",
    "E6",
    "F6",
    "F#6",
    "G6",
    "G#6",
    "A6",
    "Bb6",
    "B6",
    "C7",
    "C#7",
    "D7",
    "Eb7",
    "E7",
    "F7",
    "F#7",
    "G7",
    "G#7",
    "A7",
    "Bb7",
    "B7",
    "C8",
]

# All 12 major scales
MAJOR_SCALES = {
    "C Major": ["C", "D", "E", "F", "G", "A", "B"],
    "Db Major": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "D Major": ["D", "E", "F#", "G", "A", "B", "C#"],
    "Eb Major": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E Major": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "F Major": ["F", "G", "A", "Bb", "C", "D", "E"],
    "F# Major": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "G Major": ["G", "A", "B", "C", "D", "E", "F#"],
    "Ab Major": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "A Major": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "Bb Major": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "B Major": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
}

# All 12 relative/natural minor scales
MINOR_SCALES = {
    "A Minor": ["A", "B", "C", "D", "E", "F", "G"],
    "Bb Minor": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
    "B Minor": ["B", "C#", "D", "E", "F#", "G", "A"],
    "C Minor": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "C# Minor": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "D Minor": ["D", "E", "F", "G", "A", "Bb", "C"],
    "D# Minor": ["Eb", "F", "Gb", "Ab", "Bb", "B", "C#"],  # ignorning C flat
    "E Minor": ["E", "F#", "G", "A", "B", "C", "D"],
    "F Minor": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "F# Minor": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "G Minor": ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "G# Minor": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
}

# Chromatic scale pitch class set notation representation
CHROMATIC_SCALE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# These are modes and scales starting on 'C', so they will need to
# be transposed before being matched with corresponding note strings.
SCALES = {
    "Acoustic": [0, 2, 4, 6, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],
    "Algerian": [0, 2, 3, 5, 6, 7, 8, 11],
    "Altered": [0, 1, 3, 4, 6, 8, 10],
    "Augmented": [0, 3, 4, 7, 8, 11],
    "Bebop": [0, 2, 4, 5, 7, 9, 10, 11],
    "Blues": [0, 3, 5, 6, 7, 11],
    "Double Harmonic": [0, 1, 4, 5, 7, 8, 11],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "Flamenco": [0, 1, 4, 5, 7, 8, 11],
    "Gong": [0, 2, 4, 7, 9],
    "Gypsy": [0, 2, 3, 6, 7, 8, 10],
    "Half-diminished": [0, 2, 3, 5, 6, 8, 10],
    "Harmonics": [0, 3, 4, 5, 7, 9],
    "Harmonic Major": [0, 2, 4, 5, 7, 8, 11],
    "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
    "Hex Aeolian": [0, 3, 5, 7, 8, 10],
    "Hex Phrygian": [0, 1, 3, 5, 8, 10],
    "Hex Sus": [0, 2, 5, 7, 8, 10],
    "Hirajoshi": [0, 4, 6, 7, 11],
    "Hungarian Minor": [0, 2, 3, 6, 7, 8, 11],
    "Hungarian Major": [0, 3, 4, 6, 7, 9, 10],
    "Ionian": [0, 2, 4, 5, 7, 9, 11],
    "In": [
        0,
        1,
        5,
        7,
        8,
    ],
    "Insen": [0, 1, 5, 7, 10],
    "Iwato": [0, 1, 5, 6, 10],
    "Locrean": [0, 1, 3, 5, 6, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Lydian augmented": [0, 2, 4, 6, 8, 9, 11],
    "Major bebop": [0, 2, 4, 5, 7, 8, 9, 11],
    "Major locrian": [0, 2, 4, 5, 6, 8, 10],
    "Major pentatonic": [0, 2, 4, 7, 9],
    "Minor pentatonic": [0, 3, 5, 8, 10],
    "Mixed Minor": [0, 2, 3, 5, 7, 9, 10, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Mel Min Ascending": [0, 2, 3, 5, 7, 9, 11],
    "Neapolitan Major": [0, 1, 3, 5, 7, 9, 11],
    "Neapolitan Minor": [0, 1, 3, 5, 7, 8, 11],
    "Octatonic 1": [0, 1, 3, 4, 6, 7, 9, 10],
    "Octatonic 2": [0, 2, 3, 5, 6, 8, 9, 11],
    "Pelog": [0, 1, 3, 6, 7, 8, 10],
    "Pelong": [0, 1, 3, 7, 8],
    "Persian": [0, 1, 4, 5, 6, 8, 11],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Phrygian Dominant": [0, 1, 4, 5, 7, 8, 10],
    "Prometheus": [0, 2, 4, 6, 7, 9, 10],
    "Raang Dhani": [0, 4, 5, 7, 10],
    "Scriabin": [0, 1, 4, 7, 9],
    "Shang": [0, 2, 5, 7, 10],
    "Tritone 1": [0, 1, 4, 5, 6, 7, 10],
    "Tritone 2": [
        0,
        1,
        2,
        6,
        7,
        8,
    ],
    "Ukrainian Dorian": [0, 2, 3, 6, 7, 9, 10],
    "Whole Tone": [0, 2, 4, 6, 8, 10],
}

# Interval list/dictionary
"""
NOTE: Develop interval sets that begin with 2 and end with 2,
      making the next cycle of intervals begin on a tone a half
      step higher than originally.

      "Self-transposing interval sets"

      ex. 
        c, d, e, f#, g, a, bb, c,
        db, eb, f, g, ab, bB, cb, db,
        d, e, f#, g#, a, b, c, d ...ect.  
"""

# intervals between notes in semi-tones
INTERVALS = {
    "Chromatic Scale": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "Major Scale": [2, 2, 1, 2, 2, 2, 1],
    "Natural Minor": [2, 1, 2, 2, 1, 2, 2],
    "Melodic Minor": [2, 1, 2, 2, 2, 2, 1],
    "Harmonic Minor": [2, 1, 2, 2, 1, 3],
    "Whole Tone": [2, 2, 2, 2, 2],
    "Octatonic": [2, 1, 2, 1, 2, 1, 2],
    "Maj Triad": [4, 3],
    "Min Triad": [3, 4],
    "Dim Triad": [3, 3],
    "Aug Triad": [4, 4],
}

# NOTE: figure out to account of octaves if pcs below are transposed!
ARPEGGIOS = {
    # root position & symmetrical
    "chromatic": [0, 1, 2, 1],
    "secundal": [0, 2, 4, 2],
    "diminished": [0, 3, 6, 3],
    "min triad": [0, 3, 7, 3],
    "maj triad": [0, 4, 7, 4],
    "augmented": [0, 4, 8, 4],
    "quartal": [0, 5, 10, 5],
}

"""
A dictionary of common chord progressions notated in roman numerals
"""
PROGRESSIONS = {
    "Pop1": ["I", "V", "vi", "IV"],
    "Pop2": ["I", "IV", "V", "IV"],
    "Pop3": ["ii", "V", "I"],
    "DooWop1": ["I", "vi", "IV", "V"],
    "DooWop2": ["I", "vi", "iv", "V"],
    "Canon": ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
    "12BarBlues": ["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "I"],
}

"""
maps roman numeral notation to scale degree. 
"""
SCALE_DEGREE_MAPPING = {
    "i": 1,
    "I": 1,
    "ii": 2,
    "II": 2,
    "iii": 3,
    "III": 3,
    "iv": 4,
    "IV": 4,
    "v": 5,
    "V": 5,
    "vi": 6,
    "VI": 6,
    "vii": 7,
    "VII": 7,
}

"""
A rather large dictionary containing all of Allen Forte's 5 to 9 
note prime form pitch class sets. A corresponding list called FORTE_NUMBERS 
is used with randint() to pick a prime form from the dictionary in pickScale().
The choice using FORTE_NUMBERS can be used to export_midi which number was used for analytical
purposes.

Each integer/pitch class functions as an index number against CHROMATIC_SCALE to 
generate a scale represented by a list of strings (i.e. ["C#4", "D5"... etc]).

    NOTE: 7-35 is the prime form of major and minor scales
    c maj would ordinarily be [0, 2, 4, 5, 7, 9, 11],
    but when you put it with the lowest interval at 
    the left at it's most "compact," it becomes 
    [11, 0, 2, 4, 5, 7, 9]. 7-35 is the prime form
    of this new arrangement. add 1 to each int in the 
    [11, 0,...] set and you get 7-35!

Info taken from here: 
https://en.wikipedia.org/wiki/List_of_pitch-class_sets
"""

SETS = {
    # 5-note sets
    "5-1": [0, 1, 2, 3, 4],
    "5-2A": [0, 1, 2, 3, 5],
    "5-2B": [0, 2, 3, 4, 5],
    "5-3A": [0, 1, 2, 4, 5],
    "5-3B": [0, 1, 3, 4, 5],
    "5-4A": [0, 1, 2, 3, 6],
    "5-4B": [0, 3, 4, 5, 6],
    "5-5A": [0, 1, 2, 3, 7],
    "5-5B": [0, 4, 5, 6, 7],
    "5-6A": [0, 1, 2, 5, 6],
    "5-6B": [0, 1, 4, 5, 6],
    "5-7A": [0, 1, 2, 6, 7],
    "5-7B": [0, 1, 5, 6, 7],
    "5-8": [0, 2, 3, 4, 6],
    "5-9A": [0, 1, 2, 4, 6],
    "5-9B": [0, 2, 4, 5, 6],
    "5-10A": [0, 1, 3, 4, 6],
    "5-10B": [0, 2, 3, 5, 6],
    "5-11A": [0, 2, 3, 4, 7],
    "5-11B": [0, 3, 4, 5, 7],
    "5-z12": [0, 1, 3, 5, 6],
    "5-13A": [0, 1, 2, 4, 8],
    "5-13B": [0, 2, 3, 4, 8],
    "5-14A": [0, 1, 2, 5, 7],
    "5-14B": [0, 2, 5, 6, 7],
    "5-15": [0, 1, 2, 6, 8],
    "5-16A": [0, 1, 3, 4, 7],
    "5-16B": [0, 3, 4, 6, 7],
    "5-z17": [0, 1, 3, 4, 8],
    "5-z18A": [0, 1, 4, 5, 7],
    "5-z18B": [0, 2, 3, 6, 7],
    "5-19A": [0, 1, 3, 6, 7],
    "5-19B": [0, 1, 4, 6, 7],
    "5-20A": [0, 1, 5, 6, 8],
    "5-20B": [0, 2, 3, 7, 8],
    "5-21A": [0, 1, 4, 5, 8],
    "5-21B": [0, 3, 4, 7, 8],
    "5-22": [0, 1, 4, 7, 8],
    "5-23A": [0, 2, 3, 5, 7],
    "5-23B": [0, 2, 4, 5, 7],
    "5-24A": [0, 1, 3, 5, 7],
    "5-25A": [0, 2, 3, 5, 8],
    "5-25B": [0, 3, 5, 6, 8],
    "5-26A": [0, 2, 4, 5, 8],
    "5-26B": [0, 3, 4, 6, 8],
    "5-27A": [0, 1, 3, 5, 8],
    "5-27B": [0, 3, 5, 7, 8],
    "5-28A": [0, 2, 3, 6, 8],
    "5-28B": [0, 2, 5, 6, 8],
    "5-29A": [0, 1, 3, 6, 8],
    "5-29B": [0, 2, 5, 7, 8],
    "5-30A": [0, 1, 4, 6, 8],
    "5-30B": [0, 2, 4, 7, 8],
    "5-31A": [0, 1, 3, 6, 9],
    "5-31B": [0, 2, 3, 6, 9],
    "5-32A": [0, 1, 4, 6, 9],
    "5-32B": [0, 3, 5, 8, 9],
    "5-33": [0, 2, 4, 6, 8],
    "5-34": [0, 2, 4, 6, 9],
    "5-35": [0, 2, 4, 7, 9],
    "5-z36A": [0, 1, 2, 4, 7],
    "5-z36B": [0, 3, 5, 6, 7],
    "5-z37": [0, 3, 4, 5, 8],
    "5-z38A": [0, 1, 2, 5, 8],
    "5-z38B": [0, 3, 6, 7, 8],
    # 6-note sets
    "6-1": [0, 1, 2, 3, 4, 5],
    "6-2A": [0, 1, 2, 3, 4, 6],
    "6-2B": [0, 2, 3, 4, 5, 6],
    "6-z3A": [0, 1, 2, 3, 5, 6],
    "6-z3B": [0, 1, 3, 4, 5, 6],
    "6-z4": [0, 1, 2, 4, 5, 6],
    "6-5A": [0, 1, 2, 3, 6, 7],
    "6-5B": [0, 1, 4, 5, 6, 7],
    "6-z6": [0, 1, 2, 5, 6, 7],
    "6-7": [0, 1, 2, 6, 7, 8],
    "6-8": [0, 2, 3, 4, 5, 7],
    "6-9A": [0, 1, 2, 3, 5, 7],
    "6-9B": [0, 2, 4, 5, 6, 7],
    "6-z10A": [0, 1, 3, 4, 5, 7],
    "6-z10B": [0, 2, 3, 4, 6, 7],
    "6-z11A": [0, 1, 2, 4, 5, 7],
    "6-z11B": [0, 2, 3, 5, 6, 7],
    "6-z12A": [0, 1, 2, 4, 6, 7],
    "6-z12B": [0, 1, 3, 5, 6, 7],
    "6-z13": [0, 1, 3, 4, 6, 7],
    "6-14A": [0, 1, 3, 4, 5, 8],
    "6-14B": [0, 3, 4, 5, 7, 8],
    "6-15A": [0, 1, 2, 4, 5, 8],
    "6-15B": [0, 3, 4, 6, 7, 8],
    "6-16A": [0, 1, 4, 5, 6, 8],
    "6-16B": [0, 2, 3, 4, 7, 8],
    "6-z17A": [0, 1, 2, 4, 7, 8],
    "6-z17B": [0, 1, 4, 6, 7, 8],
    "6-18A": [0, 1, 2, 5, 7, 8],
    "6-18B": [0, 1, 3, 6, 7, 8],
    "6-z19A": [0, 1, 3, 4, 7, 8],
    "6-z19B": [0, 1, 4, 5, 7, 8],
    "6-20": [0, 1, 4, 5, 8, 9],
    "6-21A": [0, 2, 3, 4, 6, 8],
    "6-21B": [0, 2, 4, 5, 6, 8],
    "6-22A": [0, 1, 2, 4, 6, 8],
    "6-22B": [0, 2, 4, 6, 7, 8],
    "6-z23": [0, 2, 3, 5, 6, 8],
    "6-z24A": [0, 1, 3, 4, 6, 8],
    "6-z24B": [0, 2, 4, 5, 7, 8],
    "6-z25A": [0, 1, 3, 5, 6, 8],
    "6-z25B": [0, 2, 3, 5, 7, 8],
    "6-z26": [0, 1, 3, 5, 7, 8],
    "6-27A": [0, 1, 3, 4, 6, 9],
    "6-27B": [0, 3, 5, 6, 8, 9],
    "6-z28": [0, 1, 3, 5, 6, 9],
    "6-z29": [0, 2, 3, 6, 7, 9],
    "6-30A": [0, 1, 3, 6, 7, 9],
    "6-30B": [0, 2, 3, 6, 8, 9],
    "6-31A": [0, 1, 4, 5, 7, 9],
    "6-31B": [0, 2, 4, 5, 8, 9],
    "6-32": [0, 2, 4, 5, 7, 9],
    "6-33A": [0, 2, 3, 5, 7, 9],
    "6-33B": [0, 2, 4, 6, 7, 9],
    "6-34A": [0, 1, 3, 5, 7, 9],
    "6-34B": [0, 2, 4, 6, 8, 9],
    "6-35": [0, 2, 4, 6, 8, 10],  # whole-tone scale
    "6-z36B": [0, 3, 4, 5, 6, 7],
    "6-z36A": [0, 1, 2, 3, 4, 7],
    "6-z37": [0, 1, 2, 3, 4, 8],
    "6-z38": [0, 1, 2, 3, 7, 8],
    "6-z39B": [0, 3, 4, 5, 6, 8],
    "6-z39A": [0, 2, 3, 4, 5, 8],
    "6-z40B": [0, 3, 5, 6, 7, 8],
    "6-z40A": [0, 1, 2, 3, 5, 8],
    "6-z41B": [0, 2, 5, 6, 7, 8],
    "6-z41A": [0, 1, 2, 3, 6, 8],
    "6-z42": [0, 1, 2, 3, 6, 9],
    "6-z43B": [0, 2, 3, 6, 7, 8],
    "6-z43A": [0, 1, 2, 5, 6, 8],
    "6-z44B": [0, 3, 4, 7, 8, 9],
    "6-z44A": [0, 1, 2, 5, 6, 9],
    "6-z45": [0, 2, 3, 4, 6, 9],
    "6-z46B": [0, 3, 5, 7, 8, 9],
    "6-z46A": [0, 1, 2, 4, 6, 9],
    "6-z47B": [0, 2, 5, 7, 8, 9],
    "6-z47A": [0, 1, 2, 4, 7, 9],
    "6-z48": [0, 1, 2, 5, 7, 9],
    "6-z49": [0, 1, 3, 4, 7, 9],
    "6-z50": [0, 1, 4, 6, 7, 9],
    # 7-note sets
    "7-1": [0, 1, 2, 3, 4, 5, 6],
    "7-2B": [0, 2, 3, 4, 5, 6, 7],
    "7-2A": [0, 1, 2, 3, 4, 5, 7],
    "7-3B": [0, 3, 4, 5, 6, 7, 8],
    "7-3A": [0, 1, 2, 3, 4, 5, 8],
    "7-4B": [0, 1, 3, 4, 5, 6, 7],
    "7-4A": [0, 1, 2, 3, 4, 6, 7],
    "7-5B": [0, 1, 2, 4, 5, 6, 7],
    "7-5A": [0, 1, 2, 3, 5, 6, 7],
    "7-6B": [0, 1, 4, 5, 6, 7, 8],
    "7-6A": [0, 1, 2, 3, 4, 7, 8],
    "7-7B": [0, 1, 2, 5, 6, 7, 8],
    "7-7A": [0, 1, 2, 3, 6, 7, 8],
    "7-8": [0, 2, 3, 4, 5, 6, 8],
    "7-9B": [0, 2, 4, 5, 6, 7, 8],
    "7-9A": [0, 1, 2, 3, 4, 6, 8],
    "7-10B": [0, 2, 3, 4, 5, 6, 9],
    "7-10A": [0, 1, 2, 3, 4, 6, 9],
    "7-11B": [0, 2, 3, 4, 5, 7, 8],
    "7-11A": [0, 1, 3, 4, 5, 6, 8],
    "7-z12": [0, 1, 2, 3, 4, 7, 9],
    "7-13B": [0, 2, 3, 4, 6, 7, 8],
    "7-13A": [0, 1, 2, 4, 5, 6, 8],
    "7-14B": [0, 1, 3, 5, 6, 7, 8],
    "7-14A": [0, 1, 2, 3, 5, 7, 8],
    "7-15": [0, 1, 2, 4, 6, 7, 8],
    "7-16B": [0, 1, 3, 4, 5, 6, 9],
    "7-16A": [0, 1, 2, 3, 5, 6, 9],
    "7-z17": [0, 1, 2, 4, 5, 6, 9],
    "7-z18A": [0, 1, 4, 5, 6, 7, 9],
    "7-z18B": [0, 1, 4, 6, 7, 8, 9],
    "7-19B": [0, 1, 2, 3, 6, 8, 9],
    "7-19A": [0, 1, 2, 3, 6, 7, 9],
    "7-20B": [0, 1, 2, 5, 7, 8, 9],
    "7-20A": [0, 1, 2, 5, 6, 7, 9],
    "7-21B": [0, 1, 3, 4, 5, 8, 9],
    "7-21A": [0, 1, 2, 4, 5, 8, 9],
    "7-22": [0, 1, 2, 5, 6, 8, 9],
    "7-23B": [0, 2, 4, 5, 6, 7, 9],
    "7-23A": [0, 2, 3, 4, 5, 7, 9],
    "7-24B": [0, 2, 4, 6, 7, 8, 9],
    "7-24A": [0, 1, 2, 3, 5, 7, 9],
    "7-25B": [0, 2, 3, 5, 6, 7, 9],
    "7-25A": [0, 2, 3, 4, 6, 7, 9],
    "7-26A": [0, 1, 3, 4, 5, 7, 9],
    "7-26B": [0, 2, 4, 5, 6, 8, 9],
    "7-27B": [0, 2, 4, 5, 7, 8, 9],
    "7-27A": [0, 1, 2, 4, 5, 7, 9],
    "7-28A": [0, 1, 3, 5, 6, 7, 9],
    "7-28B": [0, 2, 3, 4, 6, 8, 9],
    "7-29B": [0, 2, 3, 5, 7, 8, 9],
    "7-29A": [0, 1, 2, 4, 6, 7, 9],
    "7-30B": [0, 1, 3, 5, 7, 8, 9],
    "7-30A": [0, 1, 2, 4, 6, 8, 9],
    "7-31B": [0, 2, 3, 5, 6, 8, 9],  # octatonic scale
    "7-31A": [0, 1, 3, 4, 6, 7, 9],
    "7-32B": [0, 1, 3, 5, 6, 8, 9],
    "7-32A": [0, 1, 3, 4, 6, 8, 9],
    "7-33": [0, 1, 2, 4, 6, 8, 10],
    "7-34": [0, 1, 3, 4, 6, 8, 10],
    "7-35": [0, 1, 3, 5, 6, 8, 10],  # maj/min prime form
    "7-z36B": [0, 2, 3, 5, 6, 7, 8],
    "7-z36A": [0, 1, 2, 3, 5, 6, 8],
    "7-z37": [0, 1, 3, 4, 5, 7, 8],
    "7-z38B": [0, 1, 3, 4, 6, 7, 8],
    "7-z38A": [0, 1, 2, 4, 5, 7, 8],
    # 8-note sets
    "8-1": [0, 1, 2, 3, 4, 5, 6, 7],
    "8-2B": [0, 2, 3, 4, 5, 6, 7, 8],
    "8-2A": [0, 1, 2, 3, 4, 5, 6, 8],
    "8-3": [0, 1, 2, 3, 4, 5, 6, 9],
    "8-4B": [0, 1, 3, 4, 5, 6, 7, 8],
    "8-4A": [0, 1, 2, 3, 4, 5, 7, 8],
    "8-5B": [0, 1, 2, 4, 5, 6, 7, 8],
    "8-5A": [0, 1, 2, 3, 4, 6, 7, 8],
    "8-6": [0, 1, 2, 3, 5, 6, 7, 8],
    "8-7": [0, 1, 2, 3, 4, 5, 8, 9],
    "8-8": [0, 1, 2, 3, 4, 7, 8, 9],
    "8-9": [0, 1, 2, 3, 6, 7, 8, 9],
    "8-10": [0, 2, 3, 4, 5, 6, 7, 9],
    "8-11B": [0, 2, 4, 5, 6, 7, 8, 9],
    "8-11A": [0, 1, 2, 3, 4, 5, 7, 9],
    "8-12A": [0, 1, 3, 4, 5, 6, 7, 9],
    "8-12B": [0, 2, 3, 4, 5, 6, 8, 9],
    "8-13B": [0, 2, 3, 5, 6, 7, 8, 9],
    "8-13A": [0, 1, 2, 3, 4, 6, 7, 9],
    "8-14A": [0, 1, 2, 4, 5, 6, 7, 9],
    "8-14B": [0, 2, 3, 4, 5, 7, 8, 9],
    "8-z15B": [0, 1, 3, 5, 6, 7, 8, 9],  # all interval tetrachord!
    "8-z15A": [0, 1, 2, 3, 4, 6, 8, 9],
    "8-16B": [0, 1, 2, 4, 6, 7, 8, 9],
    "8-16A": [0, 1, 2, 3, 5, 7, 8, 9],
    "8-17": [0, 1, 3, 4, 5, 6, 8, 9],
    "8-18B": [0, 1, 3, 4, 6, 7, 8, 9],
    "8-18A": [0, 1, 2, 3, 5, 6, 8, 9],
    "8-19B": [0, 1, 3, 4, 5, 7, 8, 9],
    "8-19A": [0, 1, 2, 4, 5, 6, 8, 9],
    "8-20": [0, 1, 2, 4, 5, 7, 8, 9],
    "8-21": [0, 1, 2, 3, 4, 6, 8, 10],
    "8-22B": [0, 1, 2, 3, 5, 7, 9, 10],
    "8-22A": [0, 1, 2, 3, 5, 6, 8, 10],
    "8-23": [0, 1, 2, 3, 5, 7, 8, 10],
    "8-24": [0, 1, 2, 4, 5, 6, 8, 10],
    "8-25": [0, 1, 2, 4, 6, 7, 8, 10],
    "8-26": [0, 1, 3, 4, 5, 7, 8, 10],
    "8-27B": [0, 1, 2, 4, 6, 7, 9, 10],
    "8-27A": [0, 1, 2, 4, 5, 7, 8, 10],
    "8-28": [0, 1, 3, 4, 6, 7, 9, 10],
    "8-z29B": [0, 2, 3, 4, 6, 7, 8, 9],
    "8-z29A": [0, 1, 2, 3, 5, 6, 7, 9],
    # 9-note sets
    "9-1": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "9-2A": [0, 1, 2, 3, 4, 5, 6, 7, 9],
    "9-2B": [0, 2, 3, 4, 5, 6, 7, 8, 9],
    "9-3B": [0, 1, 3, 4, 5, 6, 7, 8, 9],
    "9-3A": [0, 1, 2, 3, 4, 5, 6, 8, 9],
    "9-4B": [0, 1, 2, 4, 5, 6, 7, 8, 9],
    "9-4A": [0, 1, 2, 3, 4, 5, 7, 8, 9],
    "9-5B": [0, 1, 2, 3, 5, 6, 7, 8, 9],
    "9-5A": [0, 1, 2, 3, 4, 6, 7, 8, 9],
    "9-6": [0, 1, 2, 3, 4, 5, 6, 8, 10],
    "9-7B": [0, 1, 2, 3, 4, 5, 7, 9, 10],
    "9-7A": [0, 1, 2, 3, 4, 5, 7, 8, 10],
    "9-8B": [0, 1, 2, 3, 4, 6, 8, 9, 10],
    "9-8A": [0, 1, 2, 3, 4, 6, 7, 8, 10],
    "9-9": [0, 1, 2, 3, 5, 6, 7, 8, 10],
    "9-10": [0, 1, 2, 3, 4, 6, 7, 9, 10],
    "9-11B": [0, 1, 2, 3, 5, 6, 8, 9, 10],
    "9-11A": [0, 1, 2, 3, 5, 6, 7, 9, 10],
    "9-12": [0, 1, 2, 4, 5, 6, 8, 9, 10],
}

# Ensemble sizes
ENSEMBLE_SIZES = {
    1: "solo",
    2: "duo",
    3: "trio",
    4: "quartet",
    5: "quintet",
    6: "sextet",
    7: "septet",
    8: "octet",
    9: "nonet",
    10: "decet",
    11: "large ensemble",
}

# Ensembles
"""
A dictionary of some template ensembles.

NOTE: obviously not complete or comprehensive. 
      just some standards that could use usefull when quick 
      templates are needed.
"""

ENSEMBLES = {
    # strings
    "string trio": ["Violin", "Viola", "Cello"],
    "string quartet": ["Violin", "Violin", "Viola", "Cello"],
    # plucked strings
    "duet: gtr/fl": ["Acoustic Guitar (nylon)", "Flute"],
    "duet: gtr/hp": ["Acoustic Guitar (nylon)", "Orchestral Harp"],
    "duet: e.gtr/e.bass": ["Electric Guitar (clean)", "Electric Bass (pick)"],
    "trio: fl/gtr/hp": ["Flute", "Acoustic Guitar (nylon)", "Orchestral Harp"],
    "guitar quartet": [
        "Acoustic Guitar (nylon)",
        "Acoustic Guitar (nylon)",
        "Acoustic Guitar (nylon)",
        "Acoustic Guitar (nylon)",
    ],
    # piano
    "duet: pno/vn": ["Violin", "Acoustic Grand Piano"],
    "duet: pno/va": ["Viola", "Acoustic Grand Piano"],
    "duet: pno/vc": ["Cello", "Acoustic Grand Piano"],
    "duet: pno/cl": ["Clarinet", "Acoustic Grand Piano"],
    "duet: pno/hn": ["French Horn", "Acoustic Grand Piano"],
    "trio: vn/vc/pno": ["Violin", "Cello", "Acoustic Grand Piano"],
    "trio: cl/vc/pno": ["Clarinet", "Cello", "Acoustic Grand Piano"],
    "trio: vn/bsn/pno": ["Violin", "Bassoon", "Acoustic Grand Piano"],
    "trio: cl/bsn/pno": ["Clarinet", "Bassoon", "Acoustic Grand Piano"],
    "quartet: 2vn/va/vc/pno": [
        "Violin",
        "Violin",
        "Viola",
        "Cello",
        "Acoustic Grand Piano",
    ],
    # brass
    # woodwinds
    "duet: fl/bsn": ["Flute", "Bassoon"],
    "duet: ob/bsn": ["Oboe", "Bassoon"],
    "duet: en/bsn": ["English Horn", "Bassoon"],
    "duet: ob/cl": ["Oboe", "Clarinet"],
    "trio: fl/ob/bsn": ["Flute", "Oboe", "Bassoon"],
    "trio: ob/en/bsn": ["Oboe", "English Horn", "Bassoon"],
    "sax trio 1": ["Soprano Sax", "Alto Sax", "Tenor Sax"],
    "sax trio 2": ["Alto Sax", "Tenor Sax", "Baritone Sax"],
    "sax quartet": ["Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax"],
    # orchestra (2222/2221/pno/strings) no percussion yet!
    "orchestra": {
        "winds": [
            "Flute",
            "Flute",
            "Oboe",
            "Oboe",
            "Clarinet",
            "Clarinet",
            "Bassoon",
            "Bassoon",
        ],
        "brass": [
            "French Horn",
            "French Horn",
            "Trumpet",
            "Trumpet",
            "Trombone",
            "Trombone",
            "Tuba",
        ],
        "piano": "Acoustic Grand Piano",
        "percussion": [],
        "strings": [
            "String Ensemble 1",  # violin 1
            "String Ensemble 2",  # violin 2
            "String Ensemble 1",  # violas
            "String Ensemble 2",  # cellos
            "String Ensemble 1",  # basses
        ],
    },
}

"""
List of each possible note for a limited set of instruments
Currently covers all of the orchestral instruments, plus a 
few others in CONCERT pitch!. 
"""
RANGE = {
    # -------------------------Orchestral---------------------------------#
    "Flute": [
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "Bb5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
    ],
    "Oboe": [
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
        "F6",
        "F#6",
        "G6",
    ],
    "Clarinet": [
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "Bb5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
    ],
    "Bassoon": [
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
    ],
    "French Horn": [
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
    ],
    "Trumpet": [
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
    ],
    "Trombone": [
        "Bb1",
        "B1",
        "C2",
        "C#2",
        "D2",
        "Eb2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
    ],
    "Tuba": [
        "E1",
        "F1",
        "F#1",
        "G1",
        "G#1",
        "A1",
        "Bb1",
        "B1",
        "C2",
        "C#2",
        "D2",
        "Eb2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
    ],
    "Violin": [
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "Bb5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
        "F6",
        "F#6",
        "G6",
        "G#6",
        "A6",
        "Bb6",
        "B6",
        "C7",
        "C#7",
        "D7",
        "Eb7",
        "E7",
    ],
    "Viola": [
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "Bb5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
        "F6",
        "F#6",
        "G6",
        "G#6",
        "A6",
    ],
    "Cello": [
        "C2",
        "C#2",
        "D2",
        "Eb2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
    ],
    "Contrabass": [
        "C1",
        "C#1",
        "D1",
        "Eb1",
        "E1",
        "F1",
        "F#1",
        "G1",
        "G#1",
        "A1",
        "Bb1",
        "B1",
        "C2",
        "C#2",
        "D2",
        "Eb2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
    ],
    # -------------------------------------Others---------------------------------------#
    "Guitar": [
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "Eb5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "Bb5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "Eb6",
        "E6",
        "F6",
        "F#6",
        "G6",
        "G#6",
        "A6",
        "Bb6",
        "B6",
    ],
    "Bass": [
        "E1",
        "F1",
        "F#1",
        "G1",
        "G#1",
        "A1",
        "Bb1",
        "B1",
        "C2",
        "C#2",
        "D2",
        "Eb2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "Bb2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "Eb3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "Bb3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "Eb4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "Bb4",
        "B4",
    ],
}

# MIDI instruments list (standard)
# NOTE: indices 0 - 110 are MELODIC/HARMONIC instruments!
INSTRUMENTS = [
    # 0-8: keyboards
    "Acoustic Grand Piano",
    "Bright Acoustic Piano",
    "Electric Grand Piano",
    "Honky-tonk Piano",
    "Electric Piano 1",
    "Electric Piano 2",
    "Harpsichord",
    "Clavinet",
    "Celesta",
    # 9-15: metal/wood pitched percussion
    "Glockenspiel",
    "Music Box",
    "Vibraphone",
    "Marimba",
    "Xylophone",
    "Tubular Bells",
    "Dulcimer",
    # 16-20: organs
    "Drawbar Organ",
    "Percussive Organ",
    "Rock Organ",
    "Church Organ",
    "Reed Organ",
    # 21-23: accordions/harmonica
    "Accordion",
    "Harmonica",
    "Tango Accordion",
    # 24-31: guitars
    "Acoustic Guitar (nylon)",
    "Acoustic Guitar (steel)",
    "Electric Guitar (jazz)",
    "Electric Guitar (clean)",
    "Electric Guitar (muted)",
    "Overdriven Guitar",
    "Distortion Guitar",
    "Guitar Harmonics",
    # 32-39: basses
    "Acoustic Bass",
    "Electric Bass (finger)",
    "Electric Bass (pick)",
    "Fretless Bass",
    "Slap Bass 1",
    "Slap Bass 2",
    "Synth Bass 1",
    "Synth Bass 2",
    # 40-45: strings
    "Violin",
    "Viola",
    "Cello",
    "Contrabass",
    "Tremolo Strings",
    "Pizzicato Strings",
    # 46: harp
    "Orchestral Harp",
    # 47: timpani
    "Timpani",
    # 48-51 : string ensembles
    "String Ensemble 1",
    "String Ensemble 2",
    "Synth Strings 1",
    "Synth Strings 2",
    # 52-54: choirs
    "Choir Aahs",
    "Voice Oohs",
    "Synth Choir",
    # 55: orchestra hit
    "Orchestra Hit",
    # 56-63: brass
    "Trumpet",
    "Trombone",
    "Tuba",
    "Muted Trumpet",
    "French Horn",
    "Brass Section",
    "Synth Brass 1",
    "Synth Brass 2",
    # 64-67: saxes
    "Soprano Sax",
    "Alto Sax",
    "Tenor Sax",
    "Baritone Sax",
    # 68-79: woodwinds
    "Oboe",
    "English Horn",
    "Bassoon",
    "Clarinet",
    "Piccolo",
    "Flute",
    "Recorder",
    "Pan Flute",
    "Blown bottle",
    "Shakuhachi",
    "Whistle",
    "Ocarina",
    # 80-95: synth leads & pads
    "Lead 1 (square)",
    "Lead 2 (sawtooth)",
    "Lead 3 (calliope)",
    "Lead 4 chiff",
    "Lead 5 (charang)",
    "Lead 6 (voice)",
    "Lead 7 (fifths)",
    "Lead 8 (bass + lead)",
    "Pad 1 (new age)",
    "Pad 2 (warm)",
    "Pad 3 (polysynth)",
    "Pad 4 (choir)",
    "Pad 5 (bowed)",
    "Pad 6 (metallic)",
    "Pad 7 (halo)",
    "Pad 8 (sweep)",
    # 96-103: misc FX
    "FX 1 (rain)",
    "FX 2 (soundtrack)",
    "FX 3 (crystal)",
    "FX 4 (atmosphere)",
    "FX 5 (brightness)",
    "FX 6 (goblins)",
    "FX 7 (echoes)",
    "FX 8 (sci-fi)",
    # 104-111: other plucked string instruments
    "Sitar",
    "Banjo",
    "Shamisen",
    "Koto",
    "Kalimba",
    "Bagpipe",
    "Fiddle",
    "Shanai",
    # Indices 112 onward are non-pitched percussion instruments and
    # other misc. sound effects
    "Tinkle Bell",
    "Agogo",
    "Steel Drums",
    "Woodblock",
    "Taiko Drum",
    "Melodic Tom",
    "Synth Drum",
    "Reverse Cymbal",
    "Guitar Fret Noise",
    "Breath Noise",
    "Seashore",
    "Bird Tweet",
    "Telephone Ring",
    "Helicopter",
    "Applause",
    "Gunshot",
]
