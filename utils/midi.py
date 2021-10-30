''' 
Utility functions for working with MIDI I/O


NOTE: Double check the math for how strt and end are incremented according to
the supplied durations. Either Finale is doing something weird or the compounding
values are creating highly precice floating point numbers that might make sheet music
representation very messy. 
  
'''

# Imports
import urllib.request
import pretty_midi as pm
from random import choice
from datetime import datetime


# Autogenerates a new filename
def newFileName(ensemble):
    '''
    Generates a title/file name by picking two random words
    then attaching the composition type (solo, duo, ensemble, etc..),
    followed by the date.
    '''
    try:
        # Get word list
        url = "https://www.mit.edu/~ecprice/wordlist.10000"
        # response = requests.get(url)
        response = urllib.request.urlopen(url)
        text = response.read().decode()
        words = text.splitlines()
        # Pick two random words
        name = choice(words) + \
            '_' + choice(words)
    except urllib.error.URLError:
        name = ensemble + ' - '

    # Get date and time (DD:MM:YY (HH:MM:SS)).
    date = datetime.now().strftime("%d-%b-%y (%H:%M:%S.%f)")
    # Name and date, and add file extension
    fileName = '{}{}.mid'.format(name, date)
    return fileName


# exports a MIDI file for any sized composition (1 solo melody to ensemble sized n)
def save(comp):
    '''
    General save function for compositions. *All instruments start at the same time!*
    Exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
    
    Requires a composition() object.

    NOTE: Might modify to allow for modified start times and ***RESTS***!!!
    '''
    # create PM object. PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=comp.tempo)
    
    # add melodies
    if len(comp.melodies) > 0:
        for i in range(len(comp.melodies)):
            strt = 0
            end = comp.melodies[i].rhythms[0]
            # create melody instrument
            instrument = pm.instrument_name_to_program(comp.melodies[i].instrument)
            melody = pm.Instrument(program=instrument)
            # add *this* melody's notes
            for j in range(len(comp.melodies[i].notes)):
                # translate note to MIDI note
                note = pm.note_name_to_number(comp.melodies[i].notes[j])
                anote = pm.Note(
                    velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
                # add to instrument object
                melody.notes.append(anote)
                try:
                    # increment strt/end times
                    strt += comp.melodies[i].rhythms[j]
                    end += comp.melodies[i].rhythms[j+1]
                except IndexError:
                    break
                
            # add melody to instrument list
            mid.instruments.append(melody)

    # add chords
    if len(comp.chords) > 0:
        # iterate through a dictionary of chord() object lists.
        key = 0
        for i in range(len(comp.chords)):
            # retrieve current chord object list
            chords = comp.chords[key]
            strt = 0
            end = chords[key].rhythm
            # create instrument object.
            instrument = pm.instrument_name_to_program(chords[i].instrument)
            chord = pm.Instrument(program=instrument)
            # iterate through current chord list
            for j in range(len(chords)):
                # this list of chord objects notes
                for k in range(len(chords[j].notes)):
                    # translate note to MIDI note
                    note = pm.note_name_to_number(chords[j].notes[k])
                    anote = pm.Note(
                        velocity=chords[j].dynamic, pitch=note, start=strt, end=end)
                    # add to instrument object
                    chord.notes.append(anote)
                try:
                    # increment strt/end times
                    strt += chords[j].rhythm
                    end += chords[j+1].rhythm
                except IndexError:
                    break
            # add chord progression to instrument list
            mid.instruments.append(chord)
            key+=1

    # write to MIDI file
    print("\nsaving", comp.midiFileName, "...")
    mid.write(f'./midi/{comp.midiFileName}')
    return 0


# save canon
def savecanon(comp, s):
    '''
    exports a MIDI file for a canonic piece with a specified beat displacement (s = float)
    
    requires a composition() object with a list of melodies.
    '''
    # create PM object. PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=comp.tempo)

    # add STARTING SUBJECT
    strt = 0
    end = comp.melodies[0].rhythms[0]
    # create melody instrument
    instrument = pm.instrument_name_to_program(comp.melodies[0].instrument)
    melody = pm.Instrument(program=instrument)
    # add *this* melody's notes
    for j in range(len(comp.melodies[0].notes)):
        # translate note to MIDI note
        note = pm.note_name_to_number(comp.melodies[0].notes[j])
        # NOTE: create a method to indicate whether the inputted melodic value is a 
        # note or a rest. it could determine how to create corresponding MIDI note on/off
        # events?
        anote = pm.Note(
            velocity=comp.melodies[0].dynamics[j], pitch=note, start=strt, end=end)
        # add to instrument object
        melody.notes.append(anote)
        try:
            # increment strt/end times
            strt += comp.melodies[0].rhythms[j]
            end += comp.melodies[0].rhythms[j+1]
        except IndexError:
            break
    mid.instruments.append(melody)

    # add canonic lines according to displacement s
    for i in range(len(comp.melodies)):
        strt = s
        # start AFTER first melody!
        try:
            end = comp.melodies[i+1].rhythms[0]
        except IndexError:
            break
        # create melody instrument
        instrument = pm.instrument_name_to_program(comp.melodies[i+1].instrument)
        melody = pm.Instrument(program=instrument)
        # add *this* melody's notes
        for j in range(len(comp.melodies[i].notes)):
            # translate note to MIDI note
            note = pm.note_name_to_number(comp.melodies[i].notes[j])
            anote = pm.Note(
                velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
            # add to instrument object
            melody.notes.append(anote)
            try:
                # increment strt/end times
                strt += comp.melodies[i].rhythms[j]
                end += comp.melodies[i].rhythms[j+1]
            except IndexError:
                break
            
        # add melody to instrument list
        mid.instruments.append(melody)
        # increment by specified amount if there's more than 2 parts
        # if len(comp.melodies) > 2:
        #     s += s
    # write to MIDI file
    print("\nwriting MIDI file...")
    mid.write(f'./midi/{comp.midiFileName}')
    return 0