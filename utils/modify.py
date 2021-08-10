#********************************************************************************************************************#
#-------------------------------------This class handles MIDI file modification--------------------------------------#
#********************************************************************************************************************#
'''
Notes:

    Convert transposition list to list of values applicable to the MIDI file pitch
        - Look into what value is equivalent to a semi tone in MIDI
TODO:
    Implement methods to create an inversion, a retrogression, and an inverted retrogression
    of a given melody in a MIDI file

    Implement a method to repeat an entire section of music and append it to a given MIDI file

    Implement a method to take a given section of music and modify notes and rhythms at random (or
    with specified user input)

    Implement a method to add notes and rhythms to the end of the file. 

'''

#IMPORTS
import pretty_midi as pm
import midi as mid
from random import randint
from decisions import decide as choice
from generate import Generate as create


#------------------------------Transposition----------------------------#

#Transpose a given list of integers (PC's) by a specified value (+ or -)
def transpose(self, row, distance):
    '''
    Transposes a list of integers representing pitch-classes
    by n semi tones, where n is supplied by the user (must be 
    between -11 -> 11).

    Returns a list of modified ints or -1 if a failure occures.

    NOTE: "distance" should either be a single value between -11 to 11 (transpose
    up or down a within a span of a major seventh in semitones), or a list of 
    values between -11 and 11 (including 0!)
    '''
    if(not row):
        return None
    for i in range(len(row)):
        row[i] += distance
        if(row[i] > 11):
            create.octaveEquiv(row[i])
    return row

#Generates list of transposition distances
def transposeList(self, notesToModify):
    '''
    Generates list of transposition distances (-11 -> 11 in semitones).
    '''
    transpositions = []
    while(len(transpositions) < len(notesToModify)):
        transpositions.append(randint(-11, 11))
    return transpositions


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

    # Duplicate thisTune to alter data
    newVariant = thisTune
    
    # Create piano instance
    pianoProg = pm.instrument_name_to_program('Piano')
    piano = pm.Instrument(program = pianoProg)

    for i in range(len(notesToAdd)):
        # Retrieve the MIDI note number for the given list of notes
        noteNum = pm.note_name_to_number(notesToAdd[i])
        # Add notes, dynamics, and durations!
        # note = pretty_midi.Note(velocity = choice.howLoud(), pitch = noteNum, start = ???, end = ???)
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

