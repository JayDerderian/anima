''' 
Utility functions for working with MIDI I/O


NOTE: Double check the math for how strt and end are incremented according to
the supplied durations. Either Finale is doing something weird or the compounding
values are creating highly precice floating point numbers that might make sheet music
representation very messy. 
  
'''

import pretty_midi as pm
from tqdm import trange
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
            # create melody instrument
            instrument = pm.instrument_name_to_program(comp.melodies[i].instrument)
            mel = pm.Instrument(program=instrument)
            # add *this* melody's notes
            for j in range(len(comp.melodies[i].notes)):
                # translate note to MIDI note
                note = pm.note_name_to_number(comp.melodies[i].notes[j])
                anote = pm.Note(
                    velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
                # add to instrument object
                mel.notes.append(anote)
                # increment strt/end times
                strt += comp.melodies[i].rhythms[j]
                # try:
                #     end += comp.melodies[i].rhythms[j+1]
                # except (ValueError, IndexError):
                #     break
                '''NOTE: for some reason the above try/catch block isn't working...'''
                j+=1
                if j == len(comp.melodies[i].notes):
                    break
                else:
                    end += comp.melodies[i].rhythms[j]
                
            # add melody to instrument list
            mid.instruments.append(mel)

    # add chords
    if len(comp.chords) > 0:
        # iterate through a dictionary of chord() object lists.
        key = 0
        cl = len(comp.chords)
        for i in range(cl):
            # retrieve current chord object list
            chrds = comp.chords[key]
            if type(chrds) == list:
                strt = 0
                end = chrds[key].rhythm
                instrument = pm.instrument_name_to_program(chrds[i].instrument)
            else:
                strt = 0
                end = chrds.rhythm
                instrument = pm.instrument_name_to_program(chrds.instrument)
            chord = pm.Instrument(program=instrument)
            # iterate through current chord list
            for j in range(len(chrds)):
                # this list of chord objects notes
                for k in range(len(chrds[j].notes)):
                    # translate note to MIDI note
                    note = pm.note_name_to_number(chrds[j].notes[k])
                    anote = pm.Note(
                        velocity=chrds[j].dynamic, pitch=note, start=strt, end=end)
                    # add to instrument object
                    chord.notes.append(anote)
                # increment strt/end times
                strt += chrds[j].rhythm
                try:
                    end += chrds[j+1].rhythm
                except IndexError:
                    break
            # add chord progression to instrument list
            mid.instruments.append(chord)
            key+=1

    # add melodichords
    if len(comp.melodichords) > 0:

        '''NOTE: figure out a way to check next object type when incrementing strt and end
                 next melody -> comp.melodichords[item+1].rhythm[0]
                 next chord -> comp.melodichords[item+1].rhythm '''
        
        strt = 0
        l = len(comp.melodichords)
        for item in range(l):

            # is this a melody object?
            if isinstance(comp.melodichords[item], Melody):

                print("saving melody...")

                # strt = 0
                end = comp.melodichords[item].rhythms[0]
                # create melody instrument
                instrument = pm.instrument_name_to_program(comp.melodichords[item].instrument)
                mel = pm.Instrument(program=instrument)

                # add *this* melody's notes
                for j in range(len(comp.melodichords[item].notes)):
                    # translate note to MIDI note
                    note = pm.note_name_to_number(comp.melodichords[item].notes[j])
                    anote = pm.Note(
                        velocity=comp.melodichords[item].dynamics[j], pitch=note, start=strt, end=end)
                    # add to instrument object
                    mel.notes.append(anote)
                    # try:
                    #     end += comp.melodichords[i].rhythms[j+1]
                    # except (ValueError, IndexError):
                    #     break
                    '''NOTE: for some reason the above try/catch block isn't working...'''
                    j+=1
                    if j == len(comp.melodichords[item].notes):
                        break
                    else:
                        end += comp.melodichords[item].rhythms[j]

                # add melody to instrument list
                mid.instruments.append(mel)

            # or a chord object?
            elif isinstance(comp.melodichords[item], Chord):
                
                print("saving chord...")

                # strt = 0
                end = comp.melodichords[item].rhythm
                instrument = pm.instrument_name_to_program(comp.melodichords[item].instrument)
                ci = pm.Instrument(program=instrument)

                for k in range(len(comp.melodichords[item].notes)):
                    # translate note to MIDI note
                    note = pm.note_name_to_number(comp.melodichords[item].notes[k])
                    anote = pm.Note(
                        velocity=comp.melodichords[item].dynamic, pitch=note, start=strt, end=end)
                    # add to instrument object
                    ci.notes.append(anote)
                try:
                    # increment strt/end times
                    strt += comp.melodichords[item].rhythm
                    if isinstance(comp.melodichords[item+1], Chord):
                        end += comp.melodichords[item+1].rhythm
                    elif isinstance(comp.melodichords[item], Melody):
                        end += comp.melodichords[item+1].rhythm[0]
                except IndexError:
                    break
                mid.instruments.append(ci)

    # write to MIDI file
    print("\nsaving", comp.midi_file_name, "...")
    mid.write(f'./midi/{comp.midi_file_name}')