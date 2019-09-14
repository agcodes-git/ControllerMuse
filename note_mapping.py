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
RS_O = 0
RIGHT_STICK_NOTES = {
    "2": [['A', RS_O + 0]],
    "3": [['B', RS_O + 0]],
    "0": [['C', RS_O + 1]],
    "1": [['E', RS_O + 1]],
}
RIGHT_STICK_COMPANY = {
    "2": [['C', RS_O + 1]],
    "3": [['D', RS_O + 1]],
    "0": [['G', RS_O + 1]],
    "1": [['A', RS_O + 1]],
}

append_volume(RS_V, RIGHT_STICK_NOTES)
append_volume(RS_AV, RIGHT_STICK_COMPANY)

LSV = 112 # Left stick volume.
LS_AV = 112 # Left stick accompanying volume.

LEFT_STICK_NOTES = {#str[n]:[] for n in range[6]}

        #RL

        # The identity. Should sound like home.
        "22": [['A', -2], ['E', -1], ['C', 0]],
        "33": [['C', -1], ['G', 0], ['E', 0] ],
        "00": [['F', -2], ['C', -1], ['A', -1]],
        "11": [['G', -2], ['D', -1], ['B', -1]],

        # Home, down.
        "20": [['E', -2], ['B', -1], ['G#', 0]],
        "21": [['G', -2], ['D', -1], ['B', -1]],
        "23": [['F', -2], ['C', -1], ['A', -1]],

        # Hope, left.
        "30": [['D', -1], ['A', -1], ['F#', 0]],
        "31": [['E', -1], ['B', -1], ['Gb', 0], ['G', 0]],
        "32": [['F#', -1], ['D', 0], ['A', 0]],

        # Caution, up.
        #"00": [['F', -2], ['C', -1], ['A', -1]],
        "01": [['C#', -2], ['G#', -1], ['F', 0]],
        #"02": [['D#', -2], ['A#', -2], ['G', 0]],
        "02": [['D', -2], ['A', -2], ['E', 0], ['F', 0]],
        #"03": [['C#', -2], ['G#', -1], ['D#', 0]],
        "03": [['C#', -2], ['A', -1], ['C#', 0]],

        # Triumph
        "12": [['G#', -2], ['E', -1], ['B', -1]],
        #"13": [['G#', -2], ['E', -1], ['B', -1]],
        #"13": [['D', -1], ['A', -1], ['F#', 0]],
        ##"13": [['A', -1], ['F', 0], ['B', 0], ['C', 0]],
        "13": [['F', -2], ['C', -1], ['A', -1], ['B', -1]],
        "10": [['E', -1], ['B', -1], ['G#', 0]],
}

LEFT_STICK_COMPANY = {

    "22": [['A', -3]],
    "33": [['C', -2]],
    "00": [['F', -3]],
    "11": [['G', -3]],

}

append_volume(LSV, LEFT_STICK_NOTES)
append_volume(LS_AV, LEFT_STICK_COMPANY)

# for n in LEFT_STICK_NOTES.keys():
#     append_volume(LSV, LEFT_STICK_NOTES[n])
# for n in LEFT_STICK_NOTES.keys():
#     append_volume(LSV, LEFT_STICK_COMPANY[n])