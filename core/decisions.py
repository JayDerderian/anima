'''
This module handles all large-scale decision making with regards to each composition mode. 
'''

'''
TODO:
    implement a way to pick elements from a randomly generated set (like a melody or chord progression) and 
    assign a "preference" to them. once this is done use these preferred subsets and develop them alongside 
    other randomly generated elements. ideally it'll allow for some degree of "organic" emergence (since each 
    preference is chosen randomly). use these preference to generate weighted decisions. 
    also, look into weighted decisions. 
'''


# IMPORTS
from math import floor
from random import randint

# Decision functions
class Decide():
    '''
    These are the RNG functions that make "decisions" about a variety of creative questions.  
    Basically you roll some dice and see what happens.

    This is the BASE CLASS for all generative functions.
    '''

    # Constructor
    def __init__(self):

        # Session info. Initialize empty dictionaries to contain current choices for each instance
        self.min_choices = {}
        self.modal_choices = {}
        self.atonal_choices = {}


    #-----------------------------------------------------------------------------------------------------------#
    #-----------------------------------------MATERIAL GENERATION-----------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------#
    
    '''
    NOTE: This will eventually contain a series of decision trees that will determine how to execute 
            different composition "modes"

    '''
    
    # Minimalist mode choices
    def min_choices(self):
        '''
        Decides generation parameters for minimalist mode
        '''
        # Create an empty dictionary
        choices = {}

        return choices

    # Tonal/modal mode choices
    def modal_choices(self):
        '''
        Decides generation parameters for tonal/modal mode
        '''
        # Create an empty dictionary
        choices = {}

        return choices

    # Atonal mode choices

    # 



    #---------------------------------------------------------------------------------------------------------------------#
    #------------------------------------------------VARIATION GENERATION-------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------#
    '''
    NOTES:
        
        - These functions are intended to work off a given MIDI file. The variations.py file has more info.
        - Update variations.py with updated choices in mainChoice().
    
    TODO: Create a single wrapper method - decisions() - for executing all choices and returning them 
          as a single dictionary.

    '''    

    # What do we want to do? modify notes (1), modify rhythms (2), both (3)
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
        print("\nDeciding what to do...")
        choice = randint(1, 7)
        if(choice == 1):
            print("...Modifying NOTES only!")
        elif(choice == 2):
            print("...Modifying RHYTHMS only!")
        elif(choice == 3):
            print("...Modifying DYNAMICS only!")
        elif(choice == 4):
            print("...Modifying NOTES & RHYTHMS!")
        elif(choice == 5):
            print("...Modifying NOTES & DYNAMICS!")
        elif(choice == 6):
            print("...Modifying RHYTHMS & DYNAMICS!")
        elif(choice == 7):
            print("...Modifying NOTES & RHYTHMS & DYNAMICS!")
        return choice

    # Choices (notes): Transpose Up (1), down (2), transpose up AND down (3), 
    # add note (4), remove note (5), both add AND remove(6)
    def what_to_do_notes(self):
        '''
        Choices: 
            1. Add/remove notes, transpose, or both?
            
            2. Transpose Up (1), down (2), transpose up AND down (3), 
               add note (4), remove note (5), both add AND remove(6)
        '''
        print("\nDeciding what to do with the notes...")
        choice = randint(1, 5)
        # Test outputs
        if(choice == 1):
            print("...Transposing UP only!")
        elif(choice == 2):
            print("...Transposing DOWN only!")
        elif(choice == 3):
            print("...Transposing UP & DOWN!")
        elif(choice == 4):
            print("...ADDING notes!")
        elif(choice == 5):
            print("...REMOVING notes!")
        elif(choice == 6):
            print("...ADDING & REMOVING notes!")
        return choice
    
    # Choices (rythms): Augment (1), diminish(2), augment AND diminish (3)
    def what_to_do_rhythms(self):
        '''
        Choices (rhythms): Augment (1), diminish(2), augment AND diminish (3)
        '''
        print("\nDeciding what to do with the rhythms...")
        choice = randint(1, 3)
        if(choice == 1):
            print("...Augmenting rhythms!")
        elif(choice == 2):
            print("...Diminishing rhythms!")
        elif(choice == 3):
            print("...Augment & diminish rhythms!")
        return choice

    # Determines how many notes to modify of a given total.
    def how_many_to_modify(self, total):
        '''
        Determines how many notes to modify of a given total.
        '''
        print("\nDeciding how many notes or rhythms to modify...")
        # Scale to file size/note count
        total_mod = self.scale_how_many(total)
        # Decide how many to modify given this new total
        total_mod = randint(1, total_mod)
        if(total_mod <= 0):
            print("...Unable to decide!")
        # print("Total:", totalModify)
        return total_mod

    # How many times should we repeat this note?
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
            # Limit to max 1/5
            reps = randint(1, floor(len(notes) / 5))
        elif(len(notes) > 8):
            # Limit to max 1/4
            reps = randint(1, floor(len(notes) / 4))
        elif(len(notes) > 6):
            # Limit to max 1/3
            reps = randint(1, floor(len(notes) / 3))
        return reps

    # Scales howMany to different MIDI note file sizes
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
    def which_notes_to_modify(self, total, total_notes):    
        '''
        Which notes should we modify given a list of note numbers?
        Generates list of index numbers to be used with a pretty_midi object.
        Formerly used with theNotes[]
        '''   
        notes_to_modify = []
        print("\nDeciding which notes to modify...") 
        # Generate raw, un-sorted index choice list within given range (totalNotes)
        while(len(notes_to_modify) < total):
            notes_to_modify.append(randint(0, total))
        # Remove any duplicates
        notes_to_modify = list(set(notes_to_modify))
        # Sort resulting list by ascending value 
        notes_to_modify.sort()
        return notes_to_modify