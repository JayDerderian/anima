'''
File for auto-generating short string quartets. This is mostly to just experiment with
and won't be posted on github.
'''

# Imports
import random
from random import randint
from utils.midi import save
from utils.save import saveInfo
import core.constants as c
from core.generate import Generate
from containers.melody import Melody
from containers.composition import Composition
from datetime import datetime as date


def newStrQtet():
    # objects
    create = Generate()
    comp = Composition()
    v1 = Melody()
    v2 = Melody()
    va = Melody()
    vc = Melody()

    # title 'n stuff
    comp.title = create.newTitle()
    title_full = comp.title + "for string quartet"
    comp.composer = create.newComposer()
    comp.tempo = create.newTempo()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")

    # disperse tempo
    v1.tempo = comp.tempo
    v2.tempo = comp.tempo
    va.tempo = comp.tempo
    vc.tempo = comp.tempo

    # assign instruments
    v1.instrument = "Violin"
    comp.instruments.append(v1.instrument)
    v2.instrument = "Violin"
    comp.instruments.append(v2.instrument)
    va.instrument = "Viola"
    comp.instruments.append(va.instrument)
    vc.instrument = "Cello"
    comp.instruments.append(vc.instrument)

    # working with pan-diatonic music for now...
    root = c.MAJOR_SCALES[randint(1, len(c.MAJOR_SCALES) - 1)]

    # generate source scale for all string parts. repeats a scale
    # 4x to the top octave, then starts over (i.e. Bb maj in octaves 2, 3, 4, and 5). 
    # this allows me to specify range using randint. might require some manual fixing
    # in finale depending on the scale(s) selected.
    scales = {}
    # total number of scales to use
    total = randint(2, 4)
    for i in range(total):
        n = 0
        scale = []
        octave = 2
        while len(scale) < 28:
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            if n == len(root):
                octave += 1
                n = 0
        scales[i] = scale
        root = c.MAJOR_SCALES[randint(1, len(c.MAJOR_SCALES) - 1)]

    # generate parts. each will have a different amount of notes, hence the multiple loops. 
    # unfortunately this method doesn't allow for immediate repetition of notes (unless by chance). 

    # violin 1 & 2 parts
    print("\nwriting violin 1 part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 4 and 5
            v1.notes.append(scale[randint(7, len(scale) - 1)])
    v1.rhythms = create.newRhythms(total=len(v1.notes), tempo=comp.tempo)
    v1.dynamics = create.newDynamics(total=len(v1.notes))
    print("\nwriting violin 2 part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 4 and 5
            v2.notes.append(scale[randint(7, len(scale) - 1)])
    v2.rhythms = create.newRhythms(total=len(v2.notes), tempo=comp.tempo)
    v2.dynamics = create.newDynamics(total=len(v2.notes))

    # viola part
    print("\nwriting viola part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 3 and 4
            va.notes.append(scale[randint(7, len(scale) - 8)])
    va.rhythms = create.newRhythms(total=len(va.notes), tempo=comp.tempo)
    va.dynamics = create.newDynamics(total=len(va.notes))

    # cello part
    print("\nwriting cello part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 2 - 3
            vc.notes.append(scale[randint(0, len(scale) - 16)])
    vc.rhythms = create.newRhythms(total=len(vc.notes), tempo=comp.tempo)
    vc.dynamics = create.newDynamics(total=len(vc.notes))

    # save all parts and write out
    comp.melodies.append(v1)
    comp.melodies.append(v2)
    comp.melodies.append(va)
    comp.melodies.append(vc)

    # generate MIDI and .txt file names
    print("\ngenerating file names...")
    comp.midiFileName = "{}{}".format(comp.title, ".mid")
    print("...MIDI file:", comp.midiFileName)
    comp.txtFileName = "{}{}".format(comp.title, '.txt')
    print("...text file:", comp.txtFileName)
    title_full = "{}{}".format(comp.title, ' for string quartet')

    # write to MIDI file and .txt file
    if save(comp) == 0:
        saveInfo(name=comp.title, fileName=comp.txtFileName, newMusic=comp)
        print("\n\nnew quartet:", title_full)
        print("\ncomposer:", comp.composer)
        print("\ndate:", comp.date)
        return comp
    else:
        print("\n\n...Unable to generate quartet!")
        return -1