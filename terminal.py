'''
----------------------------------------------------------------------------------------------------
                       THIS FILE IS FOR RUNNING THE PROGRAM IN THE TERMINAL

    User options include: 
        -single melody generation (random or using source data) 
        -single chord generation (random or using source data) 
        -chord progression generation (random or using source data)
        -composition (1 random inst + pno) generation (random or using source data)

    Run via terminal in the program's directory using 'python terminal.py'

----------------------------------------------------------------------------------------------------
'''

# Imports
import constants as c
from test import newData
from random import randint
from generate import Generate
from modes.rando import newRandomComposition


# Main menu
def mainMenu():
    '''
    it's in the title
    '''
    print("\n")
    print("-------------------MAIN MENU-----------------")
    print("                                             ")
    print("   0. Exit                                   ")
    print("   1. Single new melody                      ")
    print("   2. Single new chord                       ")
    print("   3. New chord progression                  ")
    print("   4. New composition (1 melody + chords)    ")
    print("   5. More comp modes (NOT READY)            ")
    print("                                             ")
    print("---------------------------------------------")
    print("\n")

# Composition modes menu
def modesMenu():
    '''
    what are ya in the mood for?
    '''
    print("\n")
    print("------------Comp Modes------------")
    print("                                  ")
    print("      0. Pure random              ")
    print("      1. Tonal/modal              ")
    print("      2. Atonal                   ")
    print("      3. Serialist                ")
    print("      4. Minimalist               ")
    print("                                  ")
    print("----------------------------------")
    print("\n")    

# Data menu
def dataMenu():
    '''
    displays data input options
    '''
    print("\n")
    print("------------------Data Inputs-----------------")
    print("                                              ")
    print("    1. Random list of ints of n length        ")
    print("    2. Random list of floats of n length      ")
    print("    3. Random list of chars of n length       ")
    print("    4. Random 0xXXXXXX hex number             ")
    print("    5. Enter your name                        ")
    print("                                              ")
    print("----------------------------------------------")
    print("\n")

# Keep going?
def keepGoing():
    '''
    Must we?
    '''
    answer = input("\nWant to do something else? y = yes, n = no\n")
    if answer.isupper():
        answer = answer.lower()
    if answer == 'y':
        return True
    else:
        return False

