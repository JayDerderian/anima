"""
a short solo for a variety of different kinds of guitars (randomly chosen)

generates a piece that alternates between single line melody and chords

simple rhythms (16th, 8th notes, quarter notes, half notes), tempo 55-63
"""

from tqdm import trange
from random import seed, randint

from utils.data import new_ints
from utils.midi import save
from utils.tools import checkrange, scaletotempo, getpcs

from core.generate import Generate
from core.constants import DYNAMICS, RANGE, TEMPOS

from containers.melody import Melody

guitars = ['Acoustic Guitar (nylon)','Acoustic Guitar (steel)',
           'Electric Guitar (jazz)', 'Electric Guitar (clean)']
rhy = [0.25, 0.5, 1.0, 2.0]

def sologuitar(tempo=None):
    '''
    NOTE: i think create.new_notes() isn't quite staying within
    the range of the guitar. it'll produce 3-note lists like ()

    generates a composition for solo guitar, either acoustic
    or electric
    
    consists of a random sequence of melody and chord objects
    '''
    
    print("\nwriting solo guitar piece...")

    seed()                                                    # initialize randint()
    create = Generate()                                       # instantiate Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(7,11)])
    else:
        comp = create.init_comp(tempo)
    gtr = guitars[randint(0,3)]                               # pick a guitar
    title_full = comp.title + " for solo " + gtr              # generate title
    ran = RANGE["Guitar"]                                     # guitar note range
    piece = []                                                # temp list to append to comp.melodichords at the end 

    total = randint(2, 25)                                    # total melody and chord objects.
    for add in trange((total), desc='progress'):              # generate melody and chord objects
        if randint(0,1) == 0:                                 # melody (0) or chord (1)?
            if randint(0,1) == 0:                             # random source material (0) or no (1)?
                m = Melody(tempo=comp.tempo, instrument=gtr)
                ints = new_ints()
                notes, m.info, m.source_scale = create.new_notes(data=ints)
                m.notes = checkrange(notes, ran)
                m.rhythms = scaletotempo(tempo=comp.tempo, 
                                         rhythms=[rhy[randint(0,3)] for r in range(len(m.notes))])
                m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))]
                m.source_data = ints
                m.pcs = getpcs(m.notes)
            else:
                m = Melody(tempo=comp.tempo, instrument=gtr)
                notes, m.info, m.source_scale = create.new_notes()
                m.notes = checkrange(notes, ran)            # make sure final notes are within the guitar's range
                m.rhythms = scaletotempo(tempo=comp.tempo, 
                                         rhythms=[rhy[randint(0,3)] for r in range(len(m.notes))])
                m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))]
                m.pcs = getpcs(m.notes)
            piece.append(m)                                   # add to temp list
            if len(piece) == total:
                break
        else:
            c_total = randint(2, 5)                           # how many chords?
            for chord in range(c_total):
                if randint(0,1) == 0:                         # use random source material?
                    ints = new_ints(t=randint(2,6))
                    notes = create.new_notes(data=ints)
                    c = create.new_chord(tempo=comp.tempo, scale=checkrange(notes[0], ran))
                    c.source_data = ints
                else:
                    notes = create.new_notes(t=randint(2,6))
                    c = create.new_chord(tempo=comp.tempo, scale=checkrange(notes[0], ran))
                    c.source_data = notes[1]
                c.source_notes = notes[2]
                c.pcs = getpcs(c.notes)
                c.instrument = gtr
                c.rhythm = scaletotempo(tempo=comp.tempo, rhythms=rhy[randint(0,3)])
                c.dynamic = DYNAMICS[randint(9,17)]
                piece.append(c)                             # add to temp list
                if len(piece) == total:   
                    break
    
    print("\n...success!")                                  # display results
    print("\ntitle:", title_full)
    print("composer:", comp.composer)
    print("date:", comp.date)
    print("midi file:", comp.midi_file_name, "\n")

    comp.melodichords = piece                        # save and export MIDI file
    save(comp)


def solo_guitar_simple(tempo=None):
        
    print("\nwriting single-line guitar piece...")

    seed()                                                                     # initialize randint()
    create = Generate()                                                        # instantiate Generate()
    if tempo==None:
        comp = create.init_comp(TEMPOS[randint(7,11)])
    else:
        comp = create.init_comp(tempo)

    gtr = guitars[randint(0,3)]                                                # pick a guitar
    title_full = comp.title + " for solo " + gtr                               # generate title
    ran = RANGE["Guitar"]                                                      # guitar note range

    m = Melody(tempo=comp.tempo, instrument=gtr)                               # create the guitar
    notes, m.info, m.source_scale = create.new_notes(t=randint(5,11))          # pick some notes
    m.notes = checkrange(notes, ran)                                           # make sure final notes are within the guitar's range
    m.rhythms = scaletotempo(tempo=comp.tempo,                                 # pick rhythms & dynamics  
                             rhythms=[rhy[randint(0,3)] for r in range(len(m.notes))])
    m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))] 
    m.pcs = getpcs(m.notes)                                                    # get pcs of              
    comp.melodies.append(m) 
    
    print("...success!")                                                       # display results and write out
    print("\ntitle:", title_full)                             
    print("composer:", comp.composer)
    print("date:", comp.date)
    print("duration:", comp.duration_str())
                                 
    save(comp)