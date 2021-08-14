'''
This module handles text file generation for new compositions
'''

# Import
from datetime import datetime as date

# Generates a new .txt file to save a new composition's meta-data to
def saveInfo(self, name, data=None, fileName=None, newMelody=None, newChords=None, newMusic=None):
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
    header = '\n\n*****************************************************************'
    # f.write(header)
    f.write(f'./midi/{header}')
    header = '\n--------------------------NEW COMPOSITION------------------------'
    # f.write(header)
    f.write(f'./midi/{header}')
    header = '\n*****************************************************************'
    # f.write(header)
    f.write(f'./midi/{header}')

    #------------------------------Add Meta-Data---------------------------#

    # Add title, instrument(s), and save inputted data
    if name is not None and newMelody is not None:
        # Generate full title
        title = '\n\n\nTITLE: ' + name
        # f.write(title)
        f.write(f'./midi/{title}')

        # Add instrument
        instrument = '\n\nInstrument(s): ' + \
            newMelody.instrument + ' and piano'
        # f.write(instrument)
        f.write(f'./midi/{instrument}')

        # Add date and time.
        d = date.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = d.strftime("%d-%b-%y %H:%M:%S")
        dateStr = '\n\nDate: ' + dateStr
        # f.write(dateStr)
        f.write(f'./midi/{dateStr}')

    elif name is not None:
        # Generate title
        title = '\n\n\nTITLE: ' + name
        # f.write(title)
        f.write(f'./midi/{title}')

        # Add date and time.
        d = date.now()
        # convert to str d-m-y hh:mm:ss
        dateStr = d.strftime("%d-%b-%y %H:%M:%S")
        dateStr = '\n\nDate: ' + dateStr
        # f.write(dateStr)
        f.write(f'./midi/{dateStr}')

    # Add Forte number, if applicable
    if newMelody is not None and newMelody.fn != "":
        fn = ''.join(newMelody.fn)
        fnInfo = '\n\nForte Number: ' + fn
        # f.write(fnInfo)
        f.write(f'./midi/{fnInfo}')

    # Add original source data
    if data is not None:
        dataStr = ''.join([str(i) for i in data])
        dataInfo = '\n\nInputted data: ' + dataStr
        # f.write(dataInfo)
        f.write(f'./midi/{dataInfo}')
    else:
        dataInfo = '\n\nInputted data: None'
        # f.write(dataInfo)
        f.write(f'./midi/{dataInfo}')

    #-------------------------Add Melody and Harmony Info--------------------#

    # Save melody info
    if newMelody is not None:
        header = "\n\n\n----------------MELODY INFO-------------------"
        # f.write(header)
        f.write(f'./midi/{header}')

        tempo = '\n\nTempo: ' + str(newMelody.tempo) + 'bpm'
        # f.write(tempo)
        f.write(f'./midi/{tempo}')

        # Get totals and input
        totalNotes = '\n\nTotal Notes: ' + str(len(newMelody.notes))
        # f.write(totalNotes)
        f.write(f'./midi/{totalNotes}')

        noteStr = ', '.join(newMelody.notes)
        notes = '\n\nNotes: ' + noteStr
        # f.write(notes)
        f.write(f'./midi/{notes}')

        totalRhythms = '\n\nTotal rhythms:' + str(len(newMelody.rhythms))
        # f.write(totalRhythms)
        f.write(f'./midi/{totalRhythms}')

        rhythmStr = ', '.join([str(i) for i in newMelody.rhythms])
        rhythms = '\nRhythms: ' + rhythmStr
        # f.write(rhythms)
        f.write(f'./midi/{rhythms}')

        totalDynamics = '\n\nTotal dynamics: ' + \
            str(len(newMelody.dynamics))
        # f.write(totalDynamics)
        f.write(f'./midi/{totalDynamics}')

        dynamicStr = ', '.join([str(i) for i in newMelody.dynamics])
        dynamics = '\nDynamics: ' + dynamicStr
        # f.write(dynamics)
        f.write(f'./midi/{dynamics}')

    if newChords is not None:
        # Save harmony data
        header = "\n\n\n----------------HARMONY INFO-------------------"
        # f.write(header)
        f.write(f'./midi/{header}')

        # Get totals
        totalChords = '\n\nTotal chords: ' + str(len(newChords))
        # f.write(totalChords)
        f.write(f'./midi/{totalChords}')

        for j in range(len(newChords)):
            noteStr = ', '.join([str(i) for i in newChords[j].notes])
            notes = '\n\nNotes: ' + noteStr
            # f.write(notes)
            f.write(f'./midi/{notes}')

            rhythm = '\nRhythm: ' + str(newChords[j].rhythm)
            # f.write(rhythm)
            f.write(f'./midi/{rhythm}')

            dynamicsStr = ', '.join([str(i) for i in newChords[j].dynamics])
            dynamics = '\nDynamics: ' + dynamicsStr
            # f.write(dynamics)
            f.write(f'./midi/{dynamics}')

    # Input all
    if newMusic is not None:
        # Save composition data
        header = "\n\n\n----------------COMPOSITION INFO-------------------"
        # f.write(header)
        f.write(f'./midi/{header}')

        # Save global tempo
        tempo = '\n\nTempo: ' + str(newMusic.tempo) + 'bpm'
        # f.write(tempo)
        f.write(f'./midi/{tempo}')

        # Add melodies and harmonies
        for j in range(len(newMusic.melodies)):
            instStr = ', '.join(newMusic.instruments[j])
            inst = '\n\nInstruments: ' + instStr
            # f.write(inst)
            f.write(f'./midi/{inst}')

            noteStr = ', '.join(newMusic.melodies[j].notes)
            notes = '\n\nNotes: ' + noteStr
            # f.write(notes)
            f.write(f'./midi/{notes}')

            rhythmStr = ', '.join([str(i) for i in newMusic.melodies[j].rhythms])
            rhythms = '\n\nRhythms: ' + rhythmStr
            # f.write(rhythms)
            f.write(f'./midi/{rhythms}')

            dynamicStr = ', '.join([str(i) for i in newMusic.melodies[j].dynamics])
            dynamics = '\n\nDynamics:' + dynamicStr
            # f.write(dynamics)
            f.write(f'./midi/{dynamics}')

    # Close instance
    f.close()
    return 0