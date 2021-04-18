#*************************************************************************************************************#
#---------------------------This class handles creating a "minimalist" composition----------------------------#
#*************************************************************************************************************#


'''
----------------------------------------------------NOTES-----------------------------------------------------

ALGORITHM:

    1. "Minimalist" mode
        1.1 Decide whether to utilize a process-based generation mode, or
            a strictly repetition based mode.

        1.2. Process-based:
            1.2.1 Create short pattern to be repeated n amount of times.
                1.2.1.1. Generate list of notes within 3* octaves of n length. (* - could also be variable)
                         For each note: 
                         Which note, dynamic & octave? 
                         Repeat? if repeat, how many times and 
                         which duration should be repeated?
    
            1.2.2 Implement additive and subtractive procedures to 
                  alter a given pitch class set pattern very gradually
                  Pick a random note in a given set and either 
                  augment* its value x amount with each repetition.
                      
                  * - amount determined randomly.

        1.3 Repetition based:

        1.4 Ambient:
            Drones, swells, use of other non-rhythmic parameters to create
            a sense of "progress" and "change"
'''


'''
#"Minimalist" mode
class minimalism(generate):
    def __init__(self):
        super(generate).__init__()






'''