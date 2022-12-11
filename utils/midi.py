"""
Utility functions for working with MIDI data and I/O
"""

from pretty_midi import PrettyMIDI, Instrument
from mido import (
    MidiFile,
    MidiTrack,
    Message,
    MetaMessage
)

from utils.tools import normalize_str
from core.constants import INSTRUMENTS, NOTES

from containers.note import Note
from containers.melody import Melody
from containers.chord import Chord
from containers.composition import Composition


def note_name_to_MIDI_num(note):
    """
    returns the corresponding MIDI note for a
    given note name string. apparently MIDI note numbers
    are the given index of a note in NOTES plus 21
    """
    return NOTES.index(note) + 21


def MIDI_num_to_note_name(num):
    """
    returns the corresponding note name string from a
    given MIDI note number
    """
    return NOTES[num - 21]


def instrument_to_program(instr):
    """
    returns an instrument program number using INSTRUMENTS, which
    maps names to number via their index values.
    """
    inst_name = normalize_str(instr)
    inst_list = [normalize_str(name) for name in INSTRUMENTS]
    return inst_list.index(inst_name)


def tempo2bpm(tempo):
    """
    converts a MIDI file tempo to tempo in BPM.
    can also take a BPM and return a MIDI file tempo

    - 250000 => 240
    - 500000 => 120
    - 1000000 => 60

    1 minute is 60,000,000 microseconds
    """
    return int(round((60 * 1000000) / tempo))


def load_midi_file(file_name: str) -> MidiFile:
    """
    loads a MIDI file using a supplied file name (i.e "song.mid")
    """
    if file_name[-4:] != '.mid':
        raise ValueError('must be a midi file name!')
    return MidiFile(filename=file_name)


def parse_midi(file_name):
    """
    retrieves a midi file from current working directory
    with a supplied file_name string.

    returns a tuple:
        - a dict with each key being a string representing
          the track number, i.e. "track 1", with the value being
          an individual track (list of Message() objects)
        - a list[Message()] of individual messages,
          ***that are separated from their original tracks! ***
    """
    msgs = []
    tracks = {}
    file = load_midi_file(file_name)
    for i, track in enumerate(file.tracks):
        tracks.update({
            f'track {str(i)}': track,
        })
        for msg in track:
            msgs.append(msg)
    return tracks, msgs


def save(comp: Composition) -> None:
    """
    Takes a composition object and constructs
    data to be written out to a MIDI file
    """

    # nothing to write out
    if len(comp.tracks) == 0:
        print("No tracks! Exiting...")
        return

    midi_writer = PrettyMIDI(initial_tempo=comp.tempo)

    # iterate over comp.tracks dictionary
    for track in comp.tracks:
        # empty track, continue on
        if len(comp.tracks[track]) == 0:
            continue

        # reset start and end markers for each track
        strt, end = 0.0, 0.0
        # list of either (or both!) Melody() or Chord() objects
        cur_track = comp.tracks[track]

        for item in cur_track:
            # handle Melody() object
            if isinstance(item, Melody):
                end += item.rhythms[0]
                instrument = instrument_to_program(item.instrument)
                mel = Instrument(program=instrument)

                for j in range(1, len(item.notes)):
                    mel.notes.append(Note(velocity=item.dynamics[j-1],
                                          pitch=note_name_to_MIDI_num(item.notes[j-1]),
                                          start=strt,
                                          end=end))
                    strt += item.rhythms[j-1]
                    end += item.rhythms[j]

                # add mel: Instrument() to instrument list
                midi_writer.instruments.append(mel)

            # handle Chord() object
            elif isinstance(item, Chord):
                end += item.rhythm
                instrument = instrument_to_program(item.instrument)
                chord = Instrument(program=instrument)

                for note in item.notes:
                    chord.notes.append(Note(velocity=item.dynamic,
                                            pitch=note_name_to_MIDI_num(note),
                                            start=strt,
                                            end=end))
                # add chord progression to instrument list
                midi_writer.instruments.append(chord)
                strt += item.rhythm

            else:
                raise TypeError("Needs to be either a Melody() or Chord() object instance!")

    # write to MIDI file
    print('\nsaving', comp.midi_file_name, '...')
    midi_writer.write(f'./midi/{comp.midi_file_name}')
