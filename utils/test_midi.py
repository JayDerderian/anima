"""
generates a simple MIDI file for testing parsing with
"""

from utils.midi import save
from utils.tools import scale_to_tempo

from containers.melody import Melody
from core.generate import Generate

def gen_test_mid():
    """
    generates a simple MIDI file for testing parsing with
    """
    g = Generate()
    comp = g.init_comp(tempo=72.0)
    comp.title = "test"
    comp.midi_file_name = comp.title + ".mid"

    m = Melody(tempo=comp.tempo,
               instrument="Acoustic Grand Piano")
    m.notes = ["C5", "D5", "E5", "C5"]
    m.rhythms = [scale_to_tempo(tempo=comp.tempo, rhythms=0.5)] * len(m.notes)
    m.dynamics = [100] * len(m.notes)

    comp.instruments.append(m.instrument)
    comp.melodies.append(m)
    save(comp)
    comp.display()
