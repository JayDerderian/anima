'''
this module handles another string quartet. this one is a simple choral
each part will have the same rhythm and dynamics. After this a free counter-
point section ensues, then each part has a repeated 3-7 note figure that
gets faster and faster, and louder and louder before ending. 

NOTE: add looped arpeggios to each part based off the first four notes of 
their part from the opening choral. 

NOTE: generate a "rhythm" that is the difference between a current
part and the longest part in the piece. append this difference to the
*end* of a rhythm list, then attempt to add original choral at end of an 
asynchronous section that will have each part in rhythmic unison again. 

THIS WILL MAKE RHTYHMS LONGER THAN THE OTHER TWO LISTS. 

need to figure out how to make a rest... will a 'None' value in
lieu of a note string?
'''
    
from tqdm import trange
from random import randint, seed

from utils.midi import save
from utils.tools import scaletotempo
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, RHYTHMS, TEMPOS

from containers.melody import Melody


def strqtet(tempo=None):
    '''
    creates a choral for string quartet using a randomly chosen mode
    '''

    # initialize
    seed()
    create = Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(20,27)]) # 100-126bpm
    else:
        comp = create.init_comp(tempo)
    title_full = comp.title + " for string quartet"

    # create our quartet
    qtet = [Melody(tempo=comp.tempo,
                   instrument='Violin'),
            Melody(tempo=comp.tempo,
                   instrument='Violin'),
            Melody(tempo=comp.tempo,
                   instrument='Viola'),
            Melody(tempo=comp.tempo,
                   instrument='Cello')]
    qtet_len = len(qtet)

    # add instruments to comp object
    for inst in range(qtet_len):
        comp.instruments.append(qtet[inst])
    comp.ensemble = 'quartet'

    print("\nwriting new string quartet...")

    # pick initial notes. 
    mode, pcs, notes = create.pick_scale(t=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    # save source info to each Melody() object
    for q in range(qtet_len):
        qtet[q].pcs.append(pcs)
        qtet[q].source_scale = source

    print("\nwriting opening...")

    # write individual *choral* lines
    total = randint(12, 30)
    for q in range(qtet_len):
        qtet[q] = writeline(qtet[q], source, total, create)

    # create rhythms
    rhy = []
    for rhythm in range(total):
        # use slower rhythms
        rhy.append(RHYTHMS[randint(1,4)])
    # create dynamics
    dyn = create.new_dynamics(total=total)

    # add rhy & dyn to each part 
    for q in range(qtet_len):
        qtet[q].rhythms.extend(rhy)
        qtet[q].dynamics.extend(dyn)

    # save original values in temp list
    qtet_orig = qtet

    print("\nwriting asynchronous lines...")

    mode, pcs, notes = create.pick_scale(t=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs, "\n")

    for q in trange((qtet_len), desc= "progress"):
        qtet[q] = writeline(qtet[q], source, total, create, asyn=True)
        qtet[q].source_scale.extend(source)
        qtet[q].pcs.append(pcs)

    print("\nrecapitulating choral opening at displaced end points...")

    for q in trange((qtet_len), desc= "progress"):
        qtet[q].notes.extend(qtet_orig[q].notes)
        qtet[q].rhythms.extend(qtet_orig[q].rhythms)
        qtet[q].dynamics.extend(qtet_orig[q].dynamics)

    print("\ngenerating ending figure and repeating until closure...")

    figs = []
    for q in trange((qtet_len), desc="progress"):
        qtet[q], f = buildending(qtet[q])
        figs.append(f)

    durations = []
    for q in range(qtet_len):
        durations.append(qtet[q].duration())
    lp = max(durations)

    print("\nsyncing...")

    for q in trange((qtet_len), desc="progress"):
        if qtet[q].duration() < lp:
            qtet[q] = sync(qtet[q], lp, figs[q])

    # save all parts then write out
    for q in range(qtet_len):
        comp.melodies.append(qtet[q])
    save(comp)

    print("\n...success!")

    # display results
    comp.display()

    return comp


#--------------------------------------------------------------------------#


def writeline(m, scale, total, create, asyn=False):
    '''
    writes each individual melodic line for each part. 
    **doesn't add rhythm or dynamics** if asyn==False,
    which it is by default. if asyn==true, then any supplied
    total will be overwritten! still working on that
    quirk...
    
    returns a modified Melody() object
    '''
    if asyn:
        # NOTE: this will redefine supplied total if asyn is True
        total = randint(12, 30)
    for things in range(total):
        # limited to octaves 4 and 5 for violins
        if m.instrument == 'Violin':
            note = scale[randint(13, len(scale)-1)]
            # trying to account for random notes chosen out of range...
            while note not in RANGE["Violin"]:
                note = scale[randint(13, len(scale)-1)]
            m.notes.append(note)
        # limit to octaves 3 and 4 for viola
        elif m.instrument == 'Viola':
            note = scale[randint(7, len(scale)-8)]
            while note not in RANGE["Viola"]:
                note = scale[randint(7, len(scale)-8)]
            m.notes.append(note)
        # limit to octaves 2 and 3 for cello
        elif m.instrument == 'Cello':
            note = scale[randint(0, len(scale)-16)]
            while note not in RANGE["Cello"]:
                note = scale[randint(0, len(scale)-16)]
            m.notes.append(note)
    
    if asyn:
        # add independent rhythms and dynamics of n length
        m.rhythms.extend(create.new_rhythms(total=len(m.notes), tempo=m.tempo))
        m.dynamics.extend(create.new_dynamics(total=len(m.notes)))

    return m


def buildending(m):
    '''
    builds a closing figure based off the last 3-7 notes and slowly 
    shortens the rhythms until they're 16th's, while increasing the 
    volume of each note.

    NOTE: dynamics don't seem to be changing. gotta fix that...
    
    returns a modified Melody() object
    '''
    # get last 3-7 notes of melody
    n = randint(3,7)

    # build initial figure
    fig = {"notes": [], "rhythms": [], "dynamics": []}
    fig["notes"] = m.notes[-n:]                        # last n notes
    fig["rhythms"] = scaletotempo(m.tempo, [2.0] * n)  # start using half-notes
    fig["dynamics"] = [100] * n                        # medium dynamic

    # add initial figure 2 times
    for add in range(2):
        m.notes.extend(fig["notes"])
        m.rhythms.extend(fig["rhythms"])
        m.dynamics.extend(fig["dynamics"])
    # change each rhythm list to next quickest value, 
    # and increase number of reps by 1 with each change.
    # volume increases with each iteration.
    cur = 2
    rep = 2
    dyn = 9 
    while cur < 9:
        fig["rhythms"] = scaletotempo(m.tempo, [RHYTHMS[cur]] * n)
        fig["dynamics"] = [DYNAMICS[dyn]] * n
        for i in range(rep):
            m.notes.extend(fig["notes"])
            m.rhythms.extend(fig["rhythms"])
            m.dynamics.extend(fig["dynamics"])
        cur+=1
        rep+=1
        dyn+=1
    return m, fig


def sync(m, lp, fig):
    '''
    repeat closing figure n times to sync up
    with the longest part in the ensemble
    '''
    while m.duration() < lp:
        m.notes.extend(fig["notes"])
        m.rhythms.extend(fig["rhythms"])
        m.dynamics.extend(fig["dynamics"])
    return m