#********************************************************************************************************************#
#-------------------------------------This class handles MIDI file modification--------------------------------------#
#********************************************************************************************************************#
'''
Notes:

    Convert transposition list to list of values applicable to the MIDI file pitch
        - Look into what value is equivalent to a semi tone in MIDI

'''

#IMPORTS
import pretty_midi
import midi as mid
from analyze import analysis
from decisions import decide as choice
from generate import generate as create

class modification(create):
    '''
    This class handles modification functions. Most functions here will export a modified
    list or pretty_midi object which will be written out using the .write() function built into
    prett_midi's library.
    '''

    def __init__(self):
        super().__init__()


    #------------------------------Transposition----------------------------#

    #Transpose a given list of integers (PC's) by a specified value (+ or -)
    def transpose(self, row, distance):
        '''
        Transpose a given list of integers (PC's) by a specified value (+ or -)
        '''
        if(not row):
            return None
        i = 0
        while (i < len(row)):
            row[i] += distance
            if(row[i] > 12):
                create.octaveEquiv(row[i])
            elif(row[i] < 0):
                while(row[i] < 0 and row[i] < 12):
                    row[i] += 12
            i += 1
        return row

    #Generates list of transposition distances
    def transposeList(self, notesToModify):
        '''
        Generates list of transposition distances (0 - 11).
        '''
        n = 0
        transpositions = []
        print("\nGenerating transpositions...")
        while(n < len(notesToModify)):
            transpositions.append(choice.distance(self))
            n += 1
        #Test outputs
        if(not transpositions):
            print("...Unable to generate transposition list!")
        print("Transpositions: ", transpositions)
        return transpositions

    #Transpose all notes UP by x distance
    def transposeUP(self, transpositions, thisTune):
        '''
        Transpose all notes UP by a series of +n distances
        '''
        if(not transpositions or not thisTune):
            return None
        newVariant = thisTune
        #newVariant = pretty_midi.PrettyMIDI() - create a PrettyMIDI object
        for instrument in newVariant.instruments:
            for note in instrument.notes:
                note.pitch += transpositions[note]
        return newVariant

    #Transpose all notes DOWN by x distance
    def transposeDOWN(self, transpositions, thisTune):
        '''
        Transpose all notes DOWN by a series of -n distances
        '''
        if(not transpositions or not thisTune):
            return None
        newVariant = thisTune
        #newVariant = pretty_midi.PrettyMIDI() - create a PrettyMIDI object
        for instrument in  newVariant.instruments:
            for note in instrument.notes:
                note.pitch -= transpositions[note]
        return newVariant

    #Transpose all notes UP OR DOWN by x distance
    def transposeUpAndDown(self, transpositions, thisTune):
        '''
        Transpose all notes UP OR DOWN by a series of +/- n distances
        '''
        if(not transpositions or not thisTune):
            return None
        newVariant = thisTune
        #newVariant = pretty_midi.PrettyMIDI() - create a PrettyMIDI object
        for instrument in newVariant.instruments:
            for note in instrument.notes:
                if(choice.upOrDown(self) == 1):
                    note.pitch += transpositions[note]
                note.pitch -= transpositions[note]
        return newVariant


    #-------------------------------------Tempo---------------------------------------#


    #Converts the values in a duration list proportionally to an inputted tempo
    def tempoConvert(self, tempo, rhythms):
        '''
        Converts the values in a duration list proportionally to an inputted tempo
        '''
        print("\nConverting durations...")
        if(not rhythms):
            print("...No duration list inputted!")
        i = 0
        conversion = tempo/60
        while(i < len(rhythms)):
            rhythms[i] *= conversion
            i += 1
        if(not rhythms):
            print("...Unable to convert durations!")
        print("New durations:", rhythms)
        return rhythms
        

    #--------------------------------------Notes--------------------------------------#


    #Add note(s) at end of MIDI file
    '''
    Note: 
        Need a way to convert the duration list to start and end times for
        the pretty_midi.Note(velocity, pitch, start, end) input function

        Might need a way to convert standard durations to floats based on the given
        tempo of the original track. Look into how to convert sets of durations into 
        durations, then convert that duration to start/end times. 

        Might also need to create a decision function for velocities (dynamics)
        '''
    def addNotes(self, notesToAdd, thisTune):
        if(not notesToAdd or not thisTune):
            return None

        #--Duplicate thisTune to alter data--#
        newVariant = thisTune
       
        #--Create piano instance--#
        #newVariant = pretty_midi.PrettyMIDI() #create a PrettyMIDI object
        pianoProg = pretty_midi.instrument_name_to_program('Piano')
        piano = pretty_midi.Instrument(program = pianoProg)

        for i in range(len(notesToAdd)):

            #--Retrieve the MIDI note number for the given list of notes--#
            noteNum = pretty_midi.note_name_to_number(notesToAdd[i])

            #--Add notes, dynamics, and durations!---#
            #note = pretty_midi.Note(velocity = choice.howLoud(), pitch = noteNum, start = ???, end = ???)
            newVariant.append(piano)

        #Note: use newVariant.write('new_variant.mid') in main to save file
        return newVariant

    #Remove note(s)
    '''
    Note:
        This will need to modify rythms by a certain percentage. If the original
        duration is starting at 0.2345 and finishing at 0.3456, then the latter number
        will need to be modified according to our specification. If the original note
        is an "eighth" note, and we want to change it to a quarter note, then the duration
        will need to be increased by 100% (doubled). The same applies to diminishing the 
        rhythms.
    '''
    
    #Augment AND Diminish rhythm(s)
    '''
    #Determine start/end times for notes.
    def alterDurations(self, thisTune, noteData, newDurations):
        scale = tools.tempoDifference(analysis.getGlobalTempo(thisTune))
        selection = math.floor(5 * random.random())
        duration = choice.newDuration(self)
        
        #Double value
        if(selection == 1):
            noteDuration *= 2
            thisTune.instrument[i].note[transpositions[x]].end * 2]
            thisTune.instrument[i].note[transpositions[x + 1]].start * 2]

            noteData[Note[selected note index][velocity, pitch, start, end * 2]
            noteData[Note[selected note index + 1][velocity, pitch, start * 2, end]

        #Add a dot (Augment by 50%)
        elif(selection == 3):
            temp = noteDuration *= 0.5
            noteDuration = noteDuration + temp

        #Diminish by 50%
        elif(selection == 3):
            noteDuration *= 0.5
            noteData[Note[selected note index][velocity, pitch, start, end * 0.5]
            noteData[Note[selected note index + 1][velocity, pitch, start * 0.5, end]

        #Diminish by 75%
        elif(selection == 4):
            noteDuration *= 0.25
            noteData[Note[selected note index][velocity, pitch, start, end * 0.25]
            noteData[Note[selected note index + 1][velocity, pitch, start * 0.25, end]

        #If in a loop to generate start/end times:
            start = 0
            for
                #end = start + noteDuration
                #start = end
                #(repeat as necessary)


    #Augments/Diminishes rhythms (measured in seconds) with a given tempo.
    def modifyTime(self, rhythm, tempo, thisTune):
        second = 60 #60bpm
        
        Find duration from note data's start/end times. (end-start)
        Modify duration by x amount to augment/diminish
        x = tuneTune's tempo/second. 
        
        
        #scale = tempo/second
        #newDuration = rhythm * scale
        return newDuration
    '''

