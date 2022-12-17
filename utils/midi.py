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
from core.constants import (
    INSTRUMENTS, NOTES, MIDI_LOC
)

from containers.note import Note
from containers.melody import Melody
from containers.chord import Chord
from containers.composition import Composition


def note_name_to_MIDI_num(note: str) -> int:
    """
    returns the corresponding MIDI note for a
    given note name string. apparently MIDI note numbers
    are the given index of a note in NOTES plus 21
    """
    return NOTES.index(note) + 21


def MIDI_num_to_note_name(num: int) -> str:
    """
    returns the corresponding note name string from a
    given MIDI note number
    """
    return NOTES[num - 21]


def instrument_to_program(instr: str) -> int:
    """
    returns an instrument program number using INSTRUMENTS, which
    maps names to number via their index values.
    """
    inst_name = normalize_str(instr)
    inst_list = [normalize_str(name) for name in INSTRUMENTS]
    return inst_list.index(inst_name)


def tempo2bpm(tempo: int) -> int:
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
    if file_name[-4:] != ".mid":
        raise ValueError("must be a midi file name!")
    return MidiFile(filename=file_name)


def parse_midi(file_name: str) -> tuple:
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


def _build_melody(start: float, end: float,
                  cur_part: Melody, midi_writer: PrettyMIDI):

    end += cur_part.rhythms[0]
    instrument = instrument_to_program(cur_part.instrument)
    mel = Instrument(program=instrument)

    for j in range(1, len(cur_part.notes)):
        mel.notes.append(Note(velocity=cur_part.dynamics[j-1],
                              pitch=note_name_to_MIDI_num(cur_part.notes[j-1]),
                              start=start,
                              end=end))
        start += cur_part.rhythms[j-1]
        end += cur_part.rhythms[j]
    # add mel: Instrument() to instrument list
    midi_writer.instruments.append(mel)
    return start, end, midi_writer


def _build_chord(start: float, end: float,
                 cur_part: Chord, midi_writer: PrettyMIDI):

    end += cur_part.rhythm
    instrument = instrument_to_program(cur_part.instrument)
    chord = Instrument(program=instrument)

    for note in cur_part.notes:
        chord.notes.append(Note(velocity=cur_part.dynamic,
                                pitch=note_name_to_MIDI_num(note),
                                start=start,
                                end=end))
    # add chord progression to instrument list
    midi_writer.instruments.append(chord)
    start += cur_part.rhythm

    return start, end, midi_writer


def save(comp: Composition) -> None:
    """
    Takes a composition object and constructs
    data to be written out to a MIDI file
    """

    # nothing to write out
    if len(comp.parts) == 0:
        print("No tracks! Exiting...")
        return

    midi_writer = PrettyMIDI(initial_tempo=comp.tempo)

    # iterate over comp.tracks dictionary
    for part in comp.parts:
        # reset start and end markers for each track
        start, end = 0.0, 0.0
        cur_part = comp.parts[part]

        # handle Melody() object
        if isinstance(cur_part, Melody):
            start, end, midi_writer = _build_melody(start, end, cur_part, midi_writer)

        # handle Chord() object
        elif isinstance(cur_part, Chord):
            start, end, midi_writer = _build_chord(start, end, cur_part, midi_writer)

        # handle a list of Chord() or Melody() objects (or both!)
        elif isinstance(cur_part, list):
            for item in cur_part:
                if isinstance(item, Melody):
                    start, end, midi_writer = _build_melody(start, end, item, midi_writer)
                elif isinstance(item, Chord):
                    start, end, midi_writer = _build_chord(start, end, item, midi_writer)
                else:
                    raise TypeError(f"Unsupported type! Cur_part is type: {type(cur_part)} "
                                    "Should be a Melody or Chord object, or list of either(or both)")

        else:
            raise TypeError(f"Unsupported type! Cur_part is type: {type(cur_part)} "
                            "Should be a Melody or Chord object, or list of either(or both)")

    # write to MIDI file
    print(f"saving {comp.midi_file_name} ... ")
    midi_writer.write(f'{MIDI_LOC}/{comp.midi_file_name}')
