'''
----------------------------------------------------------------------------------------------------
                       THIS FILE IS FOR RUNNING THE PROGRAM IN THE TERMINAL

    User options include: 
        -single melody generation (random or using source data) 
        -single chord generation (random or using source data) 
        -chord progression generation (random or using source data)
        -composition (1 random inst + pno) generation (random or using source data)
        -run testing software

----------------------------------------------------------------------------------------------------
'''

# Imports
import test
from test import newData
from random import randint
from generate import generate

# Driver code class
class run():
    '''
    Class for executing generative functions in the terminal
    '''
    # Constructor
    def __init__(self) -> None:
        pass

    # Main menu
    def mainMenu(self):
        '''
        it's in the title
        '''
        print("\n")
        print("-------------------Main Menu-----------------")
        print("                                             ")
        print("   0. Exit                                   ")
        print("   1. New melody                             ")
        print("   2. New chord                              ")
        print("   3. New chord progression                  ")
        print("   4. New composition (1 melody + chords)    ")
        print("   5. Run testing software                   ")
        print("                                             ")
        print("---------------------------------------------")
        print("\n")

    # Data menu
    def dataMenu(self):
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

    # Test menu
    def testMenu(self):
        '''
        displays testing options
        '''
        print("\n")
        print("------------Testing options--------------")
        print("                                         ")
        print("          1. Run quick test              ")
        print("          2. Run all tests               ")
        print("                                         ")
        print("-----------------------------------------")
        print("\n")

    # Welcoming message
    def hello(self):
        '''
        what's up
        '''
        print("\n*~*~*~*~*~Let's make some music!~*~*~*~*~*~*~\n")

    # Exit message
    def goodBye(self):
        '''
        smell ya later, chump
        '''
        print("\n~~~~Have a nice day!~~~~\n\n")

    # Keep going?
    def keepGoing(self):
        '''
        Must we?
        '''
        answer = input("\nWant to do something else? y = yes, n = no\n")
        if(answer.isupper()):
            answer = answer.lower()
        if(answer == 'y'):
            return True
        else:
            return False

    # Driver code for using the generative functions in the terminal
    def start(self):
        '''
        Main driver code. 
        
        User options include: 
        -single melody generation (random or using source data) 
        -single chord generation (random or using source data) 
        -chord progression generation (random or using source data)
        -composition (1 random inst + pno) generation (random or using source data)
        -run testing software
        '''
        # Hello
        self.hello()
        
        # Create generator instance
        create = generate()

        # Main loop
        going = True
        while(going):
            # Main menu 
            self.mainMenu()
            choice = int(input("Selection (0 - 5): "))
            # Error check...
            attempts = 0
            while(choice > 5 or choice < 0):
                print("try again bub")
                choice = int(input("Selection (0 - 4): "))
                attempts += 1
                if(attempts > 9):
                    print("\njust about had enough of yer shinanigans!")
                    exit()

            # Exit
            if(choice == 0):
                self.goodBye()
                exit()

            # Generate melody
            if(choice == 1):
                print("\nCreate a new melody (1) from scratch, or use source data (2)?")
                c = int(input("Selection (1 or 2): "))
                # Error check...
                attempts = 0
                while(c > 2 or c < 1):
                    print("\ntry again bub\n")
                    c = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if(attempts > 9):
                        print("\njust about had enough of yer shinanigans!")
                        exit()
                
                # From scratch
                if(c == 1):
                    tune = create.newMelody()
                    if(tune != -1):
                        create.displayMelody(tune)
                        print("\nEnjoy your new melody! :)\n")
                    else:
                        print("RIP :(\n")

                # Using supplied data
                elif(c == 2):
                    # List options
                    self.dataMenu()
                    d = int(input("Selection (1 - 5): "))
                    # Error check...
                    attempts = 0
                    while(d > 5 or d < 1):
                        print("\ntry again bub\n")
                        d = int(input("Selection (1 - 5): "))
                        attempts+=1
                        if(attempts > 9):
                            print("\nhad enough of your shenanigans!\n")
                            exit()

                    # Random ints
                    if(d == 1):
                        data = newData(d)
                    # Random floats
                    elif(d == 2):
                        data = newData(d)
                    # Random chars/letters
                    elif(d == 3):
                        data = newData(d)
                    # Random hex number
                    elif(d == 4):
                        data = newData(d)
                    # user enters their name
                    elif(d == 5):
                        data = input("\nYour name: ")
                        d = 3

                    # Generate melody
                    tune = create.newMelody(data, d)
                    if(tune != -1):
                        create.displayMelody(tune)
                        print("\nEnjoy your new melody! :)\n")
                    else:
                        print("\n:(\n")

            # Generate chord
            elif(choice == 2):
                print("\nNew random chord (1) or from scale (2)?")
                c = int(input("Selection (1 or 2): "))
                # Error check...
                attempts = 0
                while(c > 2 or c < 1):
                    print("\ntry again bub\n")
                    c = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if(attempts > 9):
                        print("\njust about had enough of yer shinanigans!")
                        exit()

                # From scratch
                if(c == 1):
                    chord = create.newChord() 
                    if(chord != -1):
                        create.displayChord(chord)
                    else:
                        print("\n:(\n")

                # From scale
                elif(c == 2):
                    print("\nUse existing scale (1) or generate a new one (2)?")
                    d = int(input("Selection (1 or 2): "))
                    # Error check...
                    attempts = 0
                    while(d > 2 or d < 1):
                        print("\ntry again bub\n")
                        d = int(input("Selection (1 or 2): "))
                        attempts += 1
                        if(attempts > 10):
                            print("\njust about had enough of yer shinanigans!")
                            exit()

                    # Use existing scale
                    if(d == 1):
                        # Randomly decide between major or minor because why not
                        if(randint(1, 2) == 1):
                            scale = create.scales[randint(1, 12)]
                        else:
                            scale = create.scales[randint(1, 12)]
                            scale = create.convertToMinor(scale)
                        tempo = create.newTempo()
                        # chord = create.newChordFromScale(scale, tempo)
                        chord = create.newChord(tempo, scale)
                        if(chord != -1):
                            create.displayChord(chord)
                        else:
                            print("\nRIP :(\n")

                    # Generate a new one
                    elif(d == 2):
                        scale = create.newScale(octave=4)
                        tempo = create.newTempo()
                        # chord = create.newChordFromScale(scale, tempo)
                        chord = create.newChord(tempo, scale)
                        if(chord != -1):
                            create.displayChord(chord)
                        else:
                            print("\n:(\n")

            # Generate chord progression
            elif(choice == 3):
                print("\nNew random chords (1) or from scale (2)?")
                c = int(input("Selection (1 or 2): "))
                # Error check...
                attempts = 0
                while(c > 2 or c < 1):
                    print("\ntry again bub\n")
                    c = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if(attempts > 9):
                        print("\njust about had enough of yer shinanigans!")
                        exit()

                # From scratch
                if(c == 1):
                    total = int(input("How many? "))
                    tempo = create.newTempo()
                    scale = create.newScale()
                    # chords = create.newChords(total, tempo, None)
                    chords = create.newProgression(total, tempo, scale)
                    if(len(chords) == 0):
                        print("\nERROR: unable to generate chords! :(\n")
                    elif(len(chords) != 0):
                        create.displayChords(chords)
                        
                # From scale
                elif(c == 2):
                    print("\nUse existing scale (1) or generate a new one (2)?")
                    d = int(input("Selection (1 or 2): "))
                    # Error check...
                    attempts = 0
                    while(d > 2 or d < 1):
                        print("\ntry again bub\n")
                        d = int(input("Selection (1 or 2): "))
                        attempts += 1
                        if(attempts > 9):
                            print("\njust about had enough of yer shinanigans!")
                            exit()

                    # Use existing scale
                    if(d == 1):
                        tempo = create.newTempo()
                        # Randomly decide between major or minor because why not
                        if(randint(1, 2) == 1):
                            scale = create.scales[randint(1, 12)]
                        else:
                            scale = create.scales[randint(1, 12)]
                            scale = create.convertToMinor(scale)
                        chords = create.newChords(randint(3, len(scale)), tempo, scale)
                        if(chords != -1):
                            create.displayChords(chords)
                        else:
                            print("\n:(\n")

                    # Generate a new one
                    elif(d == 2):
                        tempo = create.newTempo()
                        scale = create.newScale(octave=4)
                        if(scale != -1):
                            chords = create.newChords(randint(3, len(scale)),tempo, scale)
                        else:
                            print("\nERROR: unable to generate scale! Exiting...")
                            break
                        if(chords != -1):
                            create.displayChords(chords)
                        else:
                            print("\n:(\n")                

            # Generate composition
            elif(choice == 4):
                print("\nCreate a new composition (1) from scratch, or use source data (2)?")
                c = int(input("Selection (1 or 2):"))
                # Error check...
                attempts = 0
                while(c > 2 or c < 1):
                    print("\ntry again bub\n")
                    c = int(input("Selection (1 or 2): "))
                    attempts += 1
                    if(attempts > 9):
                        print("\njust about had enough of yer shinanigans!")
                        exit()
                
                # From scratch
                if(c == 1):
                    if(create.newComposition() != -1):
                        print("\nEnjoy your new music! :)\n")
                    else:
                        print("\n:(\n")

                # Using supplied data
                elif(c == 2):
                    # List options
                    self.dataMenu()
                    d = int(input("Selection (1 - 5): "))
                    # Error check...
                    attempts = 0
                    while(d > 5 or d < 1):
                        print("\ntry again bub\n")
                        d = int(input("Selection (1 - 5): "))
                        attempts += 1
                        if(attempts > 10):
                            print("\njust about had enough of yer shinanigans!")
                            exit()

                    # Random ints
                    if(d == 1):
                        data = newData(d)
                    # Random floats
                    elif(d == 2):
                        data = newData(d)
                    # Random string
                    elif(d == 3):
                        data = newData(d)
                    # Random hex number (string)
                    elif(d == 4):
                        data = newData(d)
                    # user enters their name
                    elif(d == 5):
                        data = input("\nYour name: ")
                        d = 3

                    # Generate composition
                    if(create.newComposition(data, d) != - 1):
                        print("\nEnjoy your new music! :)\n")
                    else:
                        print("\n:(\n")
            
            # Run test suite
            elif(choice == 5):
                self.testMenu()
                t = int(input("Selection: "))
                # error check...
                attempts = 0
                while(t < 0 or t > 5):
                    print("\ntry again bub")
                    t = int(input("Selection:"))
                    attempts += 1
                    if(attempts > 10):
                        print("\njust about had it with yer shenanigans")
                        exit()

                # run quick test
                if(t == 1):
                    test.quickTest()

                # run full test
                if(t == 2):
                    test.runAll()

            # Again?
            going = self.keepGoing()

        # Exit message
        self.goodBye()
        return 0

#----------------------------Driver Code---------------------------#

# Run via terminal in the program's directory using 'python run.py'
run().start()