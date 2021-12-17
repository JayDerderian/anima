'''
this generates a composition (septet) where each part plays the same 7-13 note 
set, but each parts rhythms and dynamics are very different. 

each part should begin with a short burst of rhythms (len(rhy) <= len(notes)-2), and the last 2 notes
should always have a long rhythm (though each individual long rhythm can be different). 
this will allow each set to kind of come back in "unision" before running off again. 
the last note in particular should have an extra long rhythm.'''

# IMPORTS
from core.generate import Generate
from core.constants import TEMPOS, DYNAMICS, INSTRUMENTS, RHYTHMS

from containers.melody import Melody
from containers.composition import Composition

from utils.midi import save

from random import randint
from datetime import datetime as date


def bloom(aged=True):

    print("\n\nstarting bloom!")

    create = Generate()
    comp = Composition()
    if aged:
        comp.title = 'Aged Face'
    else:
        comp.title = create.new_title()
    title_full = "{}{}".format(comp.title, " for mixed septet")
    comp.composer = 'Rando Calrisian'
    comp.ensemble = 'mixed septet'
    comp.date = date.now().strftime("%b-%d-%y %H:%M:%S")
    comp.midi_file_name = comp.title + ".mid"
    comp.txt_file_name = comp.title + ".txt"
    # defaults to mid-range tempos
    comp.tempo = TEMPOS[randint(5,20)]

    def new_mel(t, notes=None):
        m = Melody(tempo=t)
        # only picking keyboards, metal or 
        # wood percussion, or the first three 
        # organs (indicies 0->18)
        '''NOTE: eventually expand possible instruments
                 to keyboards, wood/metal pitched percussion,
                 organs, accordians/harmonics, guitars, and basses
                 
                 indecies: 0->39'''
        m.instrument = INSTRUMENTS[randint(0,18)]
        # the notes
        '''NOTE: find a way to disperse these notes one octave
                 above and two below current note strings'''
        if aged:
            m.notes = ['A4','G4','E4','D5','F4','A4','C5','E5']
        elif aged==False and notes != None:
            m.notes = notes[0]
            m.info = notes[1]
        else:
            notes = create.new_notes(t=randint(7,13))
            m.notes = notes[0]
            m.info = notes[1]
        # add rhythmic initial burst to all the 
        # last two notes
        for r in range(len(m.notes)-2):
            m.rhythms.append(RHYTHMS[randint(6,9)])
            m.dynamics.append(DYNAMICS[randint(9,17)])
        # add long rhythms to last two notes
        for r in range(2):
            m.rhythms.append(RHYTHMS[randint(0,2)])
            m.dynamics.append(DYNAMICS[randint(9,17)])
        return m

    # generate 7 melodies/parts
    print("\nwriting initial melody...")
    melodies = []
    if aged==False:
        notes = create.new_notes(t=randint(7,13))
        for melody in range(7):
            melodies.append(new_mel(comp.tempo, notes))
    else:
        for melody in range(7):
            melodies.append(new_mel(comp.tempo))

    # save each instrument to comp
    for melody in range(len(melodies)):
        comp.instruments.append(melodies[melody].instrument)

    # # repeat each melody 4 times in each part
    # print("\nrepeating each part 4 times...")
    # for mel in range(len(melodies)):
    #     # get copy of current melody
    #     m = melodies[mel]
    #     # append all it's data 4 times to itself
    #     for add in range(4):
    #         melodies[mel].notes.extend(m.notes)
    #         melodies[mel].rhythms.extend(m.rhythms)
    #         melodies[mel].dynamics.extend(m.dynamics)

    # save all melodies to comp object,
    # then export MIDI file
    comp.melodies = melodies
    save(comp)

    # display results & return comp object
    print("\nnew septet:", title_full)
    print("instruments:", comp.instruments)
    print("\ncomposer:", comp.composer)
    print("date:", comp.date)
    print("tempo:", comp.tempo)
    duration = comp.duration()
    if duration > 60.0:
        duration /=60.0
        print("duration", duration, "minutes\n")
    else:
        print("duration:", duration, "seconds\n")
    return comp