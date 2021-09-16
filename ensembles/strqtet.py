'''
File for auto-generating string quartets. This is mostly to just experiment with
and won't be posted on github.

Begins with very free, non (intentionally) immitative counterpoint, which then
leads to the arpeggio activity described below:

Arpeggios MUST START ON THE LAST NOTE in their lists! Can go either up or down,
depending on the octave (octave 5 will start at the top of the arpeggio and go down, then
back up, oct 4 goes up then down

find in original source scale,  play it with a long rhythm, 
then build using every other note either downward or upward from end_note. 
once this repeating note set is established, start appending rhythms (long), 
after n repetitions (appending to v1.notes), select next fastest rhythm 
from c.RHYTHMS, going until 16th notes are being used (if tempois 60 or above), 
or 32nds (if tempo is less than 60). after n repetitions, pick a high note,
play it loud and long, then move to ending with all parts in unision.

~~~UNISION ENDING~~~

need a way to ensure all parts are the same duration so as to ensure they re-align
after having such disjointed parts. 

Start arpeggios at end of each part, each slowly speeding up, then once each are at
their maximum velocities, stop adding arpeggios to part that has the longest duration.
every other part will repeat their apex arpeggios n times until they're all the same
duration of the longest part. 

'''

# Imports
from random import randint
from utils.midi import save
from utils.save import saveInfo
import core.constants as c
from core.generate import Generate
from containers.melody import Melody
from containers.composition import Composition
from datetime import datetime as date


def strqtet(tempo=None):
   
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
        comp.tempo = create.newTempo()
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


    #############################
    # SOURE MATERIAL GENERATION #
    #############################

    # generate source scale for all string parts. 
    print("\ncreating modal source scale...")
    scales = newSource(create)


    ########################################
    # ASYNCHRONOUS NOTES/FREE COUNTERPOINT #
    ########################################
    '''
    NOTE: There's probably a way to make the 4 loops below happen in one
          big one that happens 4 times...'''

    # violin 1 & 2 parts
    print("\nwriting violin 1 part...")
    v1 = writeasync(v1, comp.tempo, scales, create)
    print("\nwriting violin 2 part...")
    v2 = writeasync(v2, comp.tempo, scales, create)
    # viola part
    print("\nwriting viola part...")
    va = writeasync(va, comp.tempo, scales, create)
    # cello part
    print("\nwriting cello part...")
    vc = writeasync(vc, comp.tempo, scales, create)


    #################################################
    # ADD SLOWLY SPEEDING UP ARPEGGIOS TO EACH PART #
    #################################################

    arpv1 = genfig(v1, scales, create)
    arpv2 = genfig(v2, scales, create)
    arpva = genfig(va, scales, create)
    arpvc = genfig(vc, scales, create)

    # figure out which of these is the longest (lp = longest part)
    durations = [v1.duration(), v2.duration(), va.duration(), vc.duration()]
    lp = max(durations)

    print("\nv1 len:", v1.duration())
    print("v2 len:", v2.duration())
    print("va len:", va.duration())
    print("vc len:", vc.duration())

    print("\nlongest part:", lp)

    if v1.duration() != lp:
        v1 = buildfig(v1, lp, arpv1, create)
        v1 = sync(v1, lp, arpv1)
    if v2.duration() != lp:
        v2 = buildfig(v2, lp, arpv2, create)
        v2 = sync(v2, lp, arpv2)
    if va.duration() != lp:
        va = buildfig(va, lp, arpva, create)
        va = sync(va, lp, arpva)
    if vc.duration() != lp:
        vc = buildfig(vc, lp, arpvc, create)
        vc = sync(vc, lp, arpvc)

    print("\nlen's after adding fig...")
    print("v1 len:", v1.duration())
    print("v2 len:", v2.duration())
    print("va len:", va.duration())
    print("vc len:", vc.duration())


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



#-----------------------------------------------------------------------------------------------#


def newSource(create):
    '''generates a dictionary of source scales
       repeats a scale 4x to the top octave, then starts over 
       (i.e. Bb maj in octaves 2, 3, 4, and 5). 
       this allows me to specify range using randint.
       might require some manual fixing in finale depending on the 
       scale(s) selected.'''

    mode, mode_pcs, notes = create.pickMode(transpose=True)
    print("\nroot:", notes[0], mode)
    scales = {}
    # total number of scales to use
    total = randint(2, 4)
    for i in range(total):
        n = 0
        scale = []
        octave = 2
        while len(scale) < 28:
            note = "{}{}".format(notes[n], octave)
            scale.append(note)
            n += 1
            if n == len(notes):
                octave += 1
                n = 0
        scales[i] = scale
        mode, mode_pcs, notes = create.pickMode(transpose=True)
        print("...new mode:", notes[0], mode)
    return scales


def writeasync(m, tempo, scales, create):
    '''
    writes each individual part for the asynchronous, free
    counterpoint section'''

    for i in range(len(scales)):
        scale = scales[i]
        '''NOTE: maybe hand-tune total a bit...'''
        total = randint(25, 50)
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
    # add rhythms and dynamics, plus save source scale
    m.rhythms = create.newRhythms(total=len(m.notes), tempo=tempo)
    m.dynamics = create.newDynamics(total=len(m.notes))
    m.sourceScale = scales

    return m


