''' 
Utility functions for working with MIDI I/O
'''

from pretty_midi import PrettyMIDI, Instrument
from mido import MidiFile, MidiTrack, Message

from utils.tools import normalize_str
from core.constants import INSTRUMENTS, NOTES
from containers.note import Note
from containers.melody import Melody
from containers.chord import Chord


# loads a MIDI file from a filename
def load(file_name):
    '''
    loads a MIDI file using a supplied file name and returns a MidiFile()
    object
    '''
    return MidiFile(filename=file_name, type=1)


# exports a MIDI file for any sized composition (1 solo melody to ensemble sized n)
def save(comp):
    '''
    General save function for compositions. *All instruments start at the same time!*
    Exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
    
    Requires a composition() object.
    '''
    # PM object is just used to just write out the file.
    mid = PrettyMIDI(initial_tempo=comp.tempo)
    
    # add melodies
    if len(comp.melodies) > 0:
        ml = len(comp.melodies)
        for i in range(ml):
            strt = 0
            end = comp.melodies[i].rhythms[0]
            instrument = instrument_to_program(comp.melodies[i].instrument)         # create melody instrument
            mel = Instrument(program=instrument)
            for j in range(len(comp.melodies[i].notes)):                            # add *this* melody's notes
                note = note_name_to_MIDI_num(comp.melodies[i].notes[j])             # translate note to MIDI note
                anote = Note(
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
                instrument = instrument_to_program(chrds[i].instrument)
            else:
                strt = 0
                end = chrds.rhythm
                instrument = instrument_to_program(chrds.instrument)
            chord = Instrument(program=instrument)
            for j in range(len(chrds)):                                             # iterate through current chord list
                for k in range(len(chrds[j].notes)):                                # add this list of chord objects notes
                    note = note_name_to_MIDI_num(chrds[j].notes[k])                # translate note to MIDI note
                    anote = Note(
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
            melodichords = comp.melodichords[item]                                         # get THIS list of melody()/chord() objects
            if isinstance(melodichords[item], Melody):                                     # is this a melody object?
                # strt = 0
                end = melodichords[item].rhythms[0]    
                instrument = instrument_to_program(melodichords[item].instrument)  # create melody instrument
                mel = Instrument(program=instrument)        
                for j in range(len(melodichords[item].notes)):                             # add *this* melody's notes
                    note = note_name_to_MIDI_num(melodichords[item].notes[j])              # translate note to MIDI note
                    anote = Note(
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
                instrument = instrument_to_program(melodichords[item].instrument)
                ci = Instrument(program=instrument)
                for k in range(len(melodichords[item].notes)):
                    note = note_name_to_MIDI_num(melodichords[item].notes[k])              # translate note to MIDI note
                    anote = Note(
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


# convert a note name string to MIDI number
def note_name_to_MIDI_num(note):
    '''
    returns the corresponding MIDI note for a 
    given note name string. apparently MIDI note numbers
    are the given index of a note in NOTES plus 21
    '''
    return NOTES.index(note) + 21


# convert instrument name to MIDI instrument number
def instrument_to_program(instr):
    '''
    returns an instrument program number using INSTRUMENTS, which
    maps names to numbers via their index values.
    '''
    inst_name = normalize_str(instr)
    inst_list = [normalize_str(name) for name in INSTRUMENTS]
    return inst_list.index(inst_name)