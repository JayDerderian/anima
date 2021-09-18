'''
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title, 
melodies, and harmonies are all independtly generated, united only by a global tempo. Length of each part
may vary substantially, as well as the instrumentation.
'''

#IMPORTS
# import core.constants as c
from core.constants import ENSEMBLE_SIZES
from core.generate import Generate
from containers.composition import Composition
from utils.save import saveInfo
import utils.midi as mid

from random import randint, choice
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
    Each part's material will be independently generated, with or without auto-generated source 
    data.
    
    Exports a MIDI file and a .txt file with composition info. 
    
    Returns a composition() object, or -1 on failure.

    TODO: Modify to create an ensemble list not stored in comp! each time an instrument is picked, remove it from
          this list. once complete, THEN append all instruments to comp.instruments

    NOTE: Need a way to decide whether to compose a single melodic, harmonic, or percussive instrument, if
          ensemble size == 1.
    '''
    print("\ngenerating new composition...")

    # new generate object
    create = Generate()
    # new composition object
    comp = Composition()

    # Generate title, composer name, and pick tempo
    comp.title = create.newTitle()
    comp.composer = create.newComposer()
    comp.tempo = create.newTempo()
    comp.date = date.now().strftime("%b-%d-%y %H:%M:%S")

    # pick ensemble size (1 - 11 instruments for now) and instrumentation
    size = randint(1, 11)
    print("\ntotal instruments:", size)
    comp.ensemble = ENSEMBLE_SIZES[size]
    # generate instrument list. remove instr from this
    # list when chosen! append chosen instr to comp.instruments
    instruments = create.newInstruments(size)
    print("instruments:", instruments)

    # how many melody instruments?
    total_melodies = randint(0, size)

    if total_melodies > 0:
        print("\npicking", total_melodies, "melodies...")
        for i in range(total_melodies):
            '''NOTE: use randomly chosen source data at some point????'''
            melody = create.newMelody(tempo=comp.tempo)
            # assign a randomly-chosen instrument to this melody
            instr = choice(instruments)
            melody.instrument = instr
            # remove from original ist
            instruments.remove(instr)
            # save to comp.instruments
            comp.instruments.append(instr)
            # save the melody
            comp.melodies.append(melody)

    # how many harmony instruments? 
    total_harmonies = size - total_melodies

    if total_harmonies > 0:
        print("\npicking", total_harmonies, "chords...")
        key = 0
        for i in range(total_harmonies):
            # total chords in this progression
            total = randint(3, 15)
            print("\nchord progression", i, "has", total, "chords...")
            # generate chords
            chords = create.newChords(total=total, tempo=comp.tempo)
            # pick instrument and assign to *all* chords in this progression
            instr = choice(instruments)
            for c in range(len(chords)):
                chords[c].instrument = instr
            instruments.remove(instr)
            comp.instruments.append(instr)
            # save chord to comp chord dictionary
            comp.chords[key] = chords
            key+=1

    # generate MIDI and .txt file names
    print("\ngenerating file names...")
    comp.midiFileName = "{}{}".format(comp.title, ".mid")
    print("...MIDI file:", comp.midiFileName)
    # comp.txtFileName = "{}{}".format(comp.title, '.txt')
    # print("...text file:", comp.txtFileName)
    if size == 1:
        if len(comp.melodies) > 1:
            title_full = "{}{}{}".format(comp.title, ' for solo ', comp.melodies[0].instrument)
        elif len(comp.chords) > 1:
            title_full = "{}{}{}".format(comp.title, ' for solo ', comp.chords[0].instrument)
    elif size > 1:
        title_full = "{}{}{}".format(comp.title, ' for mixed ', comp.ensemble)

    # export to MIDI file and .txt file
    mid.save(comp)     
    # saveInfo(name=title_full, fileName=comp.txtFileName, newMusic=comp) 
    
    # Display results
    print("\ntitle:", title_full)
    print("composer:", comp.composer)
    print("date", comp.date)
    print("tempo:", comp.tempo)
    print("midi file saved as:", comp.midiFileName)
    # print("Text file saved as:", comp.txtFileName)
    print()
    return comp