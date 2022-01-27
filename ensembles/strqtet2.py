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

rhy = [0.5, 1]                                     # 8ths and qter notes
rests_dur = [0.5, 1]                               # rest durations. pair with notes that will be SILENT!
ranges = {'Violin' : RANGE["Violin"],              # dictionary of ranges for instruments in this ensemble 
          'Viola'  : RANGE["Viola"], 
          'Cello'  : RANGE["Cello"]}          

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
        comp = create.init_comp(TEMPOS[randint(20,29)]) 
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
        '''
        NOTE: produces a note repeated n times with an arbitrarily
        chosen rest duration. ensemble should be in rhythmic *unison*
        '''
        for q in range(qtet_len):                   # write each part
            mod_source = checkrange(source, ranges[qtet[q].instrument])   # make sure to pick notes withiin this instrument's range
            qtet[q].notes.extend([choice(mod_source)] * total)
            qtet[q].rhythms.extend([scaletotempo(comp.tempo, 0.125)] * total)  # NOTE: something is wonky with the rhythms...
            qtet[q].dynamics.extend([DYNAMICS[randint(9,17)]] * total)
            qtet[q].notes.append("C4")              # "silent" note since MIDI doesn't actually have real rests
            qtet[q].rhythms.append(scaletotempo(comp.tempo, choice(rhy)))
            qtet[q].dynamics.append(REST)

    # durs = []                                       # end of this section is current longest part
    # for q in range(qtet_len):
    #     durs.append(qtet[q].duration())
    # us_end = max(durs)
    # sections["Opening Unision 16ths"] = qtet        # save section. section is the list of Melody()
    #                                                 # objects in their current state                                      
    # print("\nadding disjointed lines...")

    # qtet_disjoint = qtet_empty                      # create a temp ensemble to encapsulate this section,
    #                                                 # then append to end of qtet

    # mode, pcs, notes = create.pick_scale(t=True)    # pick new source notes. 
    # source = create.new_source_scale(notes)
    # print("...using", notes[0], mode)
    # print("...notes:", notes)
    # print("...pcs:", pcs)

    # for q in range(qtet_len):                       # save meta-data
    #     qtet_disjoint[q].pcs = pcs
    #     qtet_disjoint[q].source_scale = source

    # each part has strings of the same note and rhythm of n length
    # happening independint of each other, all with a very soft dynamic
    # dis_bursts = randint(5,11)
    # for db in trange((dis_bursts), desc='progress'):
    #     total = randint(5,13)
    #     for q in range(qtet_len):
    #         s = checkrange(source, ranges[qtet_disjoint[q].instrument])  
    #         n = [choice(s)] * total
    #         r = [choice(rhy)] * total                                  
    #         d = [DYNAMICS[randint(9,17)]] * total
    #         rst = choice(rhy)                       # add a rest at the end of the note string
    #         n.append("C4")                          # "silent" note since MIDI doesn't actually have rests
    #         d.append(REST)
    #         r.append(rst)
    #         reps = randint(5, 13)
    #         for thing in range(reps):
    #             qtet_disjoint[q].notes.extend(n)
    #             qtet_disjoint[q].rhythms.extend(r)
    #             qtet_disjoint[q].dynamics.extend(d)
           
    # for q in range(qtet_len):                           # append all new data to qtet, then use qtet_disjoint to save with sections
    #     qtet[q].notes.extend(qtet_disjoint[q].notes)
    #     qtet[q].rhythms.extend(qtet_disjoint[q].rhythms)
    #     qtet[q].dynamics.extend(qtet_disjoint[q].dynamics)
    #     qtet[q].pcs.extend(qtet_disjoint[q].pcs)
    #     qtet[q].source_scale.extend(qtet_disjoint[q].source_scale)
        
    # durs = []                                      # end of this section is current longest part
    # for q in range(qtet_len):
    #     durs.append(qtet[q].duration())
    # dis_end = max(durs)
    # sections["Disjointed Notes"] = qtet_disjoint   # save section (list of Melody() object states) to dictionary                                     

    # eventually re-align parts to do unison rhythmic bursts of equal length,
    # but each part has their own set of notes (same lengths though!)

    # qtet_choral = qtet_empty                            # new empty ensemble for this section

    # find longest part, add a half-note duration, then subtract all other 
    # durations from this to get the difference, then assign a silent note, 
    # rhythm, and dynamic to this duration value.



    # end with long, quiet chord, then one sudden loud, different chord


    print("\n...success!")
    comp.display()

    # save and write out
    for q in range(qtet_len):
        comp.melodies.append(qtet[q])
    save(comp)       