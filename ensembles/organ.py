"""
this module composes a short, slow piece for organ,
with or without a melody
"""

# Imports
from random import randint

from utils.midi import save

from core.generate import Generate
from core.constants import TEMPOS


def organ(tempo=None):
    """
    generates a short piece with chords for organ
    """
    print("\nwriting organ piece...")

    create = Generate()
    if tempo is None:
        tempo = TEMPOS[randint(7, 12)]
    comp = create.init_comp(tempo=tempo)
    comp.instruments.append("Reed Organ")
    title_full = comp.title + " for solo organ"

    # generate 2-5 chords based off 2-4
    # randomly chosen and built scales between octaves 2 - 3
    source_scale = create.new_source_scale(root=create.pick_root()[0])
    chords = create.new_chords(total=randint(2, 5), tempo=comp.tempo, scale=source_scale)
    for chord in range(len(chords)):
        chords[chord].instrument = "Reed Organ"
    comp.add_part(chords, chords[0].instrument)

    # write out to MIDI file & display results
    save(comp)
    comp.display()


if __name__ == "__main__":
    organ()
