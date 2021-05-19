#*******************************************************************************************************#
#-----------------------------Utility functions for working with MIDI I/O ------------------------------#
#*******************************************************************************************************#

'''
    This module is for handling MIDI I/O with generous help from the pretty_midi library.
    There may be other misc functions here too at some point.


'''
import pretty_midi as pm
from pretty_midi import constants as inst

class midiStuff():
    '''
    This class is for handling MIDI I/O with generous help from the pretty_midi library.
    There may be other misc functions here too at some point.
    '''

    def __init__(self):
        super().__init__()

    # Imports a MIDI file
    def load(self, fileName):
        '''
        Imports a MIDI file from a given file name or path.
        Returns a PrettyMIDI object using the given filename.
        '''
        print("\nImporting MIDI file...")
        # Import file
        thisTune = pm.PrettyMIDI(fileName) 
        if(not thisTune):
            print("...Unable to import file!")
            return -1
        print("...File imported!")
        return thisTune


    # Save a MIDI object to a pre-existing file
    # def saveCurrent(self, fileName, notes, rhythms, dynamics, tempo, instTotal)
    '''
    Saves a MIDI object to a pre-existing MIDI file. Input must be a 
    string with the format 'filename.mid'
    '''
    def save(self, fileName):
        if(fileName is None):
            return -1
        print("\nSaving file...")
        pm.PrettyMIDI.write(fileName)
        return 0
    
    # Outputs a single melody/instrument to a MIDI file
    def saveMelody(self, newMelody):
        '''
        Outputs a single instrument MIDI file (ideally). Returns 0 on success, -1 on failure. 
        To be used with melody generation.

        NOTE: Double check the math for how strt and end are incremented according to
        the supplied durations. Either Finale is doing something weird or the compounding
        values are creating highly precice floating point numbers that might make sheet music
        representation very messy. 
        '''
        # Check incoming data
        if(newMelody.hasData() == False):
            return -1

        # Variables
        strt = 0
        end = 0

        # Create PM object and single instrument. 
        # PM object is mainly used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo = newMelody.tempo)
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        '''
        Randomly choose an instrument? 
        instrument = pm.instrument_name_to_program(inst.INSTRUMENT_MAP[randint(0, 110))
        '''
        melody = pm.Instrument(program = instrument)

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        for i in range(len(newMelody.notes)):
            # Converts note name strings to MIDI note numbers
            note = pm.note_name_to_number(newMelody.notes[i])
            # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
            note = pm.Note(velocity= newMelody.dynamics[i], pitch= note, start= strt, end= end)
            # Then places container in melody notes list.
            melody.notes.append(note)
            # Increment rhythms (note event strt/end times)
            try:
                strt += newMelody.rhythms[i]
                end += newMelody.rhythms[i + 1]
            except IndexError:
                break  

        # Write out file from MIDI object
        mid.instruments.append(melody)
        # print("saving", fileName, "...")
        # mid.write(fileName)
        mid.write('new-melody.mid')
        return 0


    # Outputs a single MIDI chord.
    def saveChord(self, newChord):
        '''
        Outputs a single MIDI chord (ideally). Also returns a pretty_midi object. 
        To be used with chord generation.
        '''
        print("\nSaving chord...")

        # Create PrettyMIDI object
        mid = pm.PrettyMIDI(initial_tempo=60)
        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program = instrument)

        print("Created instrument:", 'Acoustic Grand Piano')

        # Add data to pm object
        for i in range(len(newChord.notes)):
            note = pm.note_name_to_number(newChord.notes[i])
            note = pm.Note(velocity= newChord.dynamics[i], pitch= note, start= 0.0, end= newChord.rhythm)
            chord.notes.append(note)
        
        # Write out file from MIDI object
        mid.instruments.append(chord)
        mid.write('new-chord.mid')
        print("'new-chord.mid' file saved!")
        return 0


    # Generates a MIDI file of the chords created by newChord()
    def saveChords(self, newChords):
        '''
        Takes a chord() object as an argument and generates a MIDI file.
        Returns a pretty_midi object. Returns 0.

        NOTE: Currently creates a separate track for EACH chord. Need to find a way
              to get them all onto one track.
        '''

        print("\nGenerating MIDI chords...")
        
        # Create PrettyMIDI object
        myChords = pm.PrettyMIDI(initial_tempo = 60)

        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program = instrument)

        strt = 0
        end = newChords[0].rhythm
        for i in range(len(newChords)):
            # Add *this* chord's notes
            for j in range(len(newChords[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(newChords[i].notes[j])
                note = pm.Note(velocity= newChords[i].dynamics[j], pitch= note, start= strt, end= end)
                # Add to instrument object
                chord.notes.append(note)
            try:
                # Increment strt/end times
                strt += newChords[i].rhythm
                end += newChords[i + 1].rhythm
            except IndexError:
                break

        # Add chord to instrument list 
        myChords.instruments.append(chord)

        # Write out file from MIDI object
        myChords.write('new-chords.mid')
        print("'new-chords' saved successfully!")
        return 0


    # Save a melody and chords
    def saveComposition(self, newMelody, newChords):
        '''
        Save a single-line melody with chords generated from that melody
        to a MIDI file. Returns -1 upon failure.
        '''
        # Check incoming data
        if(newMelody.hasData() == False):
            return -1
        if(len(newChords) == 0):
            return -1

        # Variables
        strt = 0
        end = 0

        # Create PM object PM object is used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo = newMelody.tempo)

        # Create melody instrument (strings)
        instrument = pm.instrument_name_to_program('Synth Strings 1')
        melody = pm.Instrument(program = instrument)

        #----------------------------Add Melody----------------------------------#

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        for i in range(len(newMelody.notes)):
            # Converts note name strings to MIDI note numbers
            note = pm.note_name_to_number(newMelody.notes[i])
            # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
            note = pm.Note(velocity= newMelody.dynamics[i], pitch= note, start= strt, end= end)
            # Then places container in melody notes list.
            melody.notes.append(note)
            # Increment rhythms (note event strt/end times)
            try:
                strt += newMelody.rhythms[i]
                end += newMelody.rhythms[i + 1]
            except IndexError:
                break  

        # Add melody to instrument list
        mid.instruments.append(melody)

        #-----------------------------Add Chords---------------------------------#

        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program = instrument)
        for i in range(len(newChords)):
            # Add *this* chord's notes
            for j in range(len(newChords[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(newChords[i].notes[j])
                note = pm.Note(velocity= newChords[i].dynamics[j], pitch= note, start= strt, end= end)
                # Add to instrument object
                chord.notes.append(note)
            # Add chord to instrument list 
            mid.instruments.append(chord)
            try:
                # Increment strt/end times
                strt += newChords[i].rhythm
                end += newChords[i + 1].rhythm
            except IndexError:
                break


        # mid.write(fileName)
        mid.write('new-composition.mid')
        return 0