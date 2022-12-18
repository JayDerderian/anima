"""
This module handles creating a purely "random" composition. Tempo, ensemble size, instruments, title,
melodies, and harmonies are all independently generated, united only by a global tempo. Length of each part
may vary substantially, as well as the instrumentation.
"""

# IMPORTS
from core.generate import Generate
from core.constants import ENSEMBLE_SIZES

import utils.midi as mid
from utils.data import new_data

from random import randint, choice


# Pure "random" mode
def new_random_composition():
    """
    Generates a composition with 1-11 melody and/or harmony instruments under a unified tempo.
    Each part's material will be independently generated, with or without auto-generated source
    data for the melody parts.

    Exports a MIDI file and a .txt file with composition info.

    Returns a composition() object, or -1 on failure.

    TODO: Need a way to decide whether to compose a single melodic, harmonic, or percussive instrument, if
          ensemble size == 1.
    """
    print("\ngenerating new composition...")

    create = Generate()
    comp = create.init_comp()

    # pick ensemble size (1 - 11 instruments for now) and instrumentation
    size = randint(1, 11)
    print("\ntotal instruments:", size)
    comp.ensemble = ENSEMBLE_SIZES[size]
    instruments = create.new_instruments(total=size)
    print("instruments:", instruments)

    # how many melody instruments?
    total_melodies = randint(0, size)

    if total_melodies > 0:
        print("\npicking", total_melodies, "melodies...")
        for i in range(total_melodies):
            # use randomly chosen source data
            if randint(1, 2) == 1:
                data_type = randint(1, 4)
                data = new_data(data_type)
                melody = create.new_melody(tempo=comp.tempo,
                                           data=data, data_type=data_type)
            # ... or not
            else:
                melody = create.new_melody(tempo=comp.tempo)
            # assign a randomly-chosen instrument to this melody
            instr = choice(instruments)
            melody.instrument = instr
            # remove from original ist
            instruments.remove(instr)
            # save the melody
            comp.add_part(melody, melody.instrument)

    # how many harmony instruments? 
    total_harmonies = size - total_melodies

    if total_harmonies > 0:
        print("\npicking", total_harmonies, "chords...")
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
            comp.add_part(chords, instr)

    # export to MIDI file and .txt file
    mid.save(comp)
    comp.display()

    return comp


if __name__ == "__main__":
    new_random_composition()
