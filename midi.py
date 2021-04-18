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
        if(newMelody.notes is None 
            or newMelody.rhythms is None 
            or newMelody.dynamics is None 
            or newMelody.tempo == 0.0):
            return -1

        # Variables
        i = 0
        strt = 0
        end = 0

        # Create PM object and single instrument. 
        # PM object is mainly used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo = newMelody.tempo)
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        '''
        Randomly choose an instrument? 
        instrument = pm.instrument_name_to_program(inst.INSTRUMENT_MAP[randint(0, 110))'''
        melody = pm.Instrument(program = instrument)

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        while(i < len(newMelody.rhythms)):
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
                i += 1
            except IndexError:
                break  

        # Write out file from MIDI object
        mid.instruments.append(melody)
        mid.write('test-melody.mid')

        return 0


    # Outputs a single MIDI chord.
    def saveChord(self, newchord, dynamics):
        '''
        Outputs a single MIDI chord (ideally). Also returns a pretty_midi object. 
        To be used with chord generation.
        
        Defaults:
            Instrument: Piano
            Tempo: 120
            Velocity: 100
        '''
        if(not newchord or not dynamics):
            return -1

        i = 0
        strt = 0.0
        end = 2.0

        # Create instrument/MIDI object
        aNewChord = pm.PrettyMIDI(initial_tempo=60)
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program = instrument)

        # Add data to pm object
        while(i < len(newchord)):
            note = pm.note_name_to_number(newchord[i])
            note = pm.Note(velocity= dynamics[i], pitch= note, start= strt, end= end)
            chord.notes.append(note)
            i += 1
        
        # Write out file from MIDI object
        aNewChord.instruments.append(chord)
        aNewChord.write('test-chord.mid')

        return 0


    # Generates a MIDI file of the chords created by newChord()
    def chordsMIDI(self, newChords):
        '''
        Generates a MIDI file of the chords created by newChord()

        NOTE: Not ready. 
            
            Still need to find a way to iterate through individual
            chords in newChords while assigning the same duration to each note
            in the chord before progressing to the next associated set of dynamics
            and chords.

            Example input:
            newChords = [['C#2','Db6', 'B4'],['','','','','','','','',],['','','','']...,n]

            i = 0: first subarray in newChords[]
            i = 1: second sub-array ""
            etc...

            i < newChords(len(i)) ??? 
            Need to iterate for the length of each individual sub-arrays.

            strt = 0
            end = rhythms[0]
            for i in range(len(rhythms)):
                for j in newChords[i[j]]:
                    note_number = pm.note_name_to_number(note_name)
                    note = pm.Note(velocity= vel, pitch= note_number, start= strt, end= end)
                    chords.notes.append(note)
                strt += end
                end += rhythms[i]

            Add returning object from newChord as an argument?
        '''

        print("\nGenerating MIDI chords...")

        # Variables and stuff
        i = 0
        dur = 4.0
        strt = 0.0
        end = 4.0
        vel = 60
        
        # Create instrument
        myChords = pm.PrettyMIDI(initial_tempo = 60)
        chordProgram = pm.instrument_name_to_program('Acoustic Grand Piano')
        chords = pm.Instrument(program = chordProgram)

        # Generate chords and append to MIDI object
        '''
        Note: Confirm whether a pm.Instrument.notes list 
              can function as a list of lists.
        '''
        while(i < len(newChords)):
            for note_name in newChords[i]:
                note_number = pm.note_name_to_number(note_name)
                note = pm.Note(velocity= vel, pitch= note_number, start= strt, end= end)
                chords.notes.append(note)
                strt += dur
                end += dur
            i += 1

        # Write out file from MIDI object
        myChords.instruments.append(chords)
        myChords.write('test-chords.mid')

        return myChords