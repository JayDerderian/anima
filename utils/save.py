'''
This module handles text file generation for new compositions. 

NOTE: Figure out a way for this method to generate a folder called "midi" if it doesn't already
exist. If not, create it and write .txt file there, otherwise just write it to there.

Also see if we can reduce the number of times f.write() is called. It seems like... a lot, in 
it's current state.
'''

# Import
import os
import sys
from datetime import datetime as date

# Generates a new .txt file to save a new composition's meta-data to
def saveInfo(name, data=None, fileName=None, newMelody=None, newChords=None, newMusic=None):
    '''
    Generates a new .txt file to save a new composition's data and meta-data to. 
    Can take a melody() object, a list of chord() objects, or a composition() object as arguments. 
    '''
    # Create a new file opening object thing
    try:
        f = open(fileName, 'w')
    except PermissionError:
        name = name + '.txt'
        f = open(name, 'w')

    # Generate a header
    f.write('\n\n*****************************************************************')
    f.write('\n--------------------------NEW COMPOSITION------------------------')
    f.write('\n*****************************************************************')

    #------------------------------Add Meta-Data---------------------------#

    # Add title, instrument(s), and save inputted data
    if name is not None and newMelody is not None:
        # Generate full title
        f.write('\n\n\nTITLE: ' + name)

        # Add instrument
        instrument = '\n\nInstrument(s): ' + \
            newMelody.instrument + ' and piano'
        f.write(instrument)

        # Add date and time.
        d = date.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = d.strftime("%d-%b-%y %H:%M:%S")
        dateStr = '\n\nDate: ' + dateStr
        f.write(dateStr)

    elif name is not None:
        # Generate title
        f.write('\n\n\nTITLE: ' + name)

        # Add date and time.
        d = date.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = d.strftime("%d-%b-%y %H:%M:%S")
        dateStr = '\n\nDate: ' + dateStr
        f.write(dateStr)

    # Add Forte number, if applicable
    if newMelody is not None and newMelody.fn != "":
        '''NOTE: this is a bandaid. Make sure only strings get here!!!'''
        if type(newMelody.fn) == list:
            newMelody.fn = str(newMelody.fn)
        fn = ''.join(newMelody.fn)
        fnInfo = '\n\nForte Number or pitch class set: ' + fn
        f.write(fnInfo)

    # Add original source data
    if data is not None:
        dataStr = ''.join([str(i) for i in data])
        dataInfo = '\n\nInputted data: ' + dataStr
        f.write(dataInfo)

    else:
        f.write('\n\nInputted data: None')

    #-------------------------Add Melody and Harmony Info--------------------#

    # Save melody info
    if newMelody is not None:
        f.write("\n\n\n----------------MELODY INFO-------------------")

        # add tempo
        f.write('\n\nTempo: ' + str(newMelody.tempo) + 'bpm')

        # Get totals and input
        totalNotes = '\n\nTotal Notes: ' + str(len(newMelody.notes))
        f.write(totalNotes)

        noteStr = ', '.join(newMelody.notes)
        notes = '\n\nNotes: ' + noteStr
        f.write(notes)

        f.write('\n\nTotal rhythms:' + str(len(newMelody.rhythms)))

        rhythmStr = ', '.join([str(i) for i in newMelody.rhythms])
        rhythms = '\nRhythms: ' + rhythmStr
        f.write(rhythms)

        totalDynamics = '\n\nTotal dynamics: ' + \
            str(len(newMelody.dynamics))
        f.write(totalDynamics)

        dynamicStr = ', '.join([str(i) for i in newMelody.dynamics])
        dynamics = '\nDynamics: ' + dynamicStr
        f.write(dynamics)

    if newChords is not None:
        # Save harmony data
        f.write("\n\n\n----------------HARMONY INFO-------------------")

        # Get totals
        totalChords = '\n\nTotal chords: ' + str(len(newChords))
        f.write(totalChords)

        for j in range(len(newChords)):
            noteStr = ', '.join([str(i) for i in newChords[j].notes])
            notes = '\n\nNotes: ' + noteStr
            f.write(notes)

            rhythm = '\nRhythm: ' + str(newChords[j].rhythm)
            f.write(rhythm)

            dynamicsStr = ', '.join([str(i) for i in newChords[j].dynamics])
            dynamics = '\nDynamics: ' + dynamicsStr
            f.write(dynamics)

    # Input all
    if newMusic is not None:
        # Save composition data
        f.write("\n\n\n----------------COMPOSITION INFO-------------------")

        # Save global tempo
        f.write('\n\nTempo: ' + str(newMusic.tempo) + 'bpm')

        # Add melodies and harmonies
        for j in range(len(newMusic.melodies)):
            instStr = ', '.join(newMusic.instruments[j])
            inst = '\n\nInstruments: ' + instStr
            f.write(inst)

            noteStr = ', '.join(newMusic.melodies[j].notes)
            notes = '\n\nNotes: ' + noteStr
            f.write(notes)

            rhythmStr = ', '.join([str(i) for i in newMusic.melodies[j].rhythms])
            rhythms = '\n\nRhythms: ' + rhythmStr
            f.write(rhythms)

            dynamicStr = ', '.join([str(i) for i in newMusic.melodies[j].dynamics])
            dynamics = '\n\nDynamics:' + dynamicStr
            f.write(dynamics)

    # Close instance
    f.close()