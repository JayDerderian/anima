'''
File for auto-generating short string quartets. This is mostly to just experiment with
and won't be posted on github.
'''

# Imports
from random import randint
from utils.midi import save
import core.constants as c
from containers.melody import Melody
from core.generate import Generate
from containers.composition import Composition


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

    # assign instruments
    v1_melody.instrument = "Violin"
    v2_melody.instrument = "Violin"
    va_melody.instrument = "Viola"
    vc_melody.instrument = "Cello"

    # disperse tempo
    v1_melody.tempo = comp.tempo
    v2_melody.tempo = comp.tempo
    vn_melody.tempo = comp.tempo
    vc_melody.tempo = comp.tempo

    # working with pan-diatonic music for now...
    root = c.MAJOR_SCALES[randint(0, len(c.MAJOR_SCALES) - 1)]

    # generate source scale for all string parts. repeats a scale
    # 4x to the top octave, then starts over (ie Bb maj in octaves 2, 3, 4, and 5). 
    # this allows me to specify range using randint. might require some manual fixing
    # in finale depending on the scale(s) selected.
    '''NOTE: need to generate multiple source scales to add harmonic variety. maybe
                create a dictionary to randomly pick a scale from, then randomly pick a note'''
    octave = 2
    n = 0
    scale = []
    while len(scale) < 28:
        note = "{}{}".format(root[n], octave)
        scale.append(note)
        n += 1
        if n == len(root):
            octave += 1
            n = 0

    print("\nsource scale:", scale)

    # generate parts. each have a different amount of notes. unfortunately this 
    # method doesn't allow for repetition of notes (unless by chance). 
    total = randint(50, 100)
    for i in range(total):
        v1_melody.notes.append(scale[randint(7, len(scale)-1)])
    v1_melody.rhythms = create.newRhythms(total=len(v1_melody.notes), tempo=comp.tempo)
    v1_melody.dynamics = create.newDynamics(total=len(v1_melody.notes))
    create.displayMelody(v1_melody)

    total = randint(50, 100)
    for i in range(total):
        v2_melody.notes.append(scale[randint(7, len(scale)-1)])
    v2_melody.rhythms = create.newRhythms(total=len(v2_melody.notes), tempo=comp.tempo)
    v2_melody.dynamics = create.newDynamics(total=len(v2_melody.notes))
    create.displayMelody(v2_melody)

    # viola part
    total = randint(50, 100)
    for i in range(total):
        va_melody.notes.append(scale[randint(0, len(scale) - 8)])
    va_melody.rhythms = create.newRhythms(total=len(va_melody.notes), tempo=comp.tempo)
    create.displayMelody(va_melody)

    # cello part
    total = randint(50, 100)
    for i in range(total):
        vc_melody.notes.append(scale[randint(0, len(scale) - 8)])
    vc_melody.rhythms = create.newRhythms(total=len(vc_melody.notes), tempo=comp.tempo)
    vc_melody.dynamics = create.newDynamics(total=len(vc_melody.notes))
    create.displayMelody(vc_melody)

    # save all parts and write out
    comp.melodies.append(v1_melody)
    comp.melodies.append(v2_melody)
    comp.melodies.append(va_melody)
    comp.melodies.append(vc_melody)

