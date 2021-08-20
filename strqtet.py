'''
File for auto-generating short string quartets. This is mostly to just experiment with
and won't be posted on github.
'''

# Imports
from random import randint
from utils.midi import save, saveMinimal
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
    v1_melody = Melody()
    v2_melody = Melody()
    va_melody = Melody()
    vc_melody = Melody()

    # title 'n stuff
    comp.title = create.newTitle()
    title_full = comp.title + "for string quartet"
    comp.composer = create.newComposer()
    comp.tempo = create.newTempo()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")

    # disperse tempo
    v1_melody.tempo = comp.tempo
    v2_melody.tempo = comp.tempo
    va_melody.tempo = comp.tempo
    vc_melody.tempo = comp.tempo

    # assign instruments
    v1_melody.instrument = "Violin"
    comp.instruments.append(v1_melody.instrument)
    v2_melody.instrument = "Violin"
    comp.instruments.append(v2_melody.instrument)
    va_melody.instrument = "Viola"
    comp.instruments.append(va_melody.instrument)
    vc_melody.instrument = "Cello"
    comp.instruments.append(vc_melody.instrument)

    # working with pan-diatonic music for now...
    root = c.MAJOR_SCALES[randint(1, len(c.MAJOR_SCALES) - 1)]

    # generate source scale for all string parts. repeats a scale
    # 4x to the top octave, then starts over (i.e. Bb maj in octaves 2, 3, 4, and 5). 
    # this allows me to specify range using randint. might require some manual fixing
    # in finale depending on the scale(s) selected.
    scales = {}
    # total number of scales to create
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

    # generate parts. each will have a different amount of notes, hence the multiple loops. 
    # unfortunately this method doesn't allow for repetition of notes (unless by chance). 

    # violin 1 & 2 parts
    print("\nwriting violin 1 part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 4 and 5
            v1_melody.notes.append(scale[randint(7, len(scale) - 1)])
    v1_melody.rhythms = create.newRhythms(total=len(v1_melody.notes), tempo=comp.tempo)
    v1_melody.dynamics = create.newDynamics(total=len(v1_melody.notes))
    print("\nwriting violin 2 part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 4 and 5
            v2_melody.notes.append(scale[randint(7, len(scale) - 1)])
    v2_melody.rhythms = create.newRhythms(total=len(v2_melody.notes), tempo=comp.tempo)
    v2_melody.dynamics = create.newDynamics(total=len(v2_melody.notes))

    # viola part
    print("\nwriting viola part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 3 and 4
            va_melody.notes.append(scale[randint(7, len(scale) - 8)])
    va_melody.rhythms = create.newRhythms(total=len(va_melody.notes), tempo=comp.tempo)
    va_melody.dynamics = create.newDynamics(total=len(va_melody.notes))

    # cello part
    print("\nwriting cello part...")
    for i in range(len(scales)):
        scale = scales[i]
        total = randint(25, 50)
        for j in range(total):
            # limited to octaves 2 - 3
            vc_melody.notes.append(scale[randint(0, len(scale) - 16)])
    vc_melody.rhythms = create.newRhythms(total=len(vc_melody.notes), tempo=comp.tempo)
    vc_melody.dynamics = create.newDynamics(total=len(vc_melody.notes))

    # save all parts and write out
    comp.melodies.append(v1_melody)
    comp.melodies.append(v2_melody)
    comp.melodies.append(va_melody)
    comp.melodies.append(vc_melody)

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