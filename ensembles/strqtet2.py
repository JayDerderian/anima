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
       
    print("\nwriting new string quartet...")

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

    # pick notes. use only one scale! 
    mode = create.pickMode(transpose=True)
    source = create.newSourceScale(mode[2])

    # write individual lines
    total = randint(12, 20)
    v1 = writeline(v1, source, total)
    v2 = writeline(v2, source, total)
    va = writeline(va, source, total)
    vc = writeline(vc, source, total)

    # write rhythms and dynamics
    # use the same one for EACH PART.
    rhy = []
    for rhythm in range(len(total)):
        # use slower rhythms
        rhy.append(RHYTHMS[randint(0,4)])
    dyn = create.newDynamics(total=total)

    v1.rhythms.extend(rhy)
    v1.dynamics.extend(dyn)

    v2.rhythms.extend(rhy)
    v2.dynamics.extend(dyn)
    
    va.rhythms.extend(rhy)
    va.dynamics.extend(dyn)

    vc.rhythms.extend(rhy)
    vc.dynamics.extend(dyn)


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
    doesn't add rhythm or dynamics, only picks
    notes from a given source scale'''

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