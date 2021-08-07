
'''
Convert composition data to ABC notation
Code by Eric Dale originally for BrainStorm
'''

def abc(title, tempo, tune, chords):

    melody = ''
    for note, rhythm in zip(tune.notes, tune.rhythms):
        melody += note_to_abc(note, rhythm)

    harmony = ''
    for i in range(len(chords)):
        chord = ''
        for note in chords[i].notes:
            chord += note_to_abc(note, chords[i].rhythm)
        harmony += '[' + chord + ']'

    song = (
        f"T:{title.title()}\n"
        f"Q:{tempo}\n"
        f"V:1\n{melody}|]\n"
        f"V:2\n{harmony}|]]\n"
    )

    return song


def note_to_abc(note, rhythm):
    abc_note = ''

    if len(note) == 2:
        idx = 1
    else:
        idx = 2

    if note[idx] == '2':
        abc_note += note[0] + ',,'
    elif note[idx] == '3':
        abc_note += note[0] + ','
    elif note[idx] == '4':
        abc_note += note[0]
    elif note[idx] == '5':
        abc_note += note[0].lower()
    elif note[idx] == '6':
        abc_note += note[0].lower() + "'"

    if idx == 2:
        if note[1] == '#':
            abc_note = '^' + abc_note
        elif note[1] == 'b':
            abc_note = '_' + abc_note

    if rhythm == 4.0:
        abc_note += '4'
    elif rhythm == 3.0:
        abc_note += '3'
    elif rhythm == 2.0:
        abc_note += '2'
    elif rhythm == 1.5:
        abc_note += '3/2'
    elif rhythm == 0.75:
        abc_note += '3/4'
    elif rhythm == 0.5:
        abc_note += '/2'
    elif rhythm == 0.375:
        abc_note += '3/8'
    elif rhythm == 0.25:
        abc_note += '/4'
    elif rhythm == 0.125:
        abc_note += '/8'

    return abc_note

    '''
        Durations in seconds (1 = quarter note (60bpm))
        Whole note to 32nd note

            [0] 4 = whole note                                                          
            [1] 3 = dotted half
            [2] 2 = half note           
            [3] 1.5 = dotted quarter    
            [4] 1 = quarter             
            [5] 0.75 = dotted eighth
            [6] 0.5 = eighth
            [7] 0.375 = dotted sixteenth
            [8] 0.25 = sixteenth 
            [9] 0.125 = thirty-second
        '''
