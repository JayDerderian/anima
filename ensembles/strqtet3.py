'''
this module handles another string quartet. this one is a simple choral
each part will have the same rhythm and dynamics. After this a free counter-
point section ensues, then each part has a repeated 3-7 note figure that
gets faster and faster, and louder and louder before ending. 

NOTE: add looped arpeggios to each part based off the first four notes of 
their part from the opening choral. '''

from tqdm import trange
from random import randint

from utils.midi import save
from utils.tools import scaletotempo
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, RHYTHMS, TEMPOS

from containers.melody import Melody


def strqtet3(tempo=None):
    '''
    creates a choral for string quartet using a randomly chosen mode'''

    # initialize
    create = Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(0,8)])
    else:
        comp = create.init_comp(tempo)
    title_full = comp.title + "for string quartet"

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
    for inst in range(len(qtet)):
        comp.instruments.append(qtet[inst])
    comp.ensemble = 'quartet'

    print("\nwriting choral...")

    # pick notes. use only one scale! 
    mode, pcs, notes = create.pick_scale(t=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    # save source info to each Melody() object
    for q in range(qtet_len):
        qtet[q].pcs = pcs
        qtet[q].source_data = source

    # write individual *choral* lines
    total = randint(12, 30)
    for q in range(4):
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

    # save original values in temp objects
    # v1_orig = v1
    # v2_orig = v2
    # va_orig = va
    # vc_orig = vc

    qtet_orig = qtet

    print("\nwriting asynchronous lines...")

    for q in range(qtet_len):
        qtet[q] = writeline(qtet[q], source, total, create, asyn=True)

    '''
    NOTE: generate a "rhythm" that is the difference between a current
    part and the longest part in the piece. append this difference to the
    *end* of a rhythm list, then attempt to add original choral at end of an 
    asynchronous section that will have each part in rhythmic unison again. 
    
    THIS WILL MAKE RHTYHMS LONGER THAN THE OTHER TWO LISTS. 
    
    need to figure out how to make a rest... will a 'None' value in
    lieu of a note string?'''

    print("\nrecapitulating choral at displaced end points...")

    for q in range(qtet_len):
        qtet[q].notes.extend(qtet_orig[q].notes)
        qtet[q].rhythms.extend(qtet_orig[q].rhythms)
        qtet[q].dynamics.extend(qtet_orig[q].dynamics)


    print("\ngenerating ending figure and repeating until closure...")
    
    qtet[0], v1fig = buildending(qtet[0])
    qtet[1], v2fig = buildending(qtet[1])
    qtet[2], vafig = buildending(qtet[2])
    qtet[3], vcfig = buildending(qtet[3])

    durations = []
    for q in range(qtet_len):
        durations.append(qtet[q].duration())
    lp = max(durations)

    if qtet[0].duration() < lp:
        qtet[0] = sync(qtet[0], lp, v1fig)
    if qtet[1].duration() < lp:
        qtet[1] = sync(qtet[1], lp, v2fig)
    if qtet[2].duration() < lp:
        qtet[2] = sync(qtet[2], lp, vafig)
    if qtet[3].duration() < lp:
        qtet[3] = sync(qtet[3], lp, vcfig)

    # save all parts then write out
    for q in range(qtet_len):
        comp.melodies.append(qtet[q])
    save(comp)

    # display results
    print("\nnew quartet:", title_full)
    print("composer:", comp.composer)
    print("date:", comp.date)
    print("tempo:", comp.tempo)
    print("duration:", comp.duration_str())
    return comp


#--------------------------------------------------------------------------#


def writeline(m, scale, total, create, asyn=False):
    '''
    writes each individual melodic line for each part. 
    **doesn't add rhythm or dynamics** if asyn==False,
    which it is by default. if asyn== true, then supplied
    total will be overwritten! still working on that
    quirk...
    
    returns a modified Melody() object'''

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
    builds an arpeggio based off the last 3-7 notes and slowly shortens the rhythms
    until they're 16th's, while increasing the volume of each note.
    
    returns a modified Melody() object'''

    # get last 3-7 notes of melody
    n = randint(3,7)

    # build initial figure
    fig = {"notes": [], "rhythms": [], "dynamics": []}
    fig["notes"] = m.notes[-n:]
    fig["rhythms"] = scaletotempo(m.tempo, [2.0] * n)
    fig["dynamics"] = [100] * n

    # add initial figure 2 times
    for add in range(2):
        m.notes.extend(fig["notes"])
        m.rhythms.extend(fig["rhythms"])
        m.dynamics.extend(fig["dynamics"])
    # change each rhythm list to next quickest value, 
    # and increase number of reps by 2 with each change.
    # volume increases with each iteration.
    cur = 2
    rep = 4
    dyn = 9 
    while cur < 9:
        fig["rhythms"] = scaletotempo(m.tempo, [RHYTHMS[cur]] * n)
        fig["dynamics"] = [DYNAMICS[dyn]] * n
        for i in range(rep):
            m.notes.extend(fig["notes"])
            m.rhythms.extend(fig["rhythms"])
            m.dynamics.extend(fig["dynamics"])
        cur+=1
        rep+=2
        dyn+=1
    return m, fig


def sync(m, lp, fig):
    while m.duration() < lp:
        m.notes.extend(fig["notes"])
        m.rhythms.extend(fig["rhythms"])
        m.dynamics.extend(fig["dynamics"])
    return m