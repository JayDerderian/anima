''' 
Utility functions for working with MIDI I/O


NOTE: Double check the math for how strt and end are incremented according to
the supplied durations. Either Finale is doing something weird or the compounding
values are creating highly precice floating point numbers that might make sheet music
representation very messy. 
  
'''

# Imports
import urllib.request
import pretty_midi as pm
from random import randint
from datetime import datetime

# Autogenerates a new filename
def newFileName(ensemble):
    '''
    Generates a title/file name by picking two random words
    then attaching the composition type (solo, duo, ensemble, etc..),
    followed by the date.

    Format: "<words> - <type> - <date: d-m-y (hh:mm:ss)>"

    Random word generation technique from:
        https://stackoverflow.com/questions/18834636/random-word-generator-python
    '''
    try:
        # Get word list
        url = "https://www.mit.edu/~ecprice/wordlist.10000"
        # response = requests.get(url)
        response = urllib.request.urlopen(url)
        # words = response.content.splitlines()
        text = response.read().decode()
        words = text.splitlines()
        # Pick two random words
        name = words[randint(0, len(words) - 1)] + \
            '_' + words[randint(0, len(words) - 1)]
    except urllib.error.URLError:
        name = ensemble + ' - '

    # Get date and time.
    date = datetime.now()
    # Convert to str d-m-y (hh:mm:ss)
    dateStr = date.strftime("%d-%b-%y (%H:%M:%S.%f)")

    # Name and date, and add file extension
    fileName = '{}{}.mid'.format(name, dateStr)
    return fileName

# Outputs a single melody/instrument to a MIDI file
def saveMelody(fileName, newMelody):
    '''
    Outputs a single instrument MIDI file (ideally). Returns 0 on success, -1 on failure. 
    To be used with melody generation.
    '''
    # Check incoming data
    if newMelody.hasData() == False:
        return -1

    # Variables
    strt = 0
    end = 0

    # Create PM object and single instrument.
    # PM object is mainly used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=newMelody.tempo)
    instrument = pm.instrument_name_to_program(newMelody.instrument)
    melody = pm.Instrument(program=instrument)

    # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
    end += newMelody.rhythms[0]
    for i in range(len(newMelody.notes)):
        # Converts note name strings to MIDI note numbers
        note = pm.note_name_to_number(newMelody.notes[i])
        # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
        note = pm.Note(
            velocity=newMelody.dynamics[i], pitch=note, start=strt, end=end)
        # Then places container in melody notes list.
        melody.notes.append(note)
        # Increment rhythms (note event strt/end times)
        try:
            strt += newMelody.rhythms[i]
            end += newMelody.rhythms[i+1]
        except IndexError:
            break

    # Write out file from MIDI object
    mid.instruments.append(melody)
    mid.write(f'./midi/{fileName}')
    return 0

# Outputs a single MIDI chord.
def saveChord(newChord):
    '''
    Takes a single chord() object and outputs a MIDI file of that chord.
    '''
    # Create PrettyMIDI object
    mid = pm.PrettyMIDI(initial_tempo=newChord.tempo)
    # Create instrument object.
    instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
    chord = pm.Instrument(program=instrument)

    # Add data to pm object
    for i in range(len(newChord.notes)):
        note = pm.note_name_to_number(newChord.notes[i])
        note = pm.Note(
            velocity=newChord.dynamics[i], pitch=note, start=0.0, end=newChord.rhythm)
        chord.notes.append(note)

    # Write out file from MIDI object
    mid.instruments.append(chord)
    fileName = 'new-chord.mid'
    mid.write(f'./midi/{fileName}')
    print("\n'new-chord.mid' file saved!")
    return 0

