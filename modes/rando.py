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
def newRandomComposition():
    '''
    Generates a composition with n number of harmony and melody instruments. At least 1 melody will be generated,
    though up to 11 parts - both melodic and harmonic - could be created.
    
    Each part creates its own source material at random. 
    
    Exports a MIDI file, a .txt file with composition info, and returns a 
    composition() object, or -1 on failure.
    '''
    # new composition object
    comp = composition()

    # pick title
    comp.title = create.newTitle()
    # add composer info
    comp.composer = "Rando Calrissian"

    # pick global tempo
    comp.tempo = create.newTempo()

    # pick ensemble size (1 - 11 isntruments for now)
    size = randint(1, len(c.ENSEMBLE_SIZES) - 1)
    comp.ensemble = c.ENSEMBLE_SIZES[size]
    comp.instruments = create.newInstruments(size)
    
    # how many melody instruments?
    total_melodies = randint(1, size)
    # pick melodies.
    for i in range(total_melodies):
        melody = create.newMelody(tempo=comp.tempo)
        '''NOTE: need a way to terminate function without ending calling
                 method '''
        if melody != -1:
            # assign an instrument to this melody
            melody.instrument = comp.instruments[i]
            # save each melody's source data, as applicable.
            # this will just be a list of "none inputted" strings, in this mode.
            comp.sourceData.append(melody.sourceData)
            # save the melody
            comp.melodies.append(melody)
        else:
            print("\nnewRandomComposition() - ERROR: unable to generate melody!")
            return -1
            
    # how many harmony instruments? use remaining number
    # will be 0 if 1 is chosen as the ensemble size.
    total_harmonies = size - total_melodies
    # pick harmonies, if applicable
    if total_harmonies > 0:
        for i in range(total_harmonies):
            # harmonies are NOT generated from melodies here!
            chord = create.newChord(tempo=comp.tempo)
            if chord != -1:
                comp.chords.append(chord)
            else:
                print("\nnewRandomComposition() - ERROR: unable to generate harmony!")
                return -1

    # export to MIDI file
    # if m.save(comp) != -1:
    #     print("\n")
    # else:
    #     print("\nUnable to generate random composition!")
    #     return -1

    # generate .txt file
    comp.fileName = "{}{}".format(comp.title, '.txt')
    print("\nText file saved as:", comp.fileName)
    if size == 1:
        title_full = "{}{}{}".format(comp.title, 'for solo', comp.melodies[0].instrument)
    elif size > 1:
        title_full = "{}{}".format(comp.title, 'for', comp.melodies[0].instrument)
        for i in range(size):
            if i == size - 1:
                title_full += "and " 
                title_full += comp.melodies[i].instrument
                break
            title_full += ", " 
            title_full += comp.melodies[i].instrument


    print("\nTitle:", title_full)
    create.saveInfo(name=comp.title, fileName=comp.fileName, newMusic=comp)

    return comp