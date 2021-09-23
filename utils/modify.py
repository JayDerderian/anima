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

Other TODO's:

    basic scale or pitch class set(s) (can also accept arrays, i.e. groups of notes, which can be used as chords)

    order the notes will be played (allows free selection of any order of those notes, sequential or otherwise)

    basic rate at which this order is assessed, again, a list of values which define a 
    rhythm which itself can be further manipulated

    a separate rhythmically defined period of rests

    variable transposition, which can be defined rhythmically

    periodic permutation of things like note order (above), rest order, order of other functions in the program

    rhythmically defined retrograde/inversion functions of note order and other functions in the program

    rhythmic scaling of certain rhythmic functions (i.e. changing the rhythmic values in another function 
    by a certain factor, which can be constant or variably defined rhythmically)

    variable states of expansion (i.e. moving notes further apart from one another, pitch-wise)

    automatically generated chords based on defined pitch scale

    rhythmically defined variable selection of tension for chords in a progression

    ability to transpose a part to a new mode of a defined pitch scale

    variably defined root cycles for chords

    rhythmically controlled assignment of whatever note is being played to any number of instruments 
    (meaning if you want note 1 to be played by instrument 1 and note 2 and 3 to be played by 
    instrument 2 and so forth in that pattern)

'''

# IMPORTS
import mido as mid
import pretty_midi as pm
from utils.tools import transpose, oe
from random import randint, choice
from core.generate import Generate


# Add note(s) at end of MIDI file
'''
NOTE: Need a way to convert the duration list to start and end times for
      the pretty_midi.Note(velocity, pitch, start, end) input function

      Might need a way to convert standard durations to floats based on the given
      tempo of the original track. Look into how to convert sets of durations into 
      durations, then convert that duration to start/end times. 

      Might also need to create a decision function for velocities (dynamics)

NOTE: input a composition() object with the additional note and rhythm data to be 
      appended at the end a MIDI file 
'''
def addNotes(notesToAdd, thisTune):

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

'''
#Augments OR Diminishes SELECTED rhythms (measured in seconds) with a given tempo.
def modifyTime(self, rhythm, tempo, thisTune):
    second = 60 #60bpm
    
    Find duration from note data's start/end times. (end-start)
    Modify duration by x amount to augment/diminish
    x = tuneTune's tempo/second. 
    
    
    #scale = tempo/second
    #newDuration = rhythm * scale
    return newDuration
'''


#Augment AND Diminish ALL rhythm(s)
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
'''