# Driver code for using the generative functions in the terminal
def run():
    '''
    Main terminal driver code. 
    
    User options include: 
    -single melody generation (random or using source data) 
    -single chord generation (random or using source data) 
    -chord progression generation (random or using source data)
    -simple composition (1 random inst + pno) generation (random or using source data)
    -use composition mode (1 of 5 options) generation for more elaborate, automatically 
     generated pieces.
    '''
    
    # Create generator instance
    create = Generate()

    # Main loop
    going = True
    while(going):
        # Main menu 
        mainMenu()
        choice = int(input("Selection (0 - 5): "))
        # Error check...
        attempts = 0
        while choice > 5 or choice < 0 :
            print("try again bub")
            choice = int(input("Selection (0 - 4): "))
            attempts += 1
            if attempts > 9:
                print("\njust about had enough of yer shinanigans!")
                exit()

        # Exit
        if choice == 0:
            exit()

        # Generate melody
        elif choice == 1:
            print("\nCreate a new melody (1) from scratch, or use source data (2)?")
            c = int(input("Selection (1 or 2): "))
            # Error check...
            attempts = 0
            while c > 2 or c < 1:
                print("\ntry again bub\n")
                c = int(input("Selection (1 or 2): "))
                attempts += 1
                if attempts > 9:
                    print("\njust about had enough of yer shinanigans!")
                    exit()
            
            # From scratch
            if c == 1:
                tune = create.newMelody()
                if tune != -1:
                    create.displayMelody(tune)
                    print("\nEnjoy your new melody! :)\n")
                else:
                    print("\n:(\n")

            # Using supplied data
            elif c == 2:
                # List options
                dataMenu()
                d = int(input("Selection (1 - 5): "))
                # Error check...
                attempts = 0
                while d > 5 or d < 1 :
                    print("\ntry again bub\n")
                    d = int(input("Selection (1 - 5): "))
                    attempts+=1
                    if attempts > 9:
                        print("\nhad enough of your shenanigans!\n")
                        exit()

                # Random ints
                if d == 1:
                    data = newData(d)
                # Random floats
                elif d == 2:
                    data = newData(d)
                # Random chars/letters
                elif d == 3:
                    data = newData(d)
                # Random hex number
                elif d == 4:
                    data = newData(d)
                # user enters their name
                elif d == 5:
                    data = input("\nYour name: ")
                    d = 3

                # Generate melody
                tune = create.newMelody(data=data, dataType=d)
                if tune != -1:
                    create.displayMelody(tune)
                    print("\nEnjoy your new melody! :)\n")
                else:
                    print("\n:(\n")

        # Generate chord
        elif choice == 2:
            print("\nNew random chord (1) or from scale (2)?")
            c = int(input("Selection (1 or 2): "))
            # Error check...
            attempts = 0
            while c > 2 or c < 1:
                print("\ntry again bub\n")
                c = int(input("Selection (1 or 2): "))
                attempts += 1
                if(attempts > 9):
                    print("\njust about had enough of yer shinanigans!")
                    exit()

            # From scratch
            if c == 1:
                tempo = create.newTempo()
                chord = create.newChord(tempo=tempo) 
                if chord != -1:
                    create.displayChord(chord)
                else:
                    print("\n:(\n")

            # From scale
            elif c == 2:
                print("\nUse existing scale (1) or generate a new one (2)?")
                d = int(input("Selection (1 or 2): "))
                # Error check...
                attempts = 0
                while d > 2 or d < 1:
                    print("\ntry again bub\n")
                    d = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if attempts > 10:
                        print("\njust about had enough of yer shinanigans!")
                        exit()

                # Use existing scale
                if d == 1:
                    tempo = create.newTempo()
                    scale, data = create.pickScale(octave=randint(2, 5))
                    chord = create.newChord(tempo, scale)
                    chord.fn = data
                    if chord != -1:
                        create.displayChord(chord)
                    else:
                        print("\n:(\n")

                # Generate a new one
                elif d == 2:
                    tempo = create.newTempo()
                    scale, data = create.newScale(octave=randint(2, 5))
                    chord = create.newChord(tempo, scale)
                    chord.fn = data
                    if chord != -1:
                        create.displayChord(chord)
                    else:
                        print("\n:(\n")

        # Generate chord progression
        elif choice == 3:
            print("\nNew random chords (1) or from scale (2)?")
            c = int(input("Selection (1 or 2): "))
            # Error check...
            attempts = 0
            while c > 2 or c < 1:
                print("\ntry again bub\n")
                c = int(input("Selection (1 or 2): "))
                attempts += 1
                if attempts > 9:
                    print("\njust about had enough of yer shinanigans!")
                    exit()

            # From scratch
            if c == 1:
                total = int(input("How many? "))
                tempo = create.newTempo()
                scale, data = create.newScale(octave=randint(2, 5))
                chords = create.newProgression(total, tempo, scale)
                # append meta data to all chords
                for i in range(len(chords)):
                    chords[i].fn = data
                if len(chords) == 0:
                    print("\nERROR: unable to generate chords! :(\n")
                elif len(chords) != 0:
                    create.displayChords(chords)
                    
            # From scale
            elif c == 2:
                print("\nUse existing scale (1) or generate a new one (2)?")
                d = int(input("Selection (1 or 2): "))
                # Error check...
                attempts = 0
                while d > 2 or d < 1:
                    print("\ntry again bub\n")
                    d = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if(attempts > 9):
                        print("\njust about had enough of yer shinanigans!")
                        exit()

                # Use existing scale
                if d == 1:
                    tempo = create.newTempo()
                    scale, data = create.pickScale(octave=randint(2, 5))
                    if scale != -1:
                        chords = create.newChords(randint(3, len(scale)), tempo, scale)
                        # append meta data to all chords
                        for i in range(len(chords)):
                            chords[i].fn = data
                    else:
                        print("\nERROR: unable to pick scale! Exiting...")
                        break
                    if chords != -1:
                        create.displayChords(chords)
                    else:
                        print("\n:(\n")

                # Generate a new one
                elif d == 2:
                    tempo = create.newTempo()
                    scale, data = create.newScale(octave=4)
                    if scale != -1:
                        chords = create.newChords(randint(3, len(scale)),tempo, scale)
                        # append meta data to all chords
                        for i in range(len(chords)):
                            chords[i].fn = data
                    else:
                        print("\nERROR: unable to generate scale! Exiting...")
                        break
                    if chords != -1:
                        create.displayChords(chords)
                    else:
                        print("\n:(\n")                

        # Generate simple composition
        elif choice == 4:
            print("\nCreate a new composition (1) from scratch, or use source data (2)?")
            c = int(input("Selection (1 or 2): "))
            # Error check...
            attempts = 0
            while c > 2 or c < 1:
                print("\ntry again bub\n")
                c = int(input("Selection (1 or 2): "))
                attempts += 1
                if attempts > 9:
                    print("\njust about had enough of yer shinanigans!")
                    exit()
            
            # From scratch
            if c == 1:
                if create.newComposition() != -1:
                    print("\nEnjoy your new music! :)\n")
                else:
                    print("\n:(\n")

            # Using supplied data
            elif c == 2:
                # List options
                dataMenu()
                d = int(input("Selection (1 - 5): "))
                # Error check...
                attempts = 0
                while d > 5 or d < 1:
                    print("\ntry again bub\n")
                    d = int(input("Selection (1 - 5): "))
                    attempts += 1
                    if(attempts > 10):
                        print("\njust about had enough of yer shinanigans!")
                        exit()

                # Random ints
                if d == 1:
                    data = newData(d)
                # Random floats
                elif d == 2:
                    data = newData(d)
                # Random string
                elif d == 3:
                    data = newData(d)
                # Random hex number (string)
                elif d == 4:
                    data = newData(d)
                # user enters their name
                elif d == 5:
                    data = input("\nYour name: ")
                    d = 3

                # Generate composition
                if create.newComposition(data=data, dataType=d) != - 1:
                    print("\nEnjoy your new music! :)\n")
                else:
                    print("\n:(\n")

        # Comp modes
        elif choice == 5:
            modesMenu()
            m = int(input("Selection (0 - 4): "))
            # Error check...
            attempts = 0
            while m > 4 or m < 0:
                print("\ntry again bub\n")
                m = int(input("Selection (0 - 4): "))
                attempts += 1
                if attempts > 9:
                    print("\njust about had enough of yer shinanigans!")
                    exit()

            # Pure random
            if m == 0:
                if newRandomComposition() != -1:
                    print("\nEnjoy your new music! :)\n")
                else:
                    print("\n:(\n")
            # Tonal/modal
            elif m == 1:
                print("\nNot ready yet :(\n")
            # Atonal
            elif m == 2:
                print("\nNot ready yet :(\n")
            # Serialist
            elif m == 3:
                print("\nNot ready yet :(\n")
            # Minimalist
            elif m == 4:
                print("\nNot ready yet :(\n")

        # Again?
        going = keepGoing()

# Call it
run()