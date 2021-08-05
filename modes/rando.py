'''
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title, 
'''

#IMPORTS
import midi as m
import constants as c
from random import randint
from generate import generate as create
from containers.composition import composition
'''
------------------------------------------------------NOTES--------------------------------------------------------------
    ALGORITHM:

    0. Pure random. RNG rules all.
        0.1. Decide on number of instruments

        0.2. Decide global tempo (invariant... for now)

        0.3. For each instrument, generate n number of notes and/or chords (not restricted to human playability). Each
             instrument will decide whether it only plays notes, chords, or both.
            0.3.1. Generate list of randomly selected note names in randomly selected octaves of n length.
            0.3.2. Generate list of individual lists of random note names in random octaves of n length.
                0.3.2.1. Each sub-list is a "chord"
                0.3.2.2. Each chord's voicings will be randomized.
            0.3.3. Generate durations for each note or chord (must not repeat any previous duration!)
                0.3.3.1. If a repeated value is found, take prev occurance value and either augment 
                         or diminish it by n. Check for duplicates and continue loop until no other
                         duplicates are found.
                0.3.3.2. Chord durations are defined as a set of integers attached to a common time duration.
            0.3.4 Generate dynamics for each chord

------------------------------------------------------------------------------------------------------------------------
'''
#Pure "random" mode
def newRandomComposition(self):
    '''
    Generates a composition with n number of harmony and melody instruments. Each part creates its own
    source material at random. Exports a MIDI file, a .txt file with composition info, and returns a 
    composition() object.
    '''
    # new composition object
    comp = composition()

    # indicate no inputted source data
    comp.sourceData.append("None")
    # pick global tempo
    comp.tempo = create.newTempo()
    # pick title
    comp.title = create.newTitle()

    # pick ensemble size (1 - 11 isntruments for now)
    size = randint(1, len(c.ENSEMBLE_SIZES))
    # ensemble size string ("duo, trio," etc...)
    comp.ensemble = c.ENSEMBLE_SIZES[size]
    comp.instruments = create.newInstruments(size)
    
    # how many melody instruments?
    total_melodies = randint(1, size - 1)
    # how many harmony instruments? use remaining number
    total_harmonies = size - total_melodies

    # pick melodies.
    for i in range(total_melodies):
        melody = create.newMelody(tempo=comp.tempo)
        if(melody != -1):
            comp.melodies.append(melody)
        else:
            continue

    # pick harmonies
    for i in range(total_harmonies):
        chord = create.newChord(tempo=comp.tempo)
        if(chord != -1):
            comp.chords.append(chord)
        else:
            continue

    # export to MIDI file

    # generate .txt file

    return comp