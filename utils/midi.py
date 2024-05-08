"""
Utility functions for working with MIDI data and I/O
"""

from os.path import join
from mido import MidiFile, MidiTrack, Message, MetaMessage
from pretty_midi import PrettyMIDI, Instrument

from utils.tools import normalize_str
from core.constants import INSTRUMENTS, NOTES, MIDI_FOLDER
from containers.note import Note
from containers.melody import Melody
from containers.chord import Chord
from containers.composition import Composition


def is_valid_midi_num(num: int) -> bool:
    """
    Returns True if the midi number is valid
    """
    return True if num >= 21 and num <= 108 else False


def note_name_to_MIDI_num(note: str) -> int:
    """
    returns the corresponding MIDI note for a
    given note name string.

    Midi numbers start at 21 and go to 108 because reasons.
    See: https://newt.phys.unsw.edu.au/jw/notes.html

    Our implementation uses indicies to match note names to note numbers,
    so we compensate for the difference in value between the index and the
    MIDI number by adding (or subtracting) 21.
    """
    return NOTES.index(note) + 21


def MIDI_num_to_note_name(num: int) -> str:
    """
    returns the corresponding note name string from a
    given MIDI note number.
    """
    if num < 21 or num > 108:
        raise ValueError("MIDI number must be between 21 and 108")
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
    if not file_name.endswith(".mid"):
        raise ValueError("must be a midi file name!")
    return MidiFile(filename=file_name)


def parse_midi(file_name: str) -> tuple[dict, list]:
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
        tracks.update(
            {
                f"track {str(i)}": track,
            }
        )
        for msg in track:
            msgs.append(msg)
    return tracks, msgs


def _to_instrument(part) -> Instrument:
    return Instrument(program=instrument_to_program(part.instrument))


def _build_melody(
    start: float, end: float, cur_part: Melody, mel_inst: Instrument
) -> tuple[float, float, Instrument]:
    end += cur_part.rhythms[0]
    for i in range(1, len(cur_part.notes)):
        mel_inst.notes.append(
            Note(
                velocity=cur_part.dynamics[i - 1],
                pitch=note_name_to_MIDI_num(cur_part.notes[i - 1]),
                start=start,
                end=end,
            )
        )
        start += cur_part.rhythms[i - 1]
        end += cur_part.rhythms[i]

    return start, end, mel_inst


def _build_chord(
    start: float, end: float, cur_part: Chord, chord_inst: Instrument
) -> tuple[float, float, Instrument]:
    end += cur_part.rhythm
    for note in cur_part.notes:
        chord_inst.notes.append(
            Note(
                velocity=cur_part.dynamic,
                pitch=note_name_to_MIDI_num(note),
                start=start,
                end=end,
            )
        )
    start += cur_part.rhythm

    return start, end, chord_inst


def export_midi(comp: Composition) -> None:
    """
    Takes a composition object and constructs data to be written out to a MIDI file
    """
    if len(comp.parts) == 0:
        print("No tracks! Exiting...")
        return

    midi_writer = PrettyMIDI(initial_tempo=comp.tempo)

    # iterate over comp.parts dictionary
    for part in comp.parts:
        # reset start and end markers for each track
        start, end = 0.0, 0.0
        cur_part = comp.parts[part]

        # handle Melody() object
        if isinstance(cur_part, Melody):
            _, _, instrument = _build_melody(
                start, end, cur_part, _to_instrument(cur_part)
            )
            midi_writer.instruments.append(instrument)
        # handle Chord() object
        elif isinstance(cur_part, Chord):
            _, _, instrument = _build_chord(
                start, end, cur_part, _to_instrument(cur_part)
            )
            midi_writer.instruments.append(instrument)

        # handle a list of Chord() or Melody() objects (or both!)
        # should be a single track!
        elif isinstance(cur_part, list):
            # we pick the instrument using the first object. instruments will
            # all have the same MIDI instrument since every object in this list will
            # also have the same instrument.
            instrument = _to_instrument(cur_part[0])
            for item in cur_part:
                if isinstance(item, Melody):
                    start, end, instrument = _build_melody(start, end, item, instrument)
                elif isinstance(item, Chord):
                    start, end, instrument = _build_chord(start, end, item, instrument)
                else:
                    raise TypeError(
                        f"Unsupported type! Cur_part is type: {type(cur_part)} "
                        "Should be a Melody or Chord object, or list of either(or both)"
                    )
            midi_writer.instruments.append(instrument)
        else:
            raise TypeError(
                f"Unsupported type! Cur_part is type: {type(cur_part)} "
                "Should be a Melody or Chord object, or list of either(or both)"
            )

    # write to MIDI file
    print(f"\nsaving {comp.midi_file_name} ... ")
    midi_writer.write(join(MIDI_FOLDER, comp.midi_file_name))
