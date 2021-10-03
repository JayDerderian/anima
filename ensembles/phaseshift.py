'''
this module contains a duet that undergoes a phase shift. a simple loop is repeated in 
unison before the second part gets a single additional rhythm introduced, making it
"out of sync" with part 1. eventually the parts re-align, hopefully'''

# Imports
from containers.melody import Melody
from random import randint, choice
from datetime import datetime as date

from utils.tools import scaletotempo
from utils.midi import save

from core.generate import Generate
from core.constants import TEMPOS, RHYTHMS, DYNAMICS

from containers.composition import Composition


def phaseshift(tempo=None):
    '''
    this method generates a duet that undergoes a phase shift process.'''

    print("\nwriting phase shift duet...")
    # initialize
    create = Generate()
    comp = Composition()
    comp.title = create.newTitle()
    comp.composer = create.newComposer()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
    title_full = comp.title + " (phase shift), for piano duet"
    if tempo==None:
        # using med tempos (60-88bpm)
        comp.tempo = TEMPOS[randint(9,17)]
    elif tempo > 40.0 or tempo < 208.0:
        comp.tempo = tempo
    else:
        comp.tempo = 60.0
    comp.ensemble = 'duet'

    # create our instruments
    m1 = Melody(tempo=comp.tempo, 
                instrument='Acoustic Grand Piano')
    m2 = Melody(tempo=comp.tempo, 
                instrument='Electric Piano 2')

    print("\nwriting melody...")
    scale = create.pickScale()
    source = create.newSourceScale(scale[2])
    total = randint(2, 10)
    print("...picking", total, "notes from", scale[2][0], scale[0])
    for stuff in range(total):
        m1.notes.append(choice(source))
        # using only dotted 8ths, 8ths, dotted 16ths, or 16ths
        m1.rhythms.append(RHYTHMS[randint(5,8)])
        # using medium dynamics
        m1.dynamics.append(DYNAMICS[randint(9,17)])
    # copy over
    m2.notes = m1.notes
    m2.rhythms = m1.rhythms
    m2.dynamics = m1.dynamics

    # repeat figure 2 times in unison (played 3 times total)
    print("\nlooping melody...")
    m1.notes.extend(m1.notes)
    m1.rhythms.extend(m1.rhythms)
    m1.dynamics.extend(m1.dynamics)
    # m2.notes.extend(m2.notes)
    # m2.rhythms.extend(m2.rhythms)
    # m2.dynamics.extend(m2.dynamics)

    # print("\noffsetting second instrument...")
    # # add a single 16th note to m2 to create the offset
    # m2.notes.append(create.newNote())
    # m2.rhythms.append(scaletotempo(tempo=comp.tempo, rhythms=0.25))
    # m2.dynamics.append(create.newDynamic())

    # print("\nlooping with offset...")
    # # repeat figure 4 times in unison
    # for repeat in range(4):
    #     m1.notes.extend(m1.notes)
    #     m1.rhythms.extend(m1.rhythms)
    #     m1.dynamics.extend(m1.dynamics)
    #     m2.notes.extend(m2.notes)
    #     m2.rhythms.extend(m2.rhythms)
    #     m2.dynamics.extend(m2.dynamics)

    # generate file name and write out
    comp.melodies.append(m1)
    comp.melodies.append(m2)
    print("\ngenerating MIDI file...")
    comp.midiFileName = comp.title + '.mid'
    print("...midi file:", comp.midiFileName)

    # save to MIDI file
    save(comp)

    # display results
    print("\n\nnew duet:", title_full)
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
