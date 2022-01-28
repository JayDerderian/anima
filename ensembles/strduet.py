'''
this module generates a string duet. the entire piece is slow,
and is a solo violin melody played against a pizzicato bass
'''

from tqdm import trange
from random import randint, seed, choice

from utils.midi import save
from utils.tools import checkrange, scaletotempo, getpcs
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, TEMPOS

from containers.melody import Melody

vn_rhy = [0.125, 1.0, 2.0, 2.5, 3.0]
bass_rhy = [1.0, 2.0]

def strduet(tempo=None):
    '''
    writes a slow duet for violin and pizzicato contrabass.
    
    tempo = 42 - 63 bpm
    '''
    
    # initialize
    seed()
    create = Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(1,10)]) # 42 - 63 bpm
    else:
        comp = create.init_comp(tempo)
    title_full = comp.title + " for violin & bass"
    comp.ensemble = "duet"

    # create our duet
    vn = Melody(tempo=comp.tempo, instrument='Violin')
    cb = Melody(tempo=comp.tempo, instrument='Pizzicato Strings')

    print("\nwriting new violin/bass duet...")

    # pick initial notes. 
    mode, pcs, notes = create.pick_scale()
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...notes:", notes)
    print("...pcs:", pcs)

    print("\nwriting violin line...")

    # pick violin notes, then use the vn duration as a iterative 
    # limit while generating bass line notes
    total = randint(9,21)
    vn_source = checkrange(source, RANGE["Violin"])
    vnr = scaletotempo(comp.tempo, vn_rhy)
    vn.notes = [choice(vn_source) for n in range(total)]
    vn.rhythms = [choice(vnr) for r in range(total)]
    vn.dynamics = [DYNAMICS[randint(9,17)] for d in range(total)]
    vn_dur = vn.duration()

    # save meta data
    vn.pcs = getpcs(vn.notes)
    vn.source_scale = vn_source
    vn.source_data = 'None'

    print("\nwriting bass line...")
    
    # pick bass notes
    bass_source = checkrange(source, RANGE["Contrabass"])
    br = scaletotempo(comp.tempo, bass_rhy)
    while cb.duration() <= vn_dur:
        cb.notes.append(choice(bass_source))
        cb.rhythms.append(choice(br))
        cb.dynamics.append(DYNAMICS[randint(9,17)])

    # save meta data
    cb.pcs = getpcs(cb.notes)
    cb.source_scale = bass_source
    cb.source_data = 'None'

    comp.melodies.append(vn)
    comp.melodies.append(cb)

    save(comp)

    print("\n...success!")
    comp.display()
    return comp