# Generates a MIDI file of the chords created by newChord()
def saveChords(fileName, newChords):
    '''
    Takes a list of chord() objects as an argument and generates a MIDI file.
    '''
    # error checks
    if type(fileName) != str:
        print("\nsaveChords() - ERROR: fileName wrong type!")
        return -1
    # is this a list
    if type(newChords) != list:
        print("\nsaveChords() - ERROR: wrong data type inputted!")
        return -1
    # is this a list of chord objects with lists of note strings?
    for i in range(len(newChords)):
        # check *these* notes
        for j in range(len(newChords[i].notes)):
            if(type(newChords[i].notes[j]) != str):
                print("\nsaveChords() - ERROR: list does not contain note strings!")
                return -1

    # create PrettyMIDI object
    '''NOTE: takes tempo from first chord object''' 
    mid = pm.PrettyMIDI(initial_tempo=newChords[0].tempo)
    # Create instrument object.
    instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
    chord = pm.Instrument(program=instrument)

    # main loop
    strt = 0
    end = newChords[0].rhythm
    for i in range(len(newChords)):
        # Add *this* chord's notes
        for j in range(len(newChords[i].notes)):
            # Translate note to MIDI note
            note = pm.note_name_to_number(newChords[i].notes[j])
            achord = pm.Note(
                velocity=newChords[i].dynamics[j], pitch=note, start=strt, end=end)
            # Add to instrument object
            chord.notes.append(achord)
        try:
            # Increment strt/end times
            strt += newChords[i].rhythm
            end += newChords[i+1].rhythm
        except IndexError:
            break

    # Add chord to instrument list
    mid.instruments.append(chord)
    # Write out file from MIDI object
    mid.write(f'./midi/{fileName}')
    # print("\n'new-chords.mid' saved successfully!")
    return 0

# Save a melody and chords
def saveComposition(newMelody, newChords, fileName):
    '''
    Save a single-line melody with chords generated to a MIDI file. 
    Returns a PrettyMIDI() object, or -1 if failure
    '''
    # Check incoming data
    if newMelody.hasData() == False:
        return -1
    if len(newChords) == 0:
        return -1

    # Variables
    strt = 0
    end = 0

    # Create PM object PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=newMelody.tempo)

    # Create melody instrument
    instrument = pm.instrument_name_to_program(newMelody.instrument)
    melody = pm.Instrument(program=instrument)

    #----------------------------Add Melody----------------------------------#

    # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
    end += newMelody.rhythms[0]
    for i in range(len(newMelody.notes)):
        # Converts note name strings to MIDI note numbers
        note = pm.note_name_to_number(newMelody.notes[i])
        # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
        note = pm.Note(
            velocity=newMelody.dynamics[i], pitch=note, start=strt, end=end)
        # Then places container in melody notes list.
        melody.notes.append(note)
        # Increment rhythms (note event strt/end times)
        try:
            strt += newMelody.rhythms[i]
            end += newMelody.rhythms[i+1]
        except IndexError:
            break

    # Add melody to instrument list
    mid.instruments.append(melody)

    #----------------------------Add Harmonies-------------------------------#

    # Create instrument object.
    instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
    chord = pm.Instrument(program=instrument)

    strt = 0
    end = newChords[0].rhythm
    for i in range(len(newChords)):
        # Add *this* chord's notes
        for j in range(len(newChords[i].notes)):
            # Translate note to MIDI note
            note = pm.note_name_to_number(newChords[i].notes[j])
            achord = pm.Note(
                velocity=newChords[i].dynamics[j], pitch=note, start=strt, end=end)
            # Add to instrument object
            chord.notes.append(achord)
        try:
            # Increment strt/end times
            strt += newChords[i].rhythm
            end += newChords[i+1].rhythm
        except IndexError:
            break

    # Add chord to instrument list
    mid.instruments.append(chord)
    # Write to MIDI file
    mid.write(f'./midi/{fileName}')
    return mid

