'''
This module handles generating atonal compositions using serialist techniques.
'''

'''
--------------------------------------------------NOTES-------------------------------------------------------
    
ALGORITHM:

    4. "Serialist" mode (base generative functions on a given number series of n length. Include 12-tone.)
        4.1. Generate prime row of n length (3 - 11)
        4.2. This prime row is to be used as an integer list to pick notes, rhythms, and dynamics. All
             parameters are derived using this row. 
        4.3. Generate inversions, retrogrades, and retrograde inversions of each parameter derived from this row.
            4.3.1. Pitches will need to I, R, and RI verisions
            4.3.2. Rhythm inversions are derived using remainder of beat, for example if a rhythm is a sixteenth note,
                   then the "inversion" is the dotted eighth note.
            4.3.3. Dynamic inversions are ppp->fff, for example. 
        4.4. Store all derivations in individual dictionaries. 


--------------------------------------------------------------------------------------------------------------

'''