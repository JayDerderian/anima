'''
This module is mainly for experimenting with creating various musical gestures 
and figures automatically, i.e. an arpeggio
'''

# imports
from random import randint, choice
from datetime import datetime as date

import core.constants as c
from core.generate import Generate

from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition

from utils.midi import save, savecanon
from utils.tools import toStr, transpose, scaletotempo


def newArp():
    '''
    Generate a arpeggio.

    Start with root scale(chromatic?)->source scale, then pick triad interval list,
    and transpose such that the highest int in triad interval list (sol), doesn't exceed
    len(source scale)-1. Hopefully it's just like generating a 4 octave keyboard in ints 
    '''
    create = Generate()
    comp = Composition()
    arp = Melody()
    
    # assign instrument & tempo
    arp.instrument = "Acoustic Grand Piano"
    arp.tempo = 60.0
    # generate root position arpeggio pattern
    print("\ngenerating root position arpeggio(s)...")
    # arp.notes.extend(create.toStr(c.ARPEGGIOS["maj triad"], octave=4))
    
    # 3-10 arpeggiations in various transpositions and octaves lol
    total = randint(3, 10)
    for i in range(total):
        # get base list
        _arp_ = create.pickArp("maj triad")
        # transpose between 1-11 semi-tones
        _arp_ = transpose(_arp_, randint(1, 11), octeq=True)
        # convert pcs to note list[str] with randomly assigned octave
        _arp_ = toStr(_arp_, octave=randint(2, 5))
        arp.notes.extend(_arp_)
    
    # append med dynamic/MIDI velocity and eighth note rhythms
    print("\nadding dynamics and rhythms...")
    for i in range(len(arp.notes)):
        # using a medium dynamic
        arp.dynamics.append(72)
        # and only eighth notes
        arp.rhythms.append(0.5)
    
    # export to MIDI file
    print("\nsaving MIDI file...")
    comp.tempo = arp.tempo
    comp.instruments.append(arp.instrument)
    comp.melodies.append(arp)
    comp.midiFileName = 'cmaj.mid'
    save(comp)    


def newProg(scale=None):
    '''
    Generate a medium amount of random/atonal/modal/triadic (try each) and
    repeat each 3 - 5 times. 
    
    first where each chord has the same rhythm,
    
    then each individual chord has an unique rhythm (i.e. 3 chords that all had
    eighth notes, now chord 1 has dotted eights, chord 2 has eighths, chord 3 
    has sixteenths, etc. each chord repeats its unique rhythm for the span of its
    repetitions) 

    then each chord has a different rhythm for its number of repetitions.
    '''
    # stuff
    create = Generate()
    comp = Composition()
    comp.tempo = 55.0
    comp.title = 'yay chords'

    # generate 4 - 7 modal chords all with 8th notes
    chords = []
    total = randint(4, 7)
    if scale==None:
        mode, pcs, scale = create.pickMode(t=True, o=randint(3, 5))
    if scale==None:
        print("\ncreating", total, "chords from", scale[0], mode, "scale...")
    else:
        print("\ncreating", total, "chords from given scale...")
    for i in range(total):
        chord = create.newChord(tempo=comp.tempo, scale=scale)
        chord.fn = mode
        chord.dynamic = 72
        chord.rhythm = 0.5
        chord.instrument = 'Acoustic Grand Piano'
        chords.append(chord)
    comp.chords[0] = chords
    print("...created", len(comp.chords[0]), "chords!")
    comp.midiFileName = comp.title + '.mid'
    print("\nchords saved as", comp.midiFileName)
    save(comp)


# generate a canon at the octave, spaced apart by 2 beats.
# then try several other kinds of canons like the 2nd voice being 
# slightly slower or faster, and in various transpositions.
def newcanon():
    '''
    Create a canon at the octave, sepearated by 2 beats. 
    '''
    print("\nwriting new canon...")

    # objects
    create = Generate()
    comp = Composition()
    # tempo 'n stuff
    comp.tempo = c.TEMPOS[randint(9, 17)]
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
    comp.composer = 'generate.py'
    # instrument objects
    m = Melody(instrument='Violin',
               tempo=comp.tempo)
    m2 = Melody(instrument='Viola',
                tempo=comp.tempo)  
    # add instruments to main list  
    comp.instruments.append(m.instrument)
    comp.instruments.append(m2.instrument)

    # pick initial starting mode + create title
    mode, modepcs, notes = create.pickMode(t=True)
    print("\nyes i canon in", notes[0], mode)
    comp.title = "{}{}{}{}".format("yes i canon in ", notes[0]," ",mode)
    title_full = "{}{}{}{}{}{}{}{}".format(
        'yes i canon in ', notes[0]," ", mode, " for ", m.instrument, " and ", m2.instrument)
    print("\ntempo:", comp.tempo)

    # create initial melody
    # generate melody list w/o octaves!
    print("\nnew melody...")
    mel = []
    total = randint(7, 19)
    for i in range(total):
        # mel.append(notes[randint(0, len(notes)-1)])
        mel.append(choice(notes))
    o = [randint(4, 5) for x in range(len(mel))]
    r = create.newRhythms(total=len(mel), tempo=comp.tempo)
    print("...notes:", mel)
    print("...octaves:", o)
    print("...rhythms:", r)

    # append octave 4 to mel, then append octave 3 to canon line
    # copy initial melody and subtract original octave values in o' by 1
    for n in range(len(mel)):
        note = "{}{}".format(mel[n], o[n])
        m.notes.append(note)
        m.dynamics.append(72)
    m.rhythms.extend(r)
    # generate m2 canonic immitation and subtract each octave value by one
    for n in range(len(mel)):
        note = "{}{}".format(mel[n], o[n]-1)
        m2.notes.append(note)
        m2.dynamics.append(72)
    m2.rhythms.extend(m.rhythms)
    
    # export to MIDI file
    comp.melodies.append(m)
    comp.melodies.append(m2)
    comp.midiFileName = "{}{}".format(comp.title, ".mid")
    diff = scaletotempo(tempo=comp.tempo, rhythms=2.0)
    savecanon(comp, s=diff)
    
    # display results
    print("\nnew piece:", title_full)
    print("midi file:", comp.midiFileName)

# generate a single melody palindrome
def newpalindrome():
    '''
    generate a single melody palindrome'''

    print("\ngenerating melodic palindrom...")

    create = Generate()
    comp = Composition()

    # initialize comp
    comp.title = create.newTitle()
    comp.composer = create.newComposer()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
    comp.tempo = c.TEMPOS[randint(9, 17)]

    # initialize melody
    m = Melody(tempo=comp.tempo,
               instrument= 'Vibraphone')
    
    # generate 4 - 9 note melody
    print("\nwriting melody...")
    notes = create.pickMode(t=True, o=randint(3,5))
    total = randint(4,9)
    for i in range(total):
        m.notes.append(choice(notes[2]))
    m.rhythms = create.newRhythms(total=len(m.notes), tempo=comp.tempo)
    m.dynamics = create.newDynamics(total=len(m.notes))

    # input each list in reverse. start with getting copies of each parameter (notes, 
    # rhythms, and dynamics), then append them to m starting at the end of each list
    print("\nreversing", m.instrument, "part...")
    end = len(m.notes)-1
    while end > -1:
        m.notes.append(m.notes[end])
        m.rhythms.append(m.rhythms[end])
        m.dynamics.append(m.dynamics[end])
        end-=1
        
    # write it out
    comp.midiFileName = comp.title + '.mid'
    comp.melodies.append(m)
    save(comp)