"""
a short solo for a variety of different kinds of guitars (randomly chosen)

generates a piece that alternates between single line melody and chords

simple rhythms (16th, 8th notes, quarter notes, half notes), tempo 55-63
"""

from tqdm import trange
from random import seed, randint, choice, choices

from utils.data import new_ints
from utils.midi import save
from utils.tools import scaletotempo

from core.analyze import Analyze
from core.generate import Generate
from core.constants import DYNAMICS, RANGE, TEMPOS

from containers.melody import Melody

guitars = ['Acoustic Guitar (nylon)','Acoustic Guitar (steel)',
           'Electric Guitar (jazz)', 'Electric Guitar (clean)']
rhy = [0.25, 0.5, 1.0, 2.0]


def sologuitar(tempo=None):
    '''
    NOTE: Not ready yet!
    
    i think create.new_notes() isn't quite staying within
    the range of the guitar. it'll produce 3-note lists like ()

    generates a composition for solo guitar, either acoustic
    or electric
    
    consists of a random sequence of melody and chord objects
    '''
    
    print("\nwriting solo guitar piece...")

    seed()                                                    # initialize randint()
    a = Analyze()                                             # get our analysis tools
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
                m.notes = a.checkrange(notes, ran)
                m.rhythms = scaletotempo(tempo=comp.tempo, 
                                         rhythms=[choice(rhy) for r in range(len(m.notes))])
                m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))]
                m.source_data = ints
                m.pcs = a.getpcs(m.notes)
            else:
                m = Melody(tempo=comp.tempo, instrument=gtr)
                notes, m.info, m.source_scale = create.new_notes()
                m.notes = a.checkrange(notes, ran)              # make sure final notes are within the guitar's range
                m.rhythms = scaletotempo(tempo=comp.tempo, 
                                         rhythms=[choice(rhy) for r in range(len(m.notes))])
                m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))]
                m.pcs = a.getpcs(m.notes)
            piece.append(m)                                   # add to temp list
            if len(piece) == total:
                break
        else:
            c_total = randint(2, 5)                           # how many chords?
            for chord in range(c_total):
                if randint(0,1) == 0:                         # use random source material?
                    ints = new_ints(t=randint(2,6))
                    notes, data, source = create.new_notes(data=ints)
                    c = create.new_chord(tempo=comp.tempo, scale=Analyze.checkrange(notes, ran))
                    c.source_data = ints
                else:
                    notes, data, source = create.new_notes(t=randint(2,6))
                    c = create.new_chord(tempo=comp.tempo, scale=a.checkrange(notes, ran))
                    c.source_data = data
                c.source_notes = source
                c.pcs = a.getpcs(c.notes)
                c.instrument = gtr
                c.rhythm = scaletotempo(tempo=comp.tempo, rhythms=choice(rhy))
                c.dynamic = DYNAMICS[randint(9,17)]
                piece.append(c)                               # add to temp list
                if len(piece) == total:     
                    break

    comp.melodichords[0] = piece                              # save and export MIDI file
    save(comp)

    print("\n...success!")                                    # display results
    comp.display()
    return comp


def solo_guitar_simple(tempo=None):
        
    print("\nwriting single-line guitar piece...")

    seed()                                                                     # initialize randint()
    a = Analyze()                                                              
    g = Generate()                                                             # instantiate Generate()
    if tempo==None:
        comp = g.init_comp(TEMPOS[randint(7,11)])
    else:
        comp = g.init_comp(tempo)
    gtr = choice(guitars)                                                      # pick a guitar
    comp.title = comp.title + " for solo " + gtr                               # generate title
    m = Melody(tempo=comp.tempo, instrument=gtr)                               # create the guitar

    total=randint(5,21)                                                        # pick some notes
    notes_, m.info, m.source_scale = g.new_notes(t=total)
    print("\nusing:")
    for i in range(len(m.info)):
        print(m.info)
    notes = a.checkrange(notes_, RANGE["Guitar"])                              # make sure final notes are within the guitar's range
    m.notes = choices(population=notes, k=randint(3,total))
    m.rhythms = scaletotempo(tempo=comp.tempo,                                 # pick rhythms & dynamics  
                             rhythms=choices(population=rhy, k=len(m.notes)))
    m.dynamics = [DYNAMICS[randint(9,17)] for d in range(len(m.notes))] 
    m.pcs = a.getpcs(m.notes)                                                  # get pcs of new melody              
    comp.melodies.append(m)                                                    # save and write out
    save(comp)
    
    print("\n...success!")                                                       
    
    comp.display()
    return comp


# Today we go home and rest, for solo guitar
def rest():
    '''
    Today We Go Home And Rest, for solo guitar

    Form: A|B|A|C|D|C|A|B|A
    '''
    # initilize stuff
    print("\ninitializing...")
    seed()
    analyze = Analyze()
    create = Generate()
    comp = create.init_comp(tempo = 73.0,
                            title = 'Today We Go Home And Rest',
                            composer = 'Jay Derderian')
    gtr = Melody(tempo = comp.tempo, instrument = 'Electric Guitar (clean)')

    # base material + containers for each generated section
    form = ['A', 'B', 'A', 'C', 'D', 'C', 'A', 'B', 'A']
    dyn = 54
    rhy = [0.5, 1.0, 2.0]
    root = ['F3', 'G3', 'A3', 'Bb3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5']
    A = {'Name': 'A',
         'Notes': ['F3', 'F4', 'D4', 'E4', 
                   'F3', 'F4', 'D4', 'E4', 'C4',
                   'F3', 'F4', 'D4', 'E4', 
                   'F3', 'F4', 'D4', 'E4', 'Bb3', 'G4', 
                   'F3', 'F4', 'D4', 'E4', 'C4', 'G4', 'A4'], 
         'Rhythms': [1.0, 0.5, 0.5, 2.0, 
                     1.0, 0.5, 0.5, 2.0, 2.0,
                     1.0, 0.5, 0.5, 2.0,
                     1.0, 0.5, 0.5, 1.0, 1.0, 1.0,
                     1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5], 
         'Dynamics': [52] * 26
    }
    B = {'Name': 'B', 'Notes': [], 'Rhythms': [], 'Dynamics': []}
    C = {'Name': 'C', 'Notes': [], 'Rhythms': [], 'Dynamics': []}
    D = {'Name': 'D', 'Notes': [], 'Rhythms': [], 'Dynamics': []}
    sects = [A, B, C, D]

    # generate B, C, and D sections
    print("\ngenerating...")
    for s in trange((len(sects)), desc='progress'):
        if sects[s]['Name'] == 'A':
            continue
        total = randint(13, 27)
        sects[s]['Notes'] = [choice(root) for n in range(total)]
        sects[s]['Rhythms'] = [choice(rhy) for r in range(total)]
        sects[s]['Dynamics'] = [dyn] * total

    # assemble
    print("\nassembling...")
    for f in trange((len(form)), desc='progress'):
        for s in range(len(sects)):
            if form[f] == sects[s]['Name']:
                gtr.notes.extend(sects[s]['Notes'])
                gtr.rhythms.extend(scaletotempo(tempo = comp.tempo, rhythms = sects[s]['Rhythms']))
                gtr.dynamics.extend(sects[s]['Dynamics'])

    # analyze and write out
    print("\nwriting out...")
    gtr.pcs = analyze.getpcs(gtr.notes)
    gtr.source_scale = root
    gtr.source_data = 'None'
    comp.melodies.append(gtr)
    comp.midi_file_name = f'{comp.title}.mid'
    comp.instruments.extend('Electric Guitar (clean)')
    save(comp)