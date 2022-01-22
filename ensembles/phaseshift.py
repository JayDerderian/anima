'''
this module contains a duet that undergoes a phase shift. a simple loop is repeated in 
unison before the second part gets a single additional rhythm introduced, making it
"out of sync" with part 1. eventually the parts re-align, hopefully'''


from tqdm import trange
from random import randint, choice, seed

from utils.tools import getpcs, scaletotempo
from utils.midi import save

from core.generate import Generate
from containers.melody import Melody

rhythms = [0.125, 0.25, 0.375]   # rhythmic vocab of 16ths, 8ths, and dotted 8ths

def phaseshift(tempo=None):
    '''
    this method generates a duet that undergoes a phase shift process.
    rather than be at two different tempos, the second part is given an extra
    note/rhythm/dynamic, and the two parts cycle against each other until
    they line up again.'''

    seed()                                                                 # seed randint() and initialize
    create = Generate()
    if tempo==None:
        comp = create.init_comp(tempo=72.0)
    else:
        comp = create.init_comp(tempo=tempo)
                                          
    duet = [Melody(tempo=comp.tempo, instrument='Acoustic Grand Piano'),   # create the duet
            Melody(tempo=comp.tempo, instrument='Electric Piano 1')]
    duet_len = len(duet)

    print("\nwriting unison duet...\n")

    notes, data, source = create.new_notes(t=randint(7,13))                # pick notes, rhythms, and dynamics, and assign to duet
    rhy = [scaletotempo(tempo=comp.tempo, rhythms=choice(rhythms)) for r in range(len(notes))]
    dyn = create.new_dynamics(total=len(notes), rests=False)
    for inst in trange((duet_len), desc='progress'):
        duet[inst].notes = notes
        duet[inst].rhythms = rhy
        duet[inst].dynamics = dyn
        duet[inst].pcs = getpcs(notes)
        duet[inst].source_data = data[0]
        duet[inst].source_scale = source

    print("\nimplementing phase shift...\n")

    # add additional note, rhythm, and dynamic to second instrument, then figure out how many times to loop
    # the two parts against each other until they line up again. extend each set of notes/rhythms/dynamics
    # to this total before finishing.
    '''
    NOTE:
        since one part will only be one note longer, then the two parts will need to iterate
        n times where n is the length of the *longer* part

        ex:
        1 = 4/4: |q q q q|q q q q|q q q q|                  repeat 3 times
        2 = 3/4: |q q q|q q q|q q q|q q q|                  repeat 4 times
    '''

    duet[1].notes.append(duet[1].notes[-1])                                # repeat the last note, rhythm and dynamic
    duet[1].rhythms.append(duet[1].rhythms[-1])
    duet[1].dynamics.append(duet[1].dynamics[-1])

    p1_len = len(duet[0].notes)                                            # repeat parts until cycle is complete
    p2_len = len(duet[1].notes)

    print("p1 len = ", p1_len)
    print("p2_len = ", p2_len)


    for add in trange((p2_len), desc='p1 progress'):
        duet[0].notes.extend(duet[0].notes)
        duet[0].rhythms.extend(duet[0].rhythms)
        duet[0].dynamics.extend(duet[0].dynamics)

    for add in trange((p1_len), desc='p2 progress'):
        duet[1].notes.extend(duet[1].notes)
        duet[1].rhythms.extend(duet[1].rhythms)
        duet[1].dynamics.extend(duet[1].dynamics)


    for i in range(duet_len):                                             # save and write out
        comp.melodies.append(duet[i])


    # save(comp)

    return comp