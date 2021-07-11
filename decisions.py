#****************************************************************************************************************#
#-------------------------------------This class handles decision functions------------=-------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------

    This module contains the decide() class which handles decisions for generative and variation functions. 

    Class hierarchy:
        
        decide():
        
            generate():
                note()
                rhythms()
                ect..
                
                Comp Modes:
                    random()
                    minimalist()
                    tonal()
                    atonal()
                    serialist()
                ect...

            variate()
                mainDecision():
                howManyNotes():
                ect..

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
import pretty_midi as pm
from pretty_midi import constants as inst
from random import randint

#Decision functions
class decide(object):
    '''
    These are the RNG functions that make "decisions" about a variety of creative questions.  
    Basically you roll some dice and see what happens.

    This is the BASE CLASS for all generative functions.
    '''

    # Constructor
    def __init__(self):

        # Used for rhythm modifications
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 
                        0.375, 0.25, 0.125]

    #-----------------------------------------------------------------------------------------------------------#
    #-----------------------------------------MATERIAL GENERATION-----------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------#

    # How many times should we repeat this note?
    def howManyRepetitions(self, notes):
        '''
        Determines how many times to repeat a note, scaled to
        the amount of rhythms generated for this melody.

        Returns 0 if supplied notes is null, and 1 if it
        receives an empty list
        '''
        if(notes is None):
            return 0
        elif(len(notes) == 0):
            return 1
        reps = 0
        '''Note: change to if(len(notes)) % 3 == 0), etc?
                 Use total notes as divisible by n as the decider rather than
                 total notes itself. I dunno.'''
        if(len(notes) > 10):
            #Limit to 1/5
            limit = math.floor(len(notes) / 5)
            reps = randint(1, limit)
        elif(len(notes) > 8):
            #Limit to 1/4
            limit = math.floor(len(notes) / 4)
            reps = randint(1, limit)
        elif(len(notes) > 6):
            #Limit to 1/3
            limit = math.floor(len(notes) / 3)
            reps = randint(1, limit)
        return reps

    # Choose melody parameters
    def melodyChoices(self):
        '''
        Choses parameters for melody generation. 
        Returns a list with each decision at a corresponding
        index.

        0 = rhythm choice (1 - 3)
        1 = dynamics choice (1 - 2)
        2 = tonality choice (1 - 2)
        3 = melodic range choice (1 - 4)
        4 = which single octave to use, if chosen (single int or None)
        5 = total elements (number of notes, rhythms, dynamics)
        '''
        choices = []

        #0 - Total elements (2-20)
        '''Determines total number of notes, rhythms, and dynamics.
           Each will be whatever randint() returns here.'''
        choices.append(randint(2, 20))

        #1 - Rhythm 
        '''Generate list of nonrepeating rhythms (1), a single repeated rhythm (2), 
           or alternate between non-repeat and repeat(3)?'''
        choices.append(randint(1, 3))

        #2 - Dynamics 
        '''Repeating single dynamic (1), non-repeating list(2), semi-repeating(3)?'''
        choices.append(randint(1, 3))

        #3 - Tonality: Tonal(1) or atonal(2)?
        choices.append(randint(1, 2))

        #4 - Melodic range
        '''Place notes in specified octave (1), used fixed range (2), 
           alternate between fixed octave and randomly chosen octaves (3),
           use randomly chosen octaves only (4)'''
        rangeChoice = randint(1, 4)
        choices.append(rangeChoice)

        #5 - Using one single octave (or not)
        if(rangeChoice == 1):
            # Which octave (2-6)?                     
            choices.append(randint(2, 6))
        else:
            choices.append(None)

        return choices

    # Choses a single instrument
    def newInstrument(self, tempo):
        '''
        Choses a MELODIC instrument from pretty_midi's container's module 
        which contains a mapping of integers to available MIDI instruments. 

        Returns a pretty_midi object containing the supplied tempo and the 
        newly chosen instrument. To be used for single instrument pieces.
        '''
        # Create new PrettyMIDI() instance
        newInstrument = pm.PrettyMIDI(initial_tempo = tempo)
        # Returns a string (I think) from the mapping
        # NOTE: Indices 0 - 110 are the MELODIC instruments in INSTRUMENT_MAP!
        instrument = inst.INSTRUMENT_MAP[randint(0, 110)]
        # Append to pm Instrument instance
        instrument = pm.Instrument(program = instrument)
        # Add to PrettyMIDI instance
        newInstrument.instruments.append(instrument)
        return newInstrument

    # Choses how many instruments to create (2 - 13 (for now))
    def howManyInstruments(self):
        return randint(2, 13)

    # Choses the instruments for a non-solo piece
    def newEnsemble(self, tempo):
        '''
        Generates a list of 2 - 13 MELODIC instruments. Does not 
        pick PERCUSSION instruments yet!

        Returns a pretty_midi object containing the supplied tempo and list of
        instruments. To be used for multi-instrument pieces.
        '''
        # Pick total number of instruments
        total = randint(2, 13)
        # Create new PrettyMIDI() instance
        newEnsemble = pm.PrettyMIDI(initial_tempo = tempo)
        # Select instruments
        while(len(newEnsemble.instruments) < total):
            # Returns a string (I think) from the mapping
            # NOTE: Indices 0 - 110 are the MELODIC instruments in INSTRUMENT_MAP!
            instrument = inst.INSTRUMENT_MAP[randint(0, 110)]
            # Append to pm Instrument object
            instrument = pm.Instrument(program = instrument)
            # Add to PrettyMIDI instance
            newEnsemble.instruments.append(instrument)
        return newEnsemble


    #---------------------------------------------------------------------------------------------------------------------#
    #------------------------------------------------VARIATION GENERATION-------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------#
    '''
    NOTES:
        
        - These functions are intended to work off a given MIDI file. The variations.py file has more info.
        - Update variations.py with updated choices in mainChoice().

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
        return math.floor(totalNotes) 

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

    #How much do we want to augment or diminish a rhythm?   
    def newDurations(self, totalModify):
        '''
        Returns a list of positive or negative floats representing
        how much to augment or diminish a rhythmic value by. 
        '''
        n = 0
        rhythmChanges = []  
        while(len(rhythmChanges) < totalModify):
            if(randint(1, 2) == 1):
                n += self.rhythms[randint(0, 9)]
                rhythmChanges.append(n)
            else:
                n -= self.rhythms[randint(0, 9)]
                rhythmChanges.append(n)
            n = 0
        return rhythmChanges


    #-----------------------------------------------------------------------------------------------------------------------#
    #------------------------------------------------COMPOSITION GENERATION-------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------#

    