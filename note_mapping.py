import input_codes.input_manager

def to_note(letter, octave, delay=0.05):
    letter_code = {
        'C' : 0,
        'C#' : 1,
        'Db':1,
        'D' : 2,
        'D#': 3,
        'Eb':3,
        'E': 4,
        'Fb':5,
        'F':5,
        'F#':6,
        'Gb':6,
        'G':7,
        'G#':8,
        'Ab':8,
        'A':9,
        'A#':10,
        'Bb':10,
        'B':11,
        'B#':12
    }
    return 60 + 12 * octave + letter_code[letter]

def append_volume(volume, stick_notes):
    for all_notes in stick_notes.keys():
        for k in range(len(stick_notes[all_notes])):
            stick_notes[all_notes][k].append(volume)

RS_V = 112 # Right stick volume.
RS_AV = 112 # Left stick accompanying volume.
RIGHT_STICK_NOTES = {
    "3": [['D', 1]],
    "4": [['E', 1]],
    "5": [['F', 1]],
    "0": [['G', 1]],
    "1": [['A', 1]],
    "2": [['Bb', 1]]
}
RIGHT_STICK_COMPANY = {
    "3": [['F', 1]],
    "4": [['G', 1]],
    "5": [['A', 1]],
    "0": [['Bb', 1]],
    "1": [['C', 2]],
    "2": [['D', 2]]
}

append_volume(RS_V, RIGHT_STICK_NOTES)
append_volume(RS_AV, RIGHT_STICK_COMPANY)

LSV = 112 # Left stick volume.
LS_AV = 112 # Left stick accompanying volume.
LEFT_STICK_NOTES = {#str[n]:[] for n in range[6]}
    "3": [['D', -1], ['A', -1], ['F', 0]],
    "4": [['F', -1], ['C', 0], ['G', 0], ['A', 0]],
    "5": [['G', -1], ['D', 0], ['A', 0]],
    "0": [['A', -1], ['E', 0], ['C#', 0]],
    "1": [['A#', -1], ['F', 0], ['D', 0]],
    "2": [['C', 0], ['G', 0], ['E', 0]],
}
LEFT_STICK_COMPANY = {
    "3": [['D', -2], ['D', -3]],
    "4": [['F', -3], ['F', -2]],
    "5": [['G', -3], ['G', -2]],
    "0": [['A', -3], ['A', -2]],
    "1": [['A#', -3], ['A#', -2]],
    "2": [['C', -2], ['C', -1]],
}

append_volume(LSV, LEFT_STICK_NOTES)
append_volume(LSV, LEFT_STICK_COMPANY)