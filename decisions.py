'''
This module handles all large-scale decision making with regards to each composition mode. 
'''

'''
----------------------------------------------------NOTES-------------------------------------------------------

    This module contains the decide() class which handles decisions for generative and variation functions. 

    Class hierarchy:
        
        decide():
        
            generate():
                note()
                rhythms()
                ect..
                
                comp Modes:
                    random()
                    minimalist()
                    tonal()
                    atonal()
                    serialist()
                ect...

            variate/modify()
                mainDecision():
                howManyNotes():
                ect..

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import constants as c
from math import floor
from random import randint

#Decision functions
class decide():
    '''
    These are the RNG functions that make "decisions" about a variety of creative questions.  
    Basically you roll some dice and see what happens.

    This is the BASE CLASS for all generative functions.
    '''

    # Constructor
    def __init__(self):
        self.alive = True

    #-----------------------------------------------------------------------------------------------------------#
    #-----------------------------------------MATERIAL GENERATION-----------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------#
    '''
    NOTE: This will eventually contain a series of decision trees that will determine how to execute 
            different composition "modes"

    '''
    
    # Minimalist mode choices
    def minChoices(self):
        '''
        Decides generation parameters for minimalist mode
        '''
        # Create an empty dictionary
        choices = {}

        return choices

    # Tonal/modal mode choices
    def modalChoices(self):
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
    def mainChoice(self):
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
    def whatToDo(self):
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
    def whatToDoRhythms(self):
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
    def howMany(self, totalNotes):
        '''
        Determines how many notes to modify of a given total.
        '''
        print("\nDeciding how many notes or rhythms to modify...")
        # Scale to file size/note count
        totalModify = self.scaleHowMany(totalNotes)
        # Decide how many to modify given this new total
        totalModify = randint(1, totalModify)
        if(totalModify <= 0):
            print("...Unable to decide!")
        # print("Total:", totalModify)
        return totalModify

    # How many times should we repeat this note?
    def howManyRepetitions(self, notes):
        '''
        Determines how many times to repeat a note, scaled to
        the amount of rhythms generated for this melody.

        Returns 0 if supplied notes is null, and 1 if it
        receives an empty list
        '''
        if(len(notes) == 0):
            return 1
        reps = 0
        '''Note: change to if(len(notes)) % 3 == 0), etc?
                 Use total notes as divisible by n as the decider rather than
                 total notes itself. I dunno.'''
        if(len(notes) > 10):
            #Limit to 1/5
            limit = floor(len(notes) / 5)
            reps = randint(1, limit)
        elif(len(notes) > 8):
            #Limit to 1/4
            limit = floor(len(notes) / 4)
            reps = randint(1, limit)
        elif(len(notes) > 6):
            #Limit to 1/3
            limit = floor(len(notes) / 3)
            reps = randint(1, limit)
        return reps

    # Scales howMany to different MIDI note file sizes
    def scaleHowMany(self, totalNotes):
        if(totalNotes == 0):
            return 0
        if(totalNotes > 1000):
            totalNotes *= 0.6
        elif(totalNotes > 5000):
            totalNotes *= 0.55
        elif(totalNotes > 10000):
            totalNotes *= 0.5
        elif(totalNotes > 20000):
            totalNotes *= 0.35
        elif(totalNotes > 50000):
            totalNotes *= 0.3
        elif(totalNotes > 100000):
            totalNotes *= 0.25
        elif(totalNotes > 200000):
            totalNotes *= 0.2
        elif(totalNotes > 500000):
            totalNotes *= 0.1 
        return floor(totalNotes) 

    # Which notes should we modify given a list of note numbers?
    # Generates list of index numbers to be used with theNotes[] 
    def whichNotesToModify(self, totalModify, totalNotes):    
        '''
        Which notes should we modify given a list of note numbers?
        Generates list of index numbers to be used with a pretty_midi object.
        Formerly used with theNotes[]
        '''   
        notesToModify = []
        print("\nDeciding which notes to modify...") 
        #Generate raw, un-sorted index choice list within given range (totalNotes)
        while(len(notesToModify) < totalModify):
            notesToModify.append(randint(0, totalNotes))
        #Remove any duplicates
        notesToModify = list(set(notesToModify))
        #Sort resulting list by ascending value 
        notesToModify.sort()
        if(not notesToModify):
            print("...Unable to decide!")
        # print("Notes to modify: ", notesToModify)
        return notesToModify