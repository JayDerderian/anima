'''
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title, 
melodies, and harmonies are all independtly generated, united only by a global tempo. Length of each part
may vary substantially, as well as the instrumentation.
'''

#IMPORTS
from midi import save
import constants as c
# from test import newData
from random import randint
from generate import Generate
from datetime import datetime as date
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

# Pure "random" mode
def newRandomComposition():
    '''
    Generates a composition with n number of harmony and melody instruments. 
    At least 1 melody will be generated, though up to 11 parts - both melodic and harmonic - could be created.
    
    Each part creates its own source material at random. 
    
    Exports a MIDI file, a .txt file with composition info. 
    
    Returns a composition() object, or -1 on failure.
    '''
    # new generate object
    create = Generate()
    # new composition object
    comp = composition()

    # pick title
    comp.title = create.newTitle()
    # add composer info
    comp.composer = "Rando Calrissian"

    # Add date and time.
    dn = date.now()
    # convert to str d-m-y hh:mm:ss
    comp.date = dn.strftime("%d-%b-%y %H:%M:%S")

    # pick global tempo
    comp.tempo = create.newTempo()

    # pick ensemble size (1 - 11 isntruments for now)
    size = randint(1, len(c.ENSEMBLE_SIZES) - 1)
    comp.ensemble = c.ENSEMBLE_SIZES[size]
    # NOTE: the first entries will always be melodic instruments! 
    comp.instruments = create.newInstruments(size)
    
    # how many melody instruments?
    total_melodies = randint(1, size)
    # pick melodies.
    for i in range(total_melodies):
        # NOTE: use randomly chosen source data at some point????
        melody = create.newMelody(tempo=comp.tempo)
        if melody != -1:
            # assign an instrument to this melody
            melody.instrument = comp.instruments[i]
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
        for j in range(total_harmonies):
            # harmonies are NOT generated from melodies here!
            chord = create.newChord(tempo=comp.tempo)
            if chord != -1:
                # add instrument
                chord.instrument = comp.instruments[i]
                comp.chords.append(chord)
                i+=1
                if i == len(comp.instruments):
                    break
            else:
                print("\nnewRandomComposition() - ERROR: unable to generate harmony!")
                return -1

    # export to MIDI file
    comp.midiFileName = "{}{}".format(comp.title, ".mid")
    if save(comp) != -1:
        print("\n...", comp.title, "saved as", comp.midiFileName)
    else:
        print("\nUnable to generate random composition!")
        return -1

    # generate .txt file and titles with all instruments listed
    comp.txtFileName = "{}{}".format(comp.title, '.txt')
    if size == 1:
        title_full = "{}{}{}".format(comp.title, 'for solo', comp.melodies[0].instrument)
    elif size > 1:
        title_full = "{}{}{}".format(comp.title, 'for mixed', comp.ensemble)
        # for i in range(comp.melodies):
        #     if i == size - 1:
        #         title_full += "and " 
        #         title_full += comp.melodies[i].instrument
        #         break
        #     title_full += ", " 
        #     title_full += comp.melodies[i].instrument
        # if len(comp.chords) > 0:
        #     for i in range(len(comp.chord)):
        #         if i == size - 1:
        #             title_full += "and " 
        #             title_full += comp.chords[i].instrument
        #             break
        #         title_full += ", " 
        #         title_full += comp.chords[i].instrument
    if create.saveInfo(name=title_full, fileName=comp.txtFileName, newMusic=comp) != 0:
        print("\nText file saved as:", comp.txtFileName)
        return -1

    # display results
    if comp.ensemble == "solo":
        print("\nNew composition:", comp.title, "for solo", comp.instruments[0])
    else:
        print("\nNew composition:", comp.title, "for mixed", comp.ensemble)

    return comp