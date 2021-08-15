'''
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title, 
melodies, and harmonies are all independtly generated, united only by a global tempo. Length of each part
may vary substantially, as well as the instrumentation.
'''

#IMPORTS
import core.midi as mid
import core.constants as c
from core.generate import Generate
from containers.composition import Composition

from random import randint
from utils.save import saveInfo
from datetime import datetime as date

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
            0.3.3. Generate durations for each note or chord
                0.3.3.1. Chord durations are defined as a set of integers attached to a common time duration.
            0.3.4 Generate dynamics for each chord

------------------------------------------------------------------------------------------------------------------------
'''

# Pure "random" mode
def newRandomComposition():
    '''
    Generates a composition with 1-11 melody and/or harmony instruments under a unified tempo. 
    Each part's source material will be independently generated, or won't use any input at all.
    
    Exports a MIDI file, a .txt file with composition info. 
    
    Returns a composition() object, or -1 on failure.

    NOTE: Need a way to decide whether to compose a single melodic, harmonic, or percussive instrument, if
          1 is chosen as the ensemble size.
    '''
    # new generate object
    create = Generate()
    # new composition object
    comp = Composition()
    '''
    NOTE: alternative composition() object initialization approach?
    comp = Composition(

        # generate title
        title = create.newTitle(),
        # add composer
        composer = "Rando Calrissian",
        
        # Add date and time.
        dn = date.now()
        # convert to str d-m-y hh:mm:ss
        date = dn.strftime("%d-%b-%y %H:%M:%S")

        # pick global tempo
        tempo = create.newTempo()

        # pick ensemble size (1 - 11 instruments for now)
        # and instrumentation
        size = randint(1, len(c.ENSEMBLE_SIZES) - 1)
        ensemble = c.ENSEMBLE_SIZES[size]
        # NOTE: the first entries will always be melodic instruments!
        # might want to vary things a bit... 
        instruments = create.newInstruments(size)
    )
    '''
    # pick title
    comp.title = create.newTitle()
    # add composer info
    '''NOTE: add random name method? Why not.'''
    comp.composer = "Rando Calrissian"

    # Add date and time.
    dn = date.now()
    # convert to str d-m-y hh:mm:ss
    comp.date = dn.strftime("%d-%b-%y %H:%M:%S")

    # pick global tempo
    comp.tempo = create.newTempo()

    # pick ensemble size (1 - 11 instruments for now)
    # and instrumentation
    size = randint(1, len(c.ENSEMBLE_SIZES) - 1)
    comp.ensemble = c.ENSEMBLE_SIZES[size]
    # NOTE: the first entries will always be melodic instruments!
    # might want to vary things a bit... 
    comp.instruments = create.newInstruments(size)
    
    # how many melody instruments?
    total_melodies = randint(0, size)
    # pick melodies.
    if total_melodies > 0:
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
    if mid.save(comp) != -1:
        print("\n...", comp.title, "saved as", comp.midiFileName)
    else:
        print("\nnewRandomComposition() - ERROR: unable to generate random composition!")
        return -1

    # generate .txt file and titles with all instruments listed
    comp.txtFileName = "{}{}".format(comp.title, '.txt')
    if size == 1:
        title_full = "{}{}{}".format(comp.title, 'for solo', comp.melodies[0].instrument)
    elif size > 1:
        title_full = "{}{}{}".format(comp.title, 'for mixed', comp.ensemble)
    if saveInfo(name=title_full, fileName=comp.txtFileName, newMusic=comp) != 0:
        print("\nText file saved as:", comp.txtFileName)
    else:
        return -1

    
    '''
    NOTE: consolidate title/str generation above then place this if-statement below:

    if mid.save(comp) !=-1 and saveInfo(name=title_full, fileName=comp.txtFileName, newMusic=comp) != 0:
        if comp.ensemble == "solo":
            print("\nNew composition:", comp.title, "for solo", comp.instruments[0])
        else:
            print("\nNew composition:", comp.title, "for mixed", comp.ensemble)
        print("\n...", comp.title, "saved as", comp.midiFileName)
        print("\nText file saved as:", comp.txtFileName)
        return 0
    else:
        print("\n...Unable to generate random composition!")
        return -1
    '''

    # display results
    if comp.ensemble == "solo":
        print("\nNew composition:", comp.title, "for solo", comp.instruments[0])
    else:
        print("\nNew composition:", comp.title, "for mixed", comp.ensemble)

    return comp