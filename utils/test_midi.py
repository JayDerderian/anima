"""
generates a simple MIDI file for testing parsing with
"""

from utils.midi import save
from utils.tools import scale_to_tempo

from containers.melody import Melody
from core.generate import Generate

def gen_test_mid():
    """
    generates a simple MIDI file for testing with
    """
    gen = Generate()
    comp = gen.init_comp(tempo=72.0)
    comp.title = "test"
    comp.midi_file_name = comp.title + ".mid"

    mel = Melody(tempo=comp.tempo,
                 instrument="Acoustic Grand Piano")
    mel.notes = ["C5", "D5", "E5", "C5"]
    mel.rhythms = [scale_to_tempo(tempo=comp.tempo, rhythms=0.5)] * len(mel.notes)
    mel.dynamics = [100] * len(mel.notes)

    comp.instruments.append(mel.instrument)
    comp.add_part(mel, mel.instrument)
    save(comp)
    comp.display()
