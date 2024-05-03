from core.generate import Generate
from utils.midi import export_midi
from ensembles import the_escape as te


def main():
    create = Generate()
    comp = create.init_comp(te.TEMPO, title="the escape", composer="contra sigma")

    chords = te.gen_piano_chords()

    comp.add_part(part=chords, instr=te.PIANO)
    export_midi(comp)