def genfig(m, scales, create):
    '''
    builds repeated figure off last note in this part 
    and its place in the source scale.
    
    returns a tuple: 
        arp notes (list[str]), 
        arp rhythms scaled to tempo (list[float]),
        arp dynamics (list[float])'''

    # find note in source scale. 
    # v1/2, if it ends w/ 5, do a downward arpeggio, if 4, then upward
    # va, if it ends in 4, do a downward apr, if 3, upward
    # vc, if it ends in 3, go down, go up if 2

    # retrieve the last note (ln) and determine
    # which octave its in

    # print("\nfinding last played note...")
    # ln = m.notes[len(m.notes)-1]
    # print("...last note:", ln)
    dn = False
    up = False
    if m.instrument == 'Violin':
        ln = m.notes[len(m.notes)-1]
        if ln.count('5')  > 0:
            dn = True
        else:
            up = True
    elif m.instrument == 'Viola':
        ln = m.notes[len(m.notes)-1]
        if ln.count('4')  > 0:
            dn = True
        else:
            up = True
    elif m.instrument == 'Cello':
        ln = m.notes[len(m.notes)-1]
        if ln.count('3')  > 0:
            dn = True
        else:
            up = True

    # build starting arp
    for i in range(len(scales)):
        # search current scale, if note isn't present,
        # try the next one. if found, build arpeggios based
        # on location in octave. 
        
        # NOTE: this doesn't guarentee the scale with the 
        # searched-for note was the same one used during the 
        # original writing method! could be entirely different 
        # harmonic context. 

        scale = scales[i]
        try:
            note = scale.index(ln)
            arp = []
            if dn==True:
                # how many notes in the arpeggio?
                t = randint(1, 3)
                # 4-note
                if t==1:
                    '''NOTE: replace hard-coded values with randint() values
                    chosen before appending'''
                    arp.append(scale[note])
                    arp.append(scale[note-3])
                    arp.append(scale[note-5])
                    arp.append(scale[note-3])
                # 5-note arp
                elif t==2:
                    arp.append(scale[note])
                    arp.append(scale[note-3])
                    arp.append(scale[note-5])
                    arp.append(scale[note-6])
                    arp.append(scale[note-4])
                # 6-note arp
                elif t==3:
                    arp.append(scale[note])
                    arp.append(scale[note-3])
                    arp.append(scale[note-5])
                    arp.append(scale[note-7])
                    arp.append(scale[note-5])
                    arp.append(scale[note-3])
                break
            elif up==True:
                t = randint(1, 3)
                # 4-note
                if t == 1:
                    arp.append(scale[note])
                    arp.append(scale[note+3])
                    arp.append(scale[note+5])
                    arp.append(scale[note+3])
                # 5-note arp
                elif t == 2:
                    arp.append(scale[note])
                    arp.append(scale[note+3])
                    arp.append(scale[note+5])
                    arp.append(scale[note+6])
                    arp.append(scale[note+4])
                # 6-note arp
                elif t == 3:
                    arp.append(scale[note])
                    arp.append(scale[note+3])
                    arp.append(scale[note+5])
                    arp.append(scale[note+7])
                    arp.append(scale[note+5])
                    arp.append(scale[note+3])
                break
        except ValueError:
            continue

    # generate starting rhythms (half-notes) and dynamics
    rhy = []
    dyn = []
    for i in range(len(arp)):
        rhy.append(create.scaletotempo(m.tempo, 2.0))
        dyn.append(52)

    return arp, rhy, dyn

def buildfig(m, lp, arp, create):
    '''
    constructs arpeggio with increasingly fast rhythms. 
    returns a modified melody() object.
    
    SCALE TO LONGEST PART (lp)
    
    get difference between current part and longest part, divide 
    difference into equal sections devoted to repetitions of a specified
    rhythm, then repeat each rhythm n times for their section
    
    NOTE: maybe add notes, rhythms, and dynamics ONE AT A TIME to
    better achieve a closer length to the longest part. might mean the
    figure will stop mid-way through. '''

    # add starting arpeggio before scaling other reps...
    for i in range(2):
        m.notes.extend(arp[0])
        m.rhythms.extend(arp[1])
        m.dynamics.extend(arp[2]) 

    # add dotted qtrs -> 16ths
    r = [1.5, 1, 0.75, 0.5, 0.375, 0.25]
    d = [60, 72, 88, 100, 108, 112]
    for k in range(6):
        rhy = []
        dyn = []
        for i in range(len(arp[0])):
            rhy.append(create.scaletotempo(m.tempo, r[k]))
            dyn.append(d[k])
        # repeat each rhy/dyn set 3x
        for i in range(3):
            m.notes.extend(arp[0])
            m.rhythms.extend(rhy)
            m.dynamics.extend(dyn)
    # add 32nds, if necessary
    if m.tempo < 52.0:
        rhy = []
        dyn = []
        for i in range(len(arp[0])):
            rhy.append(create.scaletotempo(m.tempo, 0.125))
            dyn.append(112)
        for i in range(2):
            m.notes.extend(arp[0])
            m.rhythms.extend(rhy)
            m.dynamics.extend(dyn)  
    # sync with longest part
    # while m.duration() < lp:
    #     m.notes.extend(arp[0])
    #     m.rhythms.extend(rhy)
    #     m.dynamics.extend(dyn)
    return m

def sync(m, lp, arptuple):
    '''
    sync all other parts against a given duration
    (longeset part/lp)'''
    arp = arptuple[0]
    rhy = arptuple[1]
    dyn = arptuple[2]
    while m.duration() < lp:
        for add in range(len(arp)):
            m.notes.append(arp[add])
            m.dynamics.append(dyn[add])
            m.rhythms.append(rhy[add])
            if m.duration() == lp:
                break
    return m