'''
this module composes a short, slow piece piece for organ, 
with or without a melody'''


# Imports
from random import randint
from datetime import datetime as date

from utils.midi import save
from utils.tools import scaletotempo
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, RHYTHMS, TEMPOS

from containers.melody import Melody
from containers.composition import Composition


def organ(t=None):
    '''
    generates a short piece for organ, with or without a melody
    
    set mel to True if a melody is to be used, otherwise do nothing.
    set t to a desired tempo, otherwise do nothing.
    
    exports a new midi file with name of the composition.'''
    create = Generate()
    if t == None:
        tempo = TEMPOS[randint(7,12)]
    comp = create.init_comp(tempo=tempo)
    comp.instruments.append('Reed Organ')

    # generate 2-5 chords based off 2-4 
    # randomly chosen and built scales between octaves
    # 2 - 3
    source = new_source(create, 2)
    for scale in range(len(source)):
        chords = create.new_chords(total=randint(2,5),
                                   tempo=comp.tempo, 
                                   scale=source[scale])
        for chord in range(len(chords)):
            chords[chord].instrument = 'Reed Organ'
    comp.chords = chords
    save(comp)



def new_source(create, scale_total, oct_total):
    '''generates a dictionary of source scales each limited
       to the same octave range. 

       oct_total must be between 1-5
       scale_total should ideally between 2-5
       
       each dict key is an integer starting on 0'''

    mode, mode_pcs, notes = create.pick_scale(t=True)
    print("\nroot:", notes[0], mode)
    scales = {}
    oct_total *= 7
    for i in range(scale_total):
        n = 0
        scale = []
        octave = 2
        while len(scale) < oct_total:
            note = "{}{}".format(notes[n], octave)
            scale.append(note)
            n += 1
            if n == len(notes):
                octave += 1
                n = 0
        scales[i] = scale
        mode, mode_pcs, notes = create.pick_scale(t=True)
        print("...new mode:", notes[0], mode)
    return scales