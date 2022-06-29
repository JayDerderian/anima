'''
This module handles all large-scale decision making with regards to each composition mode. 

This should essentially be a wrapper for the generate module, wherein this module applies
weighted decisions towards the randomly generated material from the various methods in 
the generate file. 

This should also handle all large-scale decision making with regards to some "higher" level
compositon "modes" (i.e. styles - "minimalise" mode, "tonal" mode, "12-tone mode", etc...)

TODO:
    implement a way to pick elements from a randomly generated set (like a melody or chord progression) and 
    assign a "preference" (weights) to them. once this is done use these preferred subsets and develop them alongside 
    other randomly generated elements. ideally it'll allow for some degree of "organic" emergence (since each 
    preference is chosen randomly). use these preference to generate weighted decisions. 
    also, look into weighted decisions. 
'''

from math import floor
from random import randint, choice, choices

from core.generate import Generate

class Decide:

    def __init__(self):

        # Session info.
        self._min_choices = {}
        self._tonal_choices = {}
        self._modal_choices = {}
        self._atonal_choices = {}
        self._twelve_tone_choices = {}

    '''
    NOTE: This will eventually contain a series of decision trees that will determine how to execute 
            different composition "modes"
    '''
    # Minimalist mode choices
    def min_choices(self):
        '''
        Decides generation parameters for minimalist mode

        1 Type_____________________________
             |            |               |
           1 Drone    2 Arp/fig     3 Rhythmic
                                    
        2 Total (3-7)        
        '''
        self._min_choices['Type'] = randint(1,3)
        self._min_choices['Total'] = randint(3,7)
        return self._min_choices

    # Tonal mode choices
    def tonal_choices(self):
        '''
        Decides generation parameters for tonal mode.
            Limited to standard church modes!

        Start with deciding the "home" key
        Generate triads (built of each scale degree) for home key
        Generate triads for each modulation destination / tonal space

        Decide tonal space progression. 
        Always start and end with "home" key, no matter where we proceed in our tonal spaces!
            [Home key, ?, ?, ..., Home key]

        Generate progressions for each tonal space (to be repeated once decided!)
            Follow some standard progressions (make dict of progs? )
            I IV V I
            ii v i
            ...

            find resource and make a constant to pull from.
        '''



        return self._tonal_choices


    # Tonal/modal mode choices
    def modal_choices(self):
        '''
        Decides generation parameters for tonal/modal mode
        '''

        return self._modal_choices

    # Atonal mode choices
    def atonal_choices(self):
        '''
        Decides generation parameters for atonal mode
        '''

        return self._atonal_choices

    # Twelve-tone mode choices
    def twelve_tone_choices(self):
        '''
        Decides generation parameters for twelve-tone mode
        '''        

        return self._twelve_tone_choices


    ### ------- VARIATION GENERATION -------- ###
    '''
    NOTE:
        - These functions are intended to work off a given MIDI file. The variations.py file has more info.
        - Update variations.py with updated choices in mainChoice().
    '''    

    def var_main_choice(self):
        '''
        What do we want to do?
        1 - Modify notes 
        2 - Modify rhythms
        3 - Modify dynamics
        4 - Modify 1 and 2
        5 - Modify 1 and 3
        6 - Modify 2 and 3
        7 - Modify ALL
        '''
        return randint(1, 7)


    def what_to_do_notes(self):
        '''
        Choices: 
            1. Add/remove notes, transpose, or both?
            
            2. Transpose Up (1), down (2), transpose up AND down (3), 
               add note (4), remove note (5), both add AND remove(6)
        '''
        return randint(1, 6)
    
 
    def what_to_do_rhythms(self):
        '''
        Choices (rhythms): Augment (1), diminish(2), augment AND diminish (3)
        '''
        return randint(1, 3)

 
    def how_many_to_modify(self, total):
        '''
        Determines how many notes to modify of a given total.
        '''
        print("\nDeciding how many notes or rhythms to modify...")
        total_mod = self.scale_how_many(total)    # Scale to file size/note count
        total_mod = randint(1, total_mod)         # Decide how many to modify given this new total
        if(total_mod <= 0):
            print("...Unable to decide!")
            return 0
        return total_mod


    def how_many_reps(self, notes):
        '''
        Determines how many times to repeat a note, scaled to
        the amount of rhythms generated for this melody.

        Returns 0 if supplied notes is null, and 1 if it
        receives an empty list
        '''
        if(len(notes) == 0):
            return 1
        reps = 0
        if(len(notes) > 10):
            reps = randint(1, floor(len(notes) / 5))  # Limit to max 1/5
        elif(len(notes) > 8):
            reps = randint(1, floor(len(notes) / 4))  # Limit to max 1/4
        elif(len(notes) > 6):
            reps = randint(1, floor(len(notes) / 3))  # Limit to max 1/3
        return reps

    # Scales how_many to different MIDI note file sizes
    def scale_how_many(self, total):
        if(total == 0):
            return 0
        if(total > 1000):
            total *= 0.6
        elif(total > 5000):
            total *= 0.55
        elif(total > 10000):
            total *= 0.5
        elif(total > 20000):
            total *= 0.35
        elif(total > 50000):
            total *= 0.3
        elif(total > 100000):
            total *= 0.25
        elif(total > 200000):
            total *= 0.2
        elif(total > 500000):
            total *= 0.1 
        return floor(total) 

    # Which notes should we modify given a list of note numbers?
    # Generates list of index numbers to be used with theNotes[] 
    def which_notes_to_modify(self, total):    
        '''
        Which notes should we modify given a list of note numbers?
        Generates list of index numbers to be used with a pretty_midi object.
        Formerly used with theNotes[]
        '''   
        print("\nDeciding which notes to modify...") 
        notes_to_modify = []

        while(len(notes_to_modify) < total):            # Generate raw, un-sorted index choice list within given range (total)
            notes_to_modify.append(randint(0, total))

        notes_to_modify = list(set(notes_to_modify))    # Remove any duplicates
        notes_to_modify.sort()                          # Sort resulting list by ascending value
        return notes_to_modify

