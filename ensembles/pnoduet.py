'''
Attempt to auto-generate a quasi-minimalist piano/marimna duet.

Use higher levels of repetition and use the methods within Generate() to accomplish this, 
rather than higher order/top-level methods

Try to use additive rhythms in the vibes, chords in the piano, and arpeggios in both as excersizes. 
'''

# Imports
import math
from random import randint, choice
from datetime import datetime as date

from utils.midi import save
from utils.txtfile import save_info
from utils.tools import scaletotempo
from core.constants import TEMPOS, RHYTHMS, DYNAMICS

from core.generate import Generate
from containers.chord import Chord
from containers.melody import Melody

from containers.composition import Composition


def pnoduet(instrument=None, tempo=None):
    '''
    generates a duet for user designated instrument, plus piano. 
    defaults to vibraphone if no instrument is inputted. 
    
    composition follows the following proceses:

    instrument: short/med ostinato (5-9 notes), only 16th, dotted 16th,
                or 8th notes undergoing an additive rhythmic process. 
                add 1 to 2 notes per additive iteration with either a 
                dotted quarter or half-note value until ostinato reaches 
                a specific lenghth (longer than chord prog, in seconds). 
                once it's this length, the whole figure just gets looped 
                without adding more notes until chords process completes.

    piano: 7-11 chords using only quarter notes, dotted quarters, and half 
           notes, with a non-repetitive rhythmic pattern. gradually 
           *subtract* rhythms (by 1 index value in RHYTHMS) from the pattern 
           as well as remove one chord from the end of the list, until there 
           are 2 chords left, using only alternating 16th abd dotted 16th notes.
    
    end with 4-9 long chords played by both instruments in rhythmic unison
    '''

    ##############
    # INITIALIZE #
    ##############

    print("\n\nwriting new [instr]/pno duet...")

    # objects
    create = Generate()    
    comp = Composition()

    # title 'n stuff
    comp.title = create.new_title()
    comp.composer = create.new_composer()
    comp.date = date.now().strftime("%d-%b-%y %H:%M:%S")
    if tempo==None:
        # using tempos between 60-88 for now
        comp.tempo = TEMPOS[randint(10, 18)]
    else:
        comp.tempo = tempo
    print("\ntempo:", comp.tempo)

    # instruments
    pno = [] # array of chord objects. 
             # assign this to comp.chords once ready
    if instrument == None:
        m = Melody(instrument='Vibraphone', 
                   tempo=comp.tempo)
    else:
        m = Melody(instrument=instrument, 
                   tempo=comp.tempo)
    comp.instruments.append(m.instrument)
    comp.instruments.append("Acoustic Grand Piano")
    
    # full title
    title_full = "{}{}{}".format(
        comp.title, ", for piano and ", m.instrument)


    ###############################
    # MELODY AND CHORD GENERATION #  
    ###############################

    # pick initial starting key/mode
    print("\npicking source notes...")
    notes = create.pick_scale(t=True)
    # append octaves 2 - 5 to have a starting source scale. 
    """if things progress well then i'll attempt to transpose figures 
    mid additive/subtractive process to give harmonic variety,
    and possibly follow a larger harmonic plan."""
    scale = create.new_source_scale(notes[2])

    # compose initial [instr] melody
    '''
    NOTE: om undergoes each modification of the intitial melody
          then gets appended to m, which is eventually added to comp
          once its time to write everything out.'''
    om = Melody(instrument=m.instrument, 
                tempo=comp.tempo)
    total = randint(5, 9)
    print("\nwriting", total, "note melody...")
    for i in range(total):
        # stay within octaves 3-5
        om.notes.append(scale[randint(7, len(scale)-1)])
        # starting with only 16th, dotted 16th, 8th, dotted 8th
        om.rhythms.append(RHYTHMS[randint(5, 8)])
        # starting with medium dynamics
        om.dynamics.append(DYNAMICS[randint(9, 17)])

    # compose initial piano chords
    chords = [] 
    cor = [] # chord original rhythms
    total = randint(7, 11)
    print("\nwriting", total, "chords...")
    for i in range(total):
        # 2 to 9 note chords!
        chord = create.new_chord(tempo=comp.tempo, scale=scale)
        chord.instrument = 'Acoustic Grand Piano'
        # re-select a rhythm within desired range...
        # (half, dotted qtr, qtr)
        chord.rhythm = RHYTHMS[randint(2, 4)]
        # store original rhythm floats to match against base constant
        # and find next lowest value. once new list of next-lowest values
        # is generated it'll be converted against global tempo then the new
        # chords will be appended to pno[]. 
        cor.append(chord.rhythm)
        # update dynamics if necessary (are any velocies
        # greater than 84 in this list? don't want it too loud...)
        if chord.dynamic > 84:
            chord.dynamic = DYNAMICS[randint(5, 15)]
        # save chords to chords list to modify, and pno with each
        # subsequent modification
        chords.append(chord)
        pno.append(chord)


    # repeat melody n times against chord progression duration. 
    # melody will need to repeat n times to get its total duration at least 
    # close to the the same as the chords so that there isnt an excessive 
    # amount of melody repetition as the additive process unfolds. eventually
    # the chords will start repeating as their duration is surpassed by the 
    # melody's. 
    reps = math.ceil(create.chord_durations(pno)/om.duration())
    '''NOTE: might need to hand-tune this a bit...'''
    if reps == 1 and (om.duration() * 2) < create.chord_durations(pno):
        reps += 2
    print("\nrepeating melody", reps, "time(s) to line up with pno better...")
    for i in range(reps):
        m.notes.extend(om.notes)
        m.rhythms.extend(om.rhythms)
        m.dynamics.extend(om.dynamics)

    #********insert single high f note to signal end of each riff cycle************
    m.notes.append('F5')
    m.dynamics.append(110)
    # m.rhythms.append(create.tempoConvert(comp.tempo, 2.0))
    m.rhythms.append(2.0)
    print("...added end-of-cycle note!")

    #********insert single f chord in piano to signal end of each chord cycle**********
    fend = Chord(instrument='Acoustic Grand Piano', 
                 tempo=comp.tempo)
    # make it a half note
    fend.rhythm = 2.0
    fend.notes = ['F2', 'C3', 'F3', 'A3', 'C4', 'F4']
    fend.dynamic = 110
    # add to original chord list. THIS IS THE FINAL ORIGINAL VERSION
    cor.append(fend.rhythm)
    chords.append(fend)
    pno.append(fend)
    print("...added end-of-cycle chord!")


    ###############################
    # ADDITIVE/SUBRACTIVE PROCESS #
    ###############################
    '''
    NOTE: if the below cycle starts working, then this whole block could 
          appear in one large loop to avoid more code.
    '''
    # print("\n\n***starting additive/subractive process!***")
    # # while len(pno) > 2:

    # # add 2 to 3 notes to vibes melody 
    # total = randint(2, 3)
    # print("\nadding", total, "notes to melody...")
    # for i in range(total):
    #     om.notes.append(scale[randint(0, len(scale)-1)])
    #     om.rhythms.append(c.RHYTHMS[randint(5, 8)])
    #     om.dynamics.append(c.DYNAMICS[randint(9, 17)])

    # # chord durations to next level down (i.e. half to dotted qtr, etc)
    #     # determine which rhythm it is (match against c.RHYTHMS), then
    #     # replace with c.RHYTHMS[i+1] for whatever rhythm it was.
    # print("\naltering rhythms...")
    # print("...original rhythms:", cor)
    # for i in range(len(cor)):
    #     if cor[i] in RHYTHMS:
    #         cor[i] = RHYTHMS[RHYTHMS.index(cor[i])+1]
    # print("...updated rhythms:", cor)

    # # update chord list rhythms (and scale to tempo)
    # for i in range(len(pno)):
    #     pno[i].rhythm = cor[i]
    
    # # remove a randomly chosen chord
    # print("\nremoving a randomly chosen chord...")
    # remove = randint(0, len(pno)-1)
    # pno.pop(remove)
    # print("...removed chord", remove, "!")

    # # repeat melody n times contingent on total number of chords. melody
    # # will need to repeat n times to get duration at least the same as the chords
    # # so as to help the two parts line up better. won't be exact. 
    
    # # at some point the melody will be longer than the chords, so the chords 
    # # will need to start repeating once they're less than half the duration 
    # # of the melody. chords should only get repetition consideration once 
    # # melody exceeds chord length, since chords are getting shorter and shorter.

    # md = om.duration()
    # cd = create.chord_durations(pno)
    # mlonger = False
    # if cd > md:
    #     diff = cd - md
    # else:
    #     diff = md - cd
    #     mlonger = True
    # '''
    # NOTE: this might not trigger every time once
    #       cd < (0.5 * md), since the first couple calls might
    #       make cd longer again. must always compare current state
    #       of om and pno, not total length in comp.melodies and 
    #       comp.chords!'''
    # if mlonger == True and cd < (0.5 * md):
    #     reps = math.ceil(diff/cd)
    # else:
    #     reps = math.ceil(diff/md)

    # # repeat chords if the melody is longer, otherwise
    # # repeat chords
    # if mlonger == True:
    #     for i in range(reps):
    #         comp.chords[1].extend(pno)
    # else:
    #     for i in range(reps):
    #         m.notes.extend(om.notes)
    #         m.rhythms.extend(om.rhythms)
    #         m.dynamics.extend(om.dynamics)


    # #********insert single high f note to signal end of each riff cycle************
    # m.notes.append('F5')
    # m.dynamics.append(110)
    # m.rhythms.append(2.0)

    # #********insert single fmaj chord in piano to signal end of each chord cycle**********
    # fend = Chord(instrument='Acoustic Grand Piano', tempo=comp.tempo)
    # # make it a half note
    # fend.rhythm = 2.0
    # fend.notes = ['F2', 'C3', 'F3', 'A3', 'C4', 'F4']
    # fend.dynamic=110
    # # add to original chord list + cor list. THIS IS THE FINAL ORIGINAL VERSION
    # cor.append(2.0)
    # pno.append(fend)

    ##########################
    # SCALE RHYTHMS TO TEMPO #
    ##########################

    print("\nscaling rhythms to tempo...")
    if comp.tempo != 60:
        # om.rhythms = create.scaletotempo(comp.tempo, om.rhythms)
        m.rhythms = scaletotempo(comp.tempo, m.rhythms)
        for i in range(len(pno)):
            pno[i].rhythm = scaletotempo(comp.tempo, pno[i].rhythm)


    #################################
    # save final info and write out #
    #################################

    comp.melodies.append(m)
    comp.chords[0] = pno
    comp.midi_file_name = comp.title + '.mid'
    # export MIDI file
    save(comp)
    # export .txt file
    # comp.txtFileName = comp.title + '.txt'
    # saveInfo(name=comp.title, fileName=comp.txtFileName, newMusic=comp)


    # display results
    print("\nnew duet:", title_full)
    print("composer:", comp.composer)
    print("date:", comp.date)
    dur = comp.duration()
    if dur > 60.0:
        dur/=60.0
        print("duration:", dur, "minutes")
    else:
        print("duration:", dur, "seconds")
    print("midi file:", comp.midi_file_name)
    return "\nhooray!"