'''
this module handles another string quartet. this one is a simple choral
each part will have the same rhythm and dynamics. notes are separate and
independent'''

# Imports
from random import randint
from datetime import datetime as date

from utils.midi import save
from utils.save import saveInfo

from core.generate import Generate
from core.constants import RHYTHMS, TEMPOS

from containers.melody import Melody
from containers.composition import Composition

def strqtet2(tempo=None):
    '''
    creates a choral for string quartet using a randomly chosen mode'''

    ##############
    # INITIALIZE #
    ##############

    # objects
    create = Generate()
    comp = Composition()

    # title 'n stuff
    comp.title = create.newTitle()
    comp.composer = create.newComposer()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
    title_full = comp.title + "for string quartet"
    if tempo==None:
        # using slow tempos (40-58)
        comp.tempo = TEMPOS[randint(0,8)]
    elif tempo > 40.0 or tempo < 208.0:
        comp.tempo = tempo
    else:
        comp.tempo = 60.0

    # initialize instrument objects and append to 
    # instrument list
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


    #####################
    # CHORAL GENERATION #
    #####################

    print("\nwriting choral...")

    # pick notes. use only one scale! 
    mode, pcs, notes = create.pickMode(transpose=True)
    source = create.newSourceScale(notes)
    print("...using", notes[0], mode)
    print("...pcs:", pcs)

    # write individual lines
    total = randint(12, 30)
    # save original lines to use later
    v1 = writeline(v1, source, total)
    v2 = writeline(v2, source, total)
    va = writeline(va, source, total)
    vc = writeline(vc, source, total)
    v1_orig = v1
    v2_orig = v2
    va_orig = va
    vc_orig = vc

    # create rhythms
    rhy = []
    for rhythm in range(total):
        # use slower rhythms
        rhy.append(RHYTHMS[randint(0,4)])
    # create dynamics
    dyn = create.newDynamics(total=total)

    # add to each part AND THE ORIGINAL SET
    v1.rhythms.extend(rhy)
    v1.dynamics.extend(dyn)
    v1_orig.rhythms.extend(rhy)
    v1_orig.dynamics.extend(dyn)

    v2.rhythms.extend(rhy)
    v2.dynamics.extend(dyn)
    v2_orig.rhythms.extend(rhy)
    v2_orig.dynamics.extend(dyn)

    va.rhythms.extend(rhy)
    va.dynamics.extend(dyn)
    va_orig.rhythms.extend(rhy)
    va_orig.dynamics.extend(dyn)

    vc.rhythms.extend(rhy)
    vc.dynamics.extend(dyn)
    vc_orig.rhythms.extend(rhy)
    vc_orig.dynamics.extend(dyn)


    #############################
    # ASYNCHRONOUS COUNTERPOINT #
    #############################

    print("\nwriting asynchronous lines...")

    v1 = writeasync(v1, comp.tempo, source, create)
    v2 = writeasync(v2, comp.tempo, source, create)
    va = writeasync(va, comp.tempo, source, create)
    vc = writeasync(vc, comp.tempo, source, create)


    # ###############################
    # # ORIGINAL CHORAL - DISPLACED #
    # ###############################

    # print("\nrecapitulating choral at displaced end points...")

    # v1.notes.extend(v1_orig.notes)
    # v1.rhythms.extend(v1_orig.rhythms)
    # v1.dynamics.extend(v1_orig.dynamics)

    # v2.notes.extend(v2_orig.notes)
    # v2.rhythms.extend(v2_orig.rhythms)
    # v2.dynamics.extend(v2_orig.dynamics)

    # va.notes.extend(va_orig.notes)
    # va.rhythms.extend(va_orig.rhythms)
    # va.dynamics.extend(va_orig.dynamics)

    # vc.notes.extend(vc_orig.notes)
    # vc.rhythms.extend(vc_orig.rhythms)
    # vc.dynamics.extend(vc_orig.dynamics)


    ###############################
    # WRITE OUT & DISPLAY RESULTS #
    ###############################

    # save all parts
    comp.melodies.append(v1)
    comp.melodies.append(v2)
    comp.melodies.append(va)
    comp.melodies.append(vc)

    # generate MIDI & .txt file names
    print("\ngenerating file names...")
    comp.midiFileName = "{}{}".format(comp.title, ".mid")
    print("...midi file:", comp.midiFileName)
    # comp.txtFileName = "{}{}".format(comp.title, '.txt')
    # print("...text file:", comp.txtFileName)
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


def writeline(m, scale, total):
    '''
    writes each individual line for each part. 
    **doesn't add rhythm or dynamics** 
    only picks notes from a given source scale
    
    returns a modified melody() object'''

    for j in range(total):
        # limited to octaves 4 and 5 for violins
        if m.instrument == 'Violin':
            m.notes.append(scale[randint(13, len(scale)-1)])
        # limit to octaves 3 and 4 for viola
        elif m.instrument == 'Viola':
            m.notes.append(scale[randint(7, len(scale)-8)])
        # limit to octaves 2 and 3 for cello
        elif m.instrument == 'Cello':
            m.notes.append(scale[randint(0, len(scale)-16)])

    return m


def writeasync(m, tempo, scale, create):
    '''
    writes each individual part for the asynchronous, free
    counterpoint section
    
    returns a modified melody() object
    
    NOTE: does the .extend() method cause a note formatting 
    error when it's inputting one note at a time?'''

    total = randint(12, 30)
    for j in range(total):
        # limited to octaves 4 and 5 for violins
        if m.instrument == 'Violin':
            m.notes.append(scale[randint(13, len(scale)-1)])
            # m.notes.extend(scale[randint(13, len(scale)-1)])
        # limit to octaves 3 and 4 for viola
        elif m.instrument == 'Viola':
            m.notes.append(scale[randint(7, len(scale)-8)])
            # m.notes.extend(scale[randint(7, len(scale)-8)])
        # limit to octaves 2 and 3 for cello
        elif m.instrument == 'Cello':
            m.notes.append(scale[randint(0, len(scale)-16)])
            # m.notes.extend(scale[randint(0, len(scale)-16)])

    # add rhythms and dynamics, plus save source scale
    m.rhythms.extend(create.newRhythms(total=len(m.notes), tempo=tempo))
    m.dynamics.extend(create.newDynamics(total=len(m.notes)))

    return m