''' 
Utility functions for working with MIDI I/O


NOTE: Double check the math for how strt and end are incremented according to
the supplied durations. Either Finale is doing something weird or the compounding
values are creating highly precice floating point numbers that might make sheet music
representation very messy. 
  
'''

import pretty_midi as pm

from containers.melody import Melody
from containers.chord import Chord


# exports a MIDI file for any sized composition (1 solo melody to ensemble sized n)
def save(comp):
    '''
    General save function for compositions. *All instruments start at the same time!*
    Exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
    
    Requires a composition() object.
    '''
    # create PM object. PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=comp.tempo)
    
    # add melodies
    if len(comp.melodies) > 0:
        ml = len(comp.melodies)
        for i in range(ml):
            strt = 0
            end = comp.melodies[i].rhythms[0]
            instrument = pm.instrument_name_to_program(comp.melodies[i].instrument) # create melody instrument
            mel = pm.Instrument(program=instrument)
            for j in range(len(comp.melodies[i].notes)):                            # add *this* melody's notes
                note = pm.note_name_to_number(comp.melodies[i].notes[j])            # translate note to MIDI note
                anote = pm.Note(
                    velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
                mel.notes.append(anote)                                             # add to instrument object
                strt += comp.melodies[i].rhythms[j]                                 # increment strt/end times
                try:
                    end += comp.melodies[i].rhythms[j+1]
                except IndexError:
                    break
            mid.instruments.append(mel)                                             # add melody to instrument list

    # add chords
    if len(comp.chords) > 0:   
        key = 0                                                                     # iterate through a dictionary of chord() object lists.
        cl = len(comp.chords)
        for i in range(cl):
            chrds = comp.chords[key]                                                # retrieve current chord object list
            if type(chrds) == list:
                strt = 0
                end = chrds[key].rhythm
                instrument = pm.instrument_name_to_program(chrds[i].instrument)
            else:
                strt = 0
                end = chrds.rhythm
                instrument = pm.instrument_name_to_program(chrds.instrument)
            chord = pm.Instrument(program=instrument)
            for j in range(len(chrds)):                                             # iterate through current chord list
                for k in range(len(chrds[j].notes)):                                # add this list of chord objects notes
                    note = pm.note_name_to_number(chrds[j].notes[k])                # translate note to MIDI note
                    anote = pm.Note(
                        velocity=chrds[j].dynamic, pitch=note, start=strt, end=end)
                    chord.notes.append(anote)                                       # add to instrument object
                strt += chrds[j].rhythm
                try:
                    end += chrds[j+1].rhythm                                        # increment strt/end times
                except IndexError:
                    break
            mid.instruments.append(chord)                                           # add chord progression to instrument list
            key+=1

    # add melodichords
    if len(comp.melodichords) > 0:

        '''NOTE: currently creating a separate track every time a chord 
        or melody is inputted. this was a similar problem from before...'''
        
        strt = 0
        l = len(comp.melodichords)
        for item in range(l):
            melodichords = comp.melodichords[item]                                          # get THIS list of melody()/chord() objects
            if isinstance(melodichords[item], Melody):                                     # is this a melody object?
                # strt = 0
                end = melodichords[item].rhythms[0]    
                instrument = pm.instrument_name_to_program(melodichords[item].instrument)  # create melody instrument
                mel = pm.Instrument(program=instrument)        
                for j in range(len(melodichords[item].notes)):                             # add *this* melody's notes
                    note = pm.note_name_to_number(melodichords[item].notes[j])             # translate note to MIDI note
                    anote = pm.Note(
                        velocity=melodichords[item].dynamics[j], pitch=note, start=strt, end=end)   
                    mel.notes.append(anote)                                                # add to instrument object
                    strt += melodichords[item].rhythms[j]
                    try:                                                                   # increment strt/end times
                        if isinstance(melodichords[item+1], Chord):
                            end += melodichords[item+1].rhythm
                        elif isinstance(melodichords[item], Melody):
                            end += melodichords[item+1].rhythms[0]
                    except IndexError:
                        break
                mid.instruments.append(mel)                                                # add melody to instrument list
            elif isinstance(melodichords[item], Chord):                                    # or a chord object?
                # strt = 0
                end = melodichords[item].rhythm
                instrument = pm.instrument_name_to_program(melodichords[item].instrument)
                ci = pm.Instrument(program=instrument)
                for k in range(len(melodichords[item].notes)):
                    note = pm.note_name_to_number(melodichords[item].notes[k])             # translate note to MIDI note
                    anote = pm.Note(
                        velocity=melodichords[item].dynamic, pitch=note, start=strt, end=end)
                    ci.notes.append(anote)                                                 # add to instrument object
                try:                                                                       # increment strt/end times
                    strt += melodichords[item].rhythm
                    if isinstance(melodichords[item+1], Chord):
                        end += melodichords[item+1].rhythm
                    elif isinstance(melodichords[item], Melody):
                        end += melodichords[item+1].rhythm[0]
                except IndexError:
                    break
                mid.instruments.append(ci)

    # write to MIDI file
    print("\nsaving", comp.midi_file_name, "...")
    mid.write(f'./midi/{comp.midi_file_name}')