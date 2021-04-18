#****************************************************************************************************************#
#---------------------------This class handles creating a purely "random" composition----------------------------#
#****************************************************************************************************************#

#IMPORTS
import mido
import pretty_midi
from create import generate as create

'''
------------------------------------------------------NOTES--------------------------------------------------------------
    ALGORITHM:

    0. Pure random. RNG rules all.
        0.1. Decide on number of instruments

        0.2. Decide global tempo (invariant... for now)

        0.3. For each instrument, generate n number of notes and/or chords (not restricted to human playability). Each
             instrument will decide whether it only plays notes, chords, or both.
            0.3.1. Generate list of randomly selected note names in randomly selected octaves of n length.
            0.3.2. Generate list of individual lists of random note names in random octaves of n length.
                0.3.2.1. Each sub-list is a "chord"
                0.3.2.2. Each chord's voicings will be randomized.
            0.3.3. Generate durations for each note or chord (must not repeat any previous duration!)
                0.3.3.1. If a repeated value is found, take prev occurance value and either augment 
                         or diminish it by n. Check for duplicates and continue loop until no other
                         duplicates are found.
                0.3.3.2. Chord durations are defined as a set of integers attached to a common time duration.
            0.3.4 Generate dynamics for each chord

------------------------------------------------------------------------------------------------------------------------
'''


#Pure "random" mode
class randomMode(generate):
    def __init__(self):
        super().__init__()

        ''''
        1.Pick tempo and instrument(s).
            1.1. If more than one, create a while-loop that iterates n times
                 while randomly selecting indicies of a dictionary containing 
                 MIDI instrument names.

                 ex.

                 tempo = self.newTempo(choice.howFast(self)) (pick from list of standard metronome markings)

                 num_instr = choice.howManyInstruments(self) (1 - n)

                 pm = pretty_midi.PrettyMidi(initial_tempo = tempo) Create object w/ specified tempo (refer to docs for other param's...)
                 while (i < num_instr):
                     instrument = choice.whichInstrument(self) (0 - n)
                     instrument = pretty_midi.instrument_to_name_program(instrument)
                     pm.instruments.append(pretty_midi.Instrument(instrument))
                     i+=1

        2.????

        3.???? 
        '''

    #def pickTempo(self):

    #def pickInstrument(self):

    #def createPiece(self):

