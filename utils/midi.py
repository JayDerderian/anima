''' 
Utility functions for working with MIDI I/O

NOTE: Replace PrettyMid with MidiFile or MidiTrack, and Instrument with Message?
      Look at how PrettyMidi uses Instruments when writing out MIDI files.

      Look at midi.MidiFile().py in the resources file!
'''

from pretty_midi import PrettyMIDI, Instrument
from mido import MidiFile, MidiTrack, Message, MetaMessage

from utils.tools import normalize_str
from core.constants import INSTRUMENTS, NOTES
from containers.note import Note
from containers.melody import Melody
from containers.chord import Chord



def note_name_to_MIDI_num(note):
    '''
    returns the corresponding MIDI note for a 
    given note name string. apparently MIDI note numbers
    are the given index of a note in NOTES plus 21
    '''
    return NOTES.index(note)+21


def MIDI_num_to_note_name(num):
    '''
    returns the corresponding note name string from a 
    given MIDI note number
    '''
    return NOTES[num-21]


def instrument_to_program(instr):
    '''
    returns an instrument program number using INSTRUMENTS, which
    maps names to numbers via their index values.
    '''
    inst_name = normalize_str(instr)
    inst_list = [normalize_str(name) for name in INSTRUMENTS]
    return inst_list.index(inst_name)


def tempo2bpm(tempo):
    '''
    converts a MIDI file tempo to tempo in BPM. 
    can also take a BPM and return a MIDI file tempo

    - 250000 => 240
    - 500000 => 120
    - 1000000 => 60
    '''
    return int(round((60 * 1000000) / tempo))


def load(file_name):
    '''
    loads a MIDI file using a supplied file name (i.e "song.mid") 
    and returns a MidiFile() object 
    '''
    if type(file_name) != str:
        raise TypeError('filename must be a string!')
    elif file_name[-4:] != '.mid':
        raise TypeError('string must end with .mid!')
    return MidiFile(filename=file_name)


def parse(file_name):
    '''
    retrieves a midi file from current working directory
    with a supplied file_name string.

    returns:
        - a dict with each key being a string representing 
          the track number, i.e. "track 1"
        - a list[Messages()] of messages
    '''
    if file_name[-4:] != '.mid':
        raise ValueError('file_name must end with .mid!')
    file = MidiFile(filename=file_name)         # open the file.         
    res = {}                                    # store extracted note/rhythm/dynamics info. analyze each track separately!
    msgs = []                                   # individual MIDI messages.
    for i, track in enumerate(file.tracks):
        res["track " + str(i)] = track          # save track to dictionary     
        for msg in track:                       # save individual messages
            msgs.append(msg)
    return res, msgs


def save(comp):
    '''
    general save function for compositions. *All instruments start at the same time!*
    exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
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
                mel.notes.append(Note(velocity=comp.melodies[i].dynamics[j], 
                                      pitch=note_name_to_MIDI_num(comp.melodies[i].notes[j]), 
                                      start=strt, 
                                      end=end))                                            
                strt += comp.melodies[i].rhythms[j]                                 # increment strt/end times
                j+=1                                                                
                if j==len(comp.melodies[i].rhythms):
                    break
                # try:                                                              # NOTE for some reason this try/except block isn't working...
                #     end += comp.melodies[i].rhythms[j+1]
                # except IndexError:
                #     break
                end += comp.melodies[j]
            mid.instruments.append(mel)                                             # add melody to instrument list

    # add chords
    if len(comp.chords) > 0:   
        key = 0                                                                     # iterate through a dictionary of chord() object lists.
        cl = len(comp.chords)
        for i in range(cl):
            chrds = comp.chords[key]                                                # retrieve current chord object list
            strt = 0
            end = chrds[key].rhythm
            instrument = instrument_to_program(chrds[i].instrument)
            chord = Instrument(program=instrument)
            for j in range(len(chrds)):                                             # iterate through current chord list
                for k in range(len(chrds[j].notes)):                                # add this list of chord objects notes
                    chord.notes.append(Note(velocity=chrds[j].dynamic, 
                                            pitch=note_name_to_MIDI_num(chrds[j].notes[k]), 
                                            start=strt, 
                                            end=end))  
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
                instrument = instrument_to_program(melodichords[item].instrument)          # create melody instrument
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
    print('\nsaving', comp.midi_file_name, '...')
    mid.write(f'./midi/{comp.midi_file_name}')
