'''
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title, 
melodies, and harmonies are all independtly generated, united only by a global tempo. Length of each part
may vary substantially, as well as the instrumentation.
'''

#IMPORTS
from core.generate import Generate
from core.constants import ENSEMBLE_SIZES

from containers.composition import Composition

import utils.midi as mid
from utils.txtfile import save_info
from utils.data import new_data

from random import randint, choice
from datetime import datetime as date


# Pure "random" mode
def new_random_composition():
    '''
    Generates a composition with 1-11 melody and/or harmony instruments under a unified tempo. 
    Each part's material will be independently generated, with or without auto-generated source 
    data for the melody parts.
    
    Exports a MIDI file and a .txt file with composition info. 
    
    Returns a composition() object, or -1 on failure.

    TODO: Need a way to decide whether to compose a single melodic, harmonic, or percussive instrument, if
          ensemble size == 1.
    '''
    print("\ngenerating new composition...")

    create = Generate()
    comp = Composition()
    comp.title = create.new_title()
    comp.composer = create.new_composer()
    comp.tempo = create.new_tempo()
    comp.date = date.now().strftime("%b-%d-%y %H:%M:%S")

    # pick ensemble size (1 - 11 instruments for now) and instrumentation
    size = randint(1, 11)
    print("\ntotal instruments:", size)
    comp.ensemble = ENSEMBLE_SIZES[size]
    # generate instrument list. 
    instruments = create.new_instruments(size)
    print("instruments:", instruments)

    # how many melody instruments?
    total_melodies = randint(0, size)

    if total_melodies > 0:
        print("\npicking", total_melodies, "melodies...")
        for i in range(total_melodies):
            # use randomly chosen source data
            if randint(1, 2) == 1:
                dt = randint(1,4)
                data = newData(dt)
                melody = create.new_melody(tempo=comp.tempo, data=data, dataType=dt)
            # ... or not
            else:
                melody = create.new_melody(tempo=comp.tempo)
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
            # generate chords
            chords = create.new_chords(total=total, tempo=comp.tempo)
            # pick instrument and assign to *all* chords in this progression
            instr = choice(instruments)
            for c in range(len(chords)):
                chords[c].instrument = instr
            instruments.remove(instr)
            comp.instruments.append(instr)
            # save chord progression to comp chord dictionary
            comp.chords[key] = chords
            key+=1

    # generate MIDI and .txt file names
    print("\ngenerating file names...")
    comp.midi_file_name = "{}{}".format(comp.title, ".mid")
    print("...MIDI file:", comp.midi_file_name)
    # comp.txt_file_name = "{}{}".format(comp.title, '.txt')
    # print("...text file:", comp.txt_file_name)
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
    d = comp.duration()
    if d > 60.0:
        d/=60.0
        print("duration:", d, "minutes")
    else:
        print("duration:", d, "seconds")
    print("midi file:", comp.midi_file_name)
    # print("text file:", comp.txtFileName)
    print()
    return comp