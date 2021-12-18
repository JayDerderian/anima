'''
this module handles another string quartet. this one is a simple choral
each part will have the same rhythm and dynamics. notes are separate and
independent'''

# Imports
from random import randint
from datetime import datetime as date

from utils.midi import save
from utils.txtfile import save_info

from core.generate import Generate
from core.constants import RHYTHMS, TEMPOS

from containers.melody import Melody
from containers.composition import Composition

def strqtet2(tempo=None):
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
    v1 = Melody(tempo=comp.tempo,
                instrument='Violin')
    v2 = Melody(tempo=comp.tempo,
                instrument='Violin')
    va = Melody(tempo=comp.tempo,
                instrument='Viola')
    vc = Melody(tempo=comp.tempo,
                instrument='Cello')
    comp.instruments.append(v1.instrument)
    comp.instruments.append(v2.instrument)
    comp.instruments.append(va.instrument)
    comp.instruments.append(vc.instrument)
    comp.ensemble = 'quartet'

    print("\nwriting choral...")

    # pick notes. use only one scale! 
    mode, pcs, notes = create.pick_scale(t=True)
    source = create.new_source_scale(notes)
    print("...using", notes[0], mode)
    print("...pcs:", pcs)

    print("\nwriting choral...")

    # write individual lines
    total = randint(12, 30)
    v1 = writeline(v1, source, total, create)
    v2 = writeline(v2, source, total, create)
    va = writeline(va, source, total, create)
    vc = writeline(vc, source, total, create)

    # create rhythms
    rhy = []
    for rhythm in range(total):
        # use slower rhythms
        rhy.append(RHYTHMS[randint(1,4)])
    # create dynamics
    dyn = create.new_dynamics(total=total)

    # add to each part 
    v1.rhythms.extend(rhy)
    v1.dynamics.extend(dyn)
    v2.rhythms.extend(rhy)
    v2.dynamics.extend(dyn)
    va.rhythms.extend(rhy)
    va.dynamics.extend(dyn)
    vc.rhythms.extend(rhy)
    vc.dynamics.extend(dyn)

    # save original values in temp objects
    v1_orig = v1
    v2_orig = v2
    va_orig = va
    vc_orig = vc

    print("\nwriting asynchronous lines...")

    v1 = writeline(v1, source, total, create, asyn=True)
    v2 = writeline(v2, source, total, create, asyn=True)
    va = writeline(va, source, total, create, asyn=True)
    vc = writeline(vc, source, total, create, asyn=True)

    '''
    NOTE: generate a "rhythm" that is the difference between a current
    part and the longest part in the piece. append this difference to the
    *end* of a rhythm list, then attempt to add original choral at end of an 
    asynchronous section that will have each part in rhythmic unison again. 
    
    THIS WILL MAKE RHTYHMS LONGER THAN THE OTHER TWO LISTS. 
    
    need to figure out how to make a rest... will a 'None' value in
    lieu of a note string?'''

    print("\nrecapitulating choral at displaced end points...")

    v1.notes.extend(v1_orig.notes)
    v1.rhythms.extend(v1_orig.rhythms)
    v1.dynamics.extend(v1_orig.dynamics)

    v2.notes.extend(v2_orig.notes)
    v2.rhythms.extend(v2_orig.rhythms)
    v2.dynamics.extend(v2_orig.dynamics)

    va.notes.extend(va_orig.notes)
    va.rhythms.extend(va_orig.rhythms)
    va.dynamics.extend(va_orig.dynamics)

    vc.notes.extend(vc_orig.notes)
    vc.rhythms.extend(vc_orig.rhythms)
    vc.dynamics.extend(vc_orig.dynamics)

    # save all parts
    comp.melodies.append(v1)
    comp.melodies.append(v2)
    comp.melodies.append(va)
    comp.melodies.append(vc)

    # generate MIDI & .txt file names
    print("\ngenerating file names...")
    comp.midi_file_name = "{}{}".format(comp.title, ".mid")
    print("...midi file:", comp.midi_file_name)
    # comp.txt_file_name = "{}{}".format(comp.title, '.txt')
    # print("...text file:", comp.txt_file_name)
    title_full = "{}{}".format(comp.title, ' for string quartet')

    # write to MIDI file & .txt file
    save(comp)
    # saveInfo(name=comp.title, fileName=comp.txtFileName, newMusic=comp)

    # display results
    print("\n\nnew quartet:", title_full)
    print("composer:", comp.composer)
    print("date:", comp.date)
    print("tempo:", comp.tempo)
    duration = comp.duration()
    if duration > 60.0:
        duration /=60.0
        print("duration", duration, "minutes\n")
    else:
        print("duration:", duration, "seconds\n")
    return comp


#--------------------------------------------------------------------------#


def writeline(m, scale, total, create, asyn=False):
    '''
    writes each individual line for each part. 
    **doesn't add rhythm or dynamics** 
    only picks notes from a given source scale
    
    returns a modified melody() object'''
    if asyn:
        # NOTE: this will redefine supplied total if asyn is True
        total = randint(12, 30)
    for things in range(total):
        # limited to octaves 4 and 5 for violins
        if m.instrument == 'Violin':
            m.notes.append(scale[randint(13, len(scale)-1)])
        # limit to octaves 3 and 4 for viola
        elif m.instrument == 'Viola':
            m.notes.append(scale[randint(7, len(scale)-8)])
        # limit to octaves 2 and 3 for cello
        elif m.instrument == 'Cello':
            m.notes.append(scale[randint(0, len(scale)-16)])
    
    if asyn==True:
        # add rhythms and dynamics, plus save source scale
        m.rhythms.extend(create.new_rhythms(total=len(m.notes), tempo=m.tempo))
        m.dynamics.extend(create.new_dynamics(total=len(m.notes)))

    return m