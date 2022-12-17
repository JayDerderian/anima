"""
A quartet whose music is a series of rapid, soft
chords that slowly swell and recede.

consistent 16ths at roughly 55 - 64 bpm, add in dotted
16ths in odd groupings (3, 5, 7 at most) to occasionally
pull against the constant pulse
"""

# Imports
from random import randint, choice
from datetime import datetime as date

from utils.midi import save
from utils.tools import scale_to_tempo

from core.constants import TEMPOS, DYNAMICS
from core.generate import Generate

from containers.composition import Composition


def mixed_qtet(ensemble=None):
    """
    A quartet whose music is a series of rapid, soft
    chords that slowly swell and recede.

    consistent 16ths at roughly 55 - 64 bpm, add in dotted
    16ths in odd groupings (3, 5, 7 at most) to occasionally
    pull against the constant pulse
    """
    print("\nwriting new mixed quartet...")
    create = Generate()
    comp = create.init_comp()
    title_full = f"{comp.title} for mixed quartet"

    print("\npicking instruments...")
    if ensemble is None:
        e = create.new_instruments(4)
    else:
        e = ensemble
    comp.instruments = e
    comp.ensemble = "quartet"

    t = randint(5, 9)  # total chords
    mode, mode_pcs, mode_notes = create.pick_scale(transpose=True)  # pick starting mode
    source = create._new_source_scale(mode_notes)  # generate source scale from mode

    print("\ngenerating", t, "chords...")
    # generate chords from source scale. each chord will be repeated either
    # 64x with 16th notes or 18x with dotted sixteenth notes
    chords = create.new_chords(total=t, tempo=comp.tempo, scale=source)

    # this list will store each repeated chord object with its growing and
    # reseeding dynamics values. once this is finished it'l be dispersed across
    # each c1..c4 list, then each list will get their instruments assigned to
    # each individual chord object.
    prog = []

    # generate swells
    print("\nadding dynamic patterns...")
    '''
    swell patterns for each chord

    4 bars in length (approximately, and for now) for the swell,
    and 4 more bars for the receed. repeat for each chord.

    swell/recession is retrograde of this patten (128 16ths total)
    36(x8), 38(8x), 40(8x), 42(8x), 48(8x), 50(8x), 52(8x), 54(8x)

    # dotted sixteenth swell/recession (18 dotted 16th's)
    92(6x), 96(6x), 100(6x)  
    '''
    for chrd in range(len(chords)):
        '''
        NOTE: find a way to modify these loops according to
              the value of i in the main for-loop to differentiate different
              swells'''
        # get current chord
        chord = chords[chrd]
        # add tempo adherent 16th note
        chord.rhythm = scale_to_tempo(tempo=comp.tempo, rhythms=0.25)
        # repeat each dynamic for the swell/reseed 8x and append to prog list
        # repeat these 4 dynamics 8 times each...
        dyn = 4
        for j in range(4):
            for k in range(8):
                chord.dynamic = DYNAMICS[dyn]
                prog.append(chord)
            dyn += 1
        dyn = 8
        for j in range(4):
            for k in range(8):
                chord.dynamic = DYNAMICS[dyn]
                prog.append(chord)
            dyn -= 1

    # test output
    print("\nfinal chord total:", len(prog))

    # assign instruments
    print("\nassigning instruments...")
    c1 = prog
    c2 = prog
    c3 = prog
    c4 = prog
    print("...adding", e[0])
    for i in range(len(c1)):
        c1[i].instrument = e[0]
    print("...adding", e[1])
    for i in range(len(c2)):
        c2[i].instrument = e[1]
    print("...adding", e[2])
    for i in range(len(c3)):
        c3[i].instrument = e[2]
    print("...adding", e[3])
    for i in range(len(c4)):
        c4[i].instrument = e[3]

    # save final chord lists
    for part in [c1, c2, c3, c4]:
        # only need to add the instrument from the
        # first object since they're all the same
        comp.add_part(part, part[0].instrument)

    # write out
    save(comp)
    # display results
    output = f"title: {title_full}" \
             f"date: {comp.date}" \
             f"composer: {comp.composer}" \
             f"instruments: {comp.instruments}," \
             f"duration: {comp.duration()}\n"
    print(output)
    return "\nhooray!"
