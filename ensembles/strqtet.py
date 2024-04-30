"""
this module generates a string quartet.

the piece opens with a series of chords, followed by a section of free counterpoint.
at some point each performer plays their part of the opening chords, asynchronously of each other,
then play a repeated series of notes who's rhythms get faster and faster until all parts are
playing 16th notes, then the piece ends.
"""

from tqdm import trange
from random import randint, seed

from utils.midi import export_midi
from utils.tools import scale_to_tempo
from utils.txtfile import gen_info_doc

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, RHYTHMS, TEMPOS

from containers.melody import Melody
from containers.composition import Composition


def str_qtet(tempo=None) -> Composition:
    """
    creates a choral for string quartet using a randomly chosen mode
    """

    # initialize
    create = Generate()
    if tempo is None:
        comp = create.init_comp(TEMPOS[randint(20, 27)])  # 100 - 126bpm
    else:
        comp = create.init_comp(tempo)
    comp.ensemble = "quartet"

    # create our quartet
    qtet = [
        Melody(tempo=comp.tempo, instrument="Violin"),
        Melody(tempo=comp.tempo, instrument="Violin"),
        Melody(tempo=comp.tempo, instrument="Viola"),
        Melody(tempo=comp.tempo, instrument="Cello"),
    ]

    print("\nwriting new string quartet...")

    # pick initial notes.
    mode, pcs, notes = create.pick_scale(transpose=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    # export_midi source info to each Melody() object
    for q in range(len(qtet)):
        qtet[q].pcs.append(pcs)
        qtet[q].source_notes = source

    print("\nwriting opening...")

    # write individual *choral* lines
    total = randint(12, 30)
    for q in range(len(qtet)):
        qtet[q] = write_line(qtet[q], source, total, create)

    # create rhythms
    rhy = []
    for rhythm in range(total):
        # use slower rhythms
        rhy.append(RHYTHMS[randint(1, 4)])

    # create dynamics
    dyn = create.new_dynamics(total=total)

    # add rhy & dyn to each part
    for q in range(len(qtet)):
        qtet[q].rhythms.extend(rhy)
        qtet[q].dynamics.extend(dyn)

    # export_midi original values in temp object
    qtet_orig = qtet

    print("\nwriting asynchronous lines...")

    mode, pcs, notes = create.pick_scale(transpose=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs, "\n")

    for q in trange((len(qtet)), desc="progress"):
        qtet[q] = write_line(qtet[q], source, total, create, asyn=True)
        qtet[q].source_notes.extend(source)
        qtet[q].pcs.append(pcs)

    print("\nrecapitulating choral opening at displaced end points...")

    for q in trange((len(qtet)), desc="progress"):
        qtet[q].notes.extend(qtet_orig[q].notes)
        qtet[q].rhythms.extend(qtet_orig[q].rhythms)
        qtet[q].dynamics.extend(qtet_orig[q].dynamics)

    print("\ngenerating ending figure and repeating until closure...")

    figs = []
    for q in trange((len(qtet)), desc="progress"):
        qtet[q], f = build_ending(qtet[q])
        figs.append(f)

    durations = []
    for q in range(len(qtet)):
        durations.append(qtet[q].duration())
    longest_part = max(durations)

    print("\nsyncing...")

    for q in trange((len(qtet)), desc="progress"):
        if qtet[q].duration() < longest_part:
            qtet[q] = sync(qtet[q], longest_part, figs[q])

    # export_midi all parts then write out
    for q in range(len(qtet)):
        comp.add_part(qtet[q], qtet[q].instrument)
    export_midi(comp)
    gen_info_doc(file_name=comp.txt_file_name, comp=comp, data=None)

    print("\n...success!")

    # display results
    comp.display()

    return comp


## Helpers ###


def write_line(
        part: Melody, scale: list, total: int, create: Generate, asyn: bool = False
) -> Melody:
    """
    writes each individual melodic line for each part.
    **doesn't add rhythm or dynamics** if asyn==False,
    which it is by default. if asyn==true, then any supplied
    total will be overwritten! still working on that
    quirk...

    returns a modified Melody() object
    """
    if asyn:
        # NOTE: this will redefine supplied total if asyn is True
        total = randint(12, 30)

    for _ in range(total):
        # limited to octaves 4 and 5 for violins
        if part.instrument == "Violin":
            note = scale[randint(13, len(scale) - 1)]
            # trying to account for random notes chosen out of range...
            while note not in RANGE["Violin"]:
                note = scale[randint(13, len(scale) - 1)]
            part.notes.append(note)

        # limit to octaves 3 and 4 for viola
        elif part.instrument == "Viola":
            note = scale[randint(7, len(scale) - 8)]
            while note not in RANGE["Viola"]:
                note = scale[randint(7, len(scale) - 8)]
            part.notes.append(note)

        # limit to octaves 2 and 3 for cello
        elif part.instrument == "Cello":
            note = scale[randint(0, len(scale) - 16)]
            while note not in RANGE["Cello"]:
                note = scale[randint(0, len(scale) - 16)]
            part.notes.append(note)

    if asyn:
        # add independent rhythms and dynamics of n length
        part.rhythms.extend(create.new_rhythms(total=len(part.notes), tempo=part.tempo))
        part.dynamics.extend(create.new_dynamics(total=len(part.notes)))

    return part


def build_ending(part: Melody) -> tuple[Melody, dict]:
    """
    builds a closing figure based off the last 3-7 notes and slowly
    shortens the rhythms until they're 16th's, while increasing the
    volume of each note.

    NOTE: dynamics don't seem to be changing. gotta fix that...

    returns a modified Melody() object
    """
    # get last 3-7 notes of melody
    n = randint(3, 7)

    # build initial figure
    fig = {
        "notes": part.notes[-n:],
        "rhythms": scale_to_tempo(part.tempo, [2.0] * n),
        "dynamics": [100] * n,
    }

    # add initial figure 2 times
    for add in range(2):
        part.notes.extend(fig["notes"])
        part.rhythms.extend(fig["rhythms"])
        part.dynamics.extend(fig["dynamics"])

    # change each rhythm list to next quickest value,
    # and increase number of reps by 1 with each change.
    # volume increases with each iteration.
    cur = 2
    rep = 2
    dyn = 9
    while cur < 9:
        fig["rhythms"] = scale_to_tempo(part.tempo, [RHYTHMS[cur]] * n)
        fig["dynamics"] = [DYNAMICS[dyn]] * n
        for i in range(rep):
            part.notes.extend(fig["notes"])
            part.rhythms.extend(fig["rhythms"])
            part.dynamics.extend(fig["dynamics"])
        cur += 1
        rep += 1
        dyn += 1

    return part, fig


def sync(melody, longest_part, fig):
    """
    repeat closing figure n times to sync up
    with the longest part in the ensemble
    """
    while melody.duration() < longest_part:
        melody.notes.extend(fig["notes"])
        melody.rhythms.extend(fig["rhythms"])
        melody.dynamics.extend(fig["dynamics"])

    return melody


if __name__ == "__main__":
    str_qtet()