# exports a MIDI file for any sized composition (1 solo melody to ensemble sized n)
def save(comp):
    '''
    Exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
    Requires a composition() object.

    NOTE: This is outputting very cool minimalist style pieces, however it should probably
    be following the lists within the comp() object. 
    '''
    # Create PM object. PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=comp.tempo)

    # add melodies
    if len(comp.melodies) > 0:
        print("\nsaving melodies...")
        for i in range(len(comp.melodies)):
            strt = 0
            # end = comp.melodies[i].rhythms[i]
            end = comp.melodies[i].rhythms[0]
            # Create melody instrument
            instrument = pm.instrument_name_to_program(comp.melodies[i].instrument)
            melody = pm.Instrument(program=instrument)
            # Add *this* melody's notes
            for j in range(len(comp.melodies[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(comp.melodies[i].notes[j])
                anote = pm.Note(
                    velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
                # Add to instrument object
                melody.notes.append(anote)
                try:
                    # Increment strt/end times
                    strt += comp.melodies[i].rhythms[j]
                    end += comp.melodies[i].rhythms[j+1]
                except IndexError:
                    break
                
            # Add melody to instrument list
            mid.instruments.append(melody)

    # add chords
    if len(comp.chords) > 0:
        print("\nsaving chords...")
        for k in range(len(comp.chords)):
            strt = 0
            end = comp.chords[k].rhythm
            # Create instrument object.
            instrument = pm.instrument_name_to_program(comp.chords[k].instrument)
            chord = pm.Instrument(program=instrument)
            # Add *this* chord's notes
            for l in range(len(comp.chords[k].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(comp.chords[k].notes[l])
                anote = pm.Note(
                    velocity=comp.chords[k].dynamics[l], pitch=note, start=strt, end=end)
                # Add to instrument object
                chord.notes.append(anote)
            try:
                # Increment strt/end times
                strt += comp.chords[k].rhythm
                end += comp.chords[k+1].rhythm
            except IndexError:
                break

            # Add chord to instrument list
            mid.instruments.append(chord)

    # Write to MIDI file
    print("\nwriting MIDI file...")
    mid.write(f'./midi/{comp.midiFileName}')
    return 0

# exports a MIDI file in a quasi-minimalist style(!)
def saveMinimal(comp):
    '''
    Exports a MIDI file for any sized composition (1 solo melody to ensemble sized n). 
    Requires a composition() object.

    NOTE: This is outputting very cool minimalist style pieces!!
    '''
    # Create PM object. PM object is used to just write out the file.
    mid = pm.PrettyMIDI(initial_tempo=comp.tempo)

    # add melodies
    if len(comp.melodies) > 0:
        print("\nsaving melodies...")
        for i in range(len(comp.melodies)):
            strt = 0
            # end = comp.melodies[i].rhythms[i]
            end = comp.melodies[i].rhythms[0]
            # Create melody instrument
            instrument = pm.instrument_name_to_program(comp.melodies[i].instrument)
            melody = pm.Instrument(program=instrument)
            # Add *this* melody's notes
            for j in range(len(comp.melodies[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(comp.melodies[i].notes[j])
                anote = pm.Note(
                    velocity=comp.melodies[i].dynamics[j], pitch=note, start=strt, end=end)
                # Add to instrument object
                melody.notes.append(anote)
                try:
                    # Increment strt/end times
                    '''NOTE: should rhythms be using i or j?'''
                    strt += comp.melodies[i].rhythms[j]
                    end += comp.melodies[i].rhythms[j+1]
                except IndexError:
                    break
                
            # Add melody to instrument list
            mid.instruments.append(melody)

    # add chords
    if len(comp.chords) > 0:
        print("\nsaving chords...")
        for k in range(len(comp.chords)):
            strt = 0
            end = comp.chords[k].rhythm
            # Create instrument object.
            instrument = pm.instrument_name_to_program(comp.chords[k].instrument)
            chord = pm.Instrument(program=instrument)
            # Add *this* chord's notes
            for l in range(len(comp.chords[k].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(comp.chords[k].notes[l])
                anote = pm.Note(
                    velocity=comp.chords[k].dynamics[l], pitch=note, start=strt, end=end)
                # Add to instrument object
                chord.notes.append(anote)
            try:
                # Increment strt/end times
                strt += comp.chords[k].rhythm
                end += comp.chords[k+1].rhythm
            except IndexError:
                break

            # Add chord to instrument list
            mid.instruments.append(chord)

    # Write to MIDI file
    print("\nwriting MIDI file...")
    mid.write(f'./midi/{comp.midiFileName}')
    return 0