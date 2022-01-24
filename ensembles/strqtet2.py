'''
this module handles the generation of a string quartet who is using fast, 
repetitive strings of rhythms (i.e. 16th notes) with either repeated or
non-repeated notes.

should be more like a scherzo. tempo will be between 120-152 by default,
unless one is supplied by the user.
'''

from tqdm import trange
from random import randint, seed, choice

from utils.midi import save
from utils.tools import scaletotempo, checkrange, getpcs
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import DYNAMICS, NOTES, REST, TEMPOS, RANGE

from containers.melody import Melody

rhy = [0.125, 0.25]                                # 16th and 8th notes only!
rests_dur = [0.5, 1, 2]                            # rest durations. pair with notes that will be SILENT!
ranges = [RANGE["Violin"], RANGE["Violin"],        # list of ranges. violin is listed twice because this 
          RANGE["Viola"], RANGE["Cello"]]          # list needs to iterate with qtet[]

def strqtet2(tempo=None):
    '''
    generates a 'scherzo' type quartet
    
    quartet is in rhythmic UNISON the whole piece! alternate between bursts of notes
    and rests. 
    '''

    print("\nwriting new string quartet...")

    seed()                                           # initialize randint, comp, and Generate()
    create = Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(26,31)]) 
    else:
        comp = create.init_comp(tempo)
    title_full = comp.title + " for string quartet"
    
    qtet = [Melody(tempo=comp.tempo,                 # create our quartet
                   instrument='Violin'),
            Melody(tempo=comp.tempo,
                   instrument='Violin'),
            Melody(tempo=comp.tempo,
                   instrument='Viola'),
            Melody(tempo=comp.tempo,
                   instrument='Cello')]
    qtet_len = len(qtet)
    qtet_empty = qtet                               # used to reset qtet for each subsequent section

    for inst in range(qtet_len):                    # add instruments to comp object
        comp.instruments.append(qtet[inst])
    comp.ensemble = 'quartet'

    sections = {}                                   # dictionary of different sections from the composition. 
                                                    # can be used to mix and match material!

    print("\nwriting opening...")

    mode, pcs, notes = create.pick_scale(t=True)    # pick initial notes. 
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    for q in range(qtet_len):                       # save meta-data
        qtet[q].pcs.append(pcs)
        qtet[q].source_scale.extend(source)
    
    us_bursts = randint(5, 11)                      # total SOFT 16th UNISON BURSTS
    for b in trange((us_bursts), desc='progress'):
        total = randint(5, 11)                      # total notes in this burst
        for q in range(qtet_len):                   # write each part
            '''NOTE: maybe find a way to find a short range of notes to pick
                     from for each part. current approach might be kinda wonky'''
            qtet[q] = writeline(qtet[q], source, total, create)
        r = [0.125] * total                         # add rhy & dyn to each part
        d = [DYNAMICS[randint(9,17)]] * total
        for q in range(qtet_len):
            qtet[q].rhythms.extend(r)
            qtet[q].dynamics.extend(d)

    durs = []                                       # end of this section is current longest part
    for q in range(qtet_len):
        durs.append(qtet[q].duration())
    us_end = max(durs)

    sections["Opening Unision 16ths"] = qtet        # save section. section is the list of Melody()
                                                    # objects in their current state                                      

    print("\n...adding disjointed lines...")

    qtet_disjoint = qtet_empty                      # create a temp ensemble to encapsulate this section,
                                                    # then append to end of qtet

    mode, pcs, notes = create.pick_scale(t=True)    # pick new source notes. 
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    for q in range(qtet_len):                       # save meta-data
        qtet_disjoint[q].pcs = pcs
        qtet_disjoint[q].source_scale = source

    # each part has strings of the same note and rhythm of n length
    # happening independint of each other, all with a very soft dynamic
    dis_bursts = randint(5,11)
    for add in trange((dis_bursts), desc='progress'):
        note = choice(checkrange(source, ranges[add]))  # pick note
        r = choice(rhy)                                 # pick rhythm
        d = DYNAMICS[randint(9,17)]                     # pick dynamic
        reps = randint(4, 10)                           # how many times should this note be played?
        for thing in range(reps):
            qtet_disjoint[add].append(note)
            qtet_disjoint[add].append(r)
            qtet_disjoint[add].dynamics.append(d)
           
    for q in range(qtet_len):                           # append all new data to qtet, then use qtet_disjoint to save with sections
        qtet[q].notes.extend(qtet_disjoint[q].notes)
        qtet[q].rhythms.extend(qtet_disjoint[q].rhythms)
        qtet[q].dynamics.extend(qtet_disjoint[q].dynamics)
        qtet[q].pcs.extend(qtet_disjoint[q].pcs)
        qtet[q].source_scale(qtet_disjoint[q].source_scale)
        
    durs = []                                           # end of this section is current longest part
    for q in range(qtet_len):
        durs.append(qtet[q].duration())
    dis_end = max(durs)

    sections["Disjointed Notes"] = qtet_disjoint        # save section (list of Melody() object states) to dictionary                                     

    # eventually re-align parts to do unison rhythmic bursts of equal length,
    # but each part has their own set of notes (same lengths though!)
    
    print("\n...realigning and writing slow, quiet choral...")

    mode, pcs, notes = create.pick_scale(t=True)        # pick new source notes. 
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    qtet_choral = qtet_empty                            # new empty ensemble for this section

    # find longest part, add a half-note duration, then subtract all other 
    # durations from this to get the difference, then assign a silent note, 
    # rhythm, and dynamic to this duration value.



    # end with long, quiet chord, then one sudden loud, different chord       


    


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
        total = randint(12, 30) # NOTE: this will redefine supplied total Iif supplied)
    for things in range(total):
        if m.instrument == 'Violin':
            note = scale[randint(13, len(scale)-1)]
            while note not in RANGE["Violin"]:
                note = scale[randint(13, len(scale)-1)]
            m.notes.append(note)
        elif m.instrument == 'Viola':
            note = scale[randint(7, len(scale)-8)]
            while note not in RANGE["Viola"]:
                note = scale[randint(7, len(scale)-8)]
            m.notes.append(note)
        elif m.instrument == 'Cello':
            note = scale[randint(0, len(scale)-16)]
            while note not in RANGE["Cello"]:
                note = scale[randint(0, len(scale)-16)]
            m.notes.append(note)
    
    if asyn:
        m.rhythms.extend(create.new_rhythms(total=len(m.notes), tempo=m.tempo))
        m.dynamics.extend(create.new_dynamics(total=len(m.notes)))

    return m