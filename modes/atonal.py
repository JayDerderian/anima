'''
This module will (eventually) handle generating atonal compositions using Forte Prime forms and harmonies
derived from one or more prime forms. 
'''

'''
ALGORITHM:

    3. "Atonal" mode (random pitch class prime form selections)
        3.1. Generate x number of prime forms.
            3.1.1. Decide on central prime form.
            3.1.2. Generate interval vector from central prime form.
        3.2 Transpose/permutate central prime form. Store results in list.
            3.2.1 Randomly chose elements from x amount of results from transpositions/permutations
        3.3 Generate scales based off elements from central prime form (each element is a new 'root')    
            3.3.1. Each scale length is 11 notes (12tet)
'''
