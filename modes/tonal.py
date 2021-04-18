#********************************************************************************************************************#
#---------------------------This class handles creating a "tonal/pandiatonic" composition----------------------------#
#********************************************************************************************************************#


'''
--------------------------------------------------------NOTES--------------------------------------------------------

ALGORITHM:

    2. "Tonal" mode (pan diatonic)
        2.1. Generate major scale from a randomly selected froom (0-11)
            2.1.1. Generate n number of associated scales
                2.1.1.1. Relative minor
                2.1.1.2. Modes based on each tonal center scale degree.
        2.2. Generate chord progression(s) based off tonal center and x number of associated scales. 
            2.2.1. Generate standard triads off each note in a major scale.
                2.2.1.1. Transpose this set of triads to any other note in the chromatic scale.
            2.2.2. Select n number of chords to be repeated x number of times
            2.2.3. Ability to transpose chord progression.
            2.2.4. Determine n number of repetitions of this progression. Possibly create list of different
                   repetition numbers.


--------------------------------------------------------------------------------------------------------------------
'''


'''
#"Pandiatonic" mode
class panDiatonic(generate):
    def __init__(self):
        super().__init__()
'''