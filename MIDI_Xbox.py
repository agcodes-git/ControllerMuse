import pygame
import pygame.midi as md
from input_codes import controller, input_manager
import time
import math
pygame.init()
pygame.midi.init()
s = pygame.display.set_mode((800,500))
p_clock = pygame.time.Clock()
import numpy as np

joysticks = controller.XInputJoystick.enumerate_devices()
j = joysticks[0]
pjs = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pjs: p.init()

#player_1 = pygame.midi.Output(0)
#player.set_instrument(12) # bells
#player.set_instrument(15) # bells
#player.set_instrument(40) # violin
# 78 is a whistle. 25 is a clavichord/banjoy
#player_1.set_instrument(130)

import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")
    print("This ran, honestly don't know if it works though.")

axis_values = {}

@j.event
def on_axis(axis, value):


    axis_values[axis] = value
    if axis == "left_trigger":
        input_manager.left[0] = value
    elif axis == "right_trigger":
        input_manager.right[0] = value
    #j.set_vibration(left[0], right[0])

# Examples:
# input_manager.axes['ax00']
# input_manager.left[0]
# input_manager.pressed('bt00')
# input_manager.hats['ht00'][1]

def A_pressed(): return input_manager.pressed('bt00')
def B_pressed(): return input_manager.pressed('bt01')
def X_pressed(): return input_manager.pressed('bt02')
def Y_pressed(): return input_manager.pressed('bt03')
def dpad_up_pressed(): return input_manager.pressed('ht00_up')
def dpad_down_pressed(): return input_manager.pressed('ht00_down')
def dpad_left_pressed(): return input_manager.pressed('ht00_left')
def dpad_right_pressed(): return input_manager.pressed('ht00_right')

def get_right_trigger(): return input_manager.right[0]
def get_left_trigger(): return input_manager.left[0]

def left_analog_stick():
    x_axis = 0.01 if 'ax00' not in input_manager.axes else input_manager.axes['ax00']
    y_axis = 0.01 if 'ax01' not in input_manager.axes else input_manager.axes['ax01']
    return x_axis, y_axis

def right_analog_stick():
    x_axis = 0.01 if 'ax04' not in input_manager.axes else input_manager.axes['ax04']
    y_axis = 0.01 if 'ax03' not in input_manager.axes else input_manager.axes['ax03']
    return x_axis, y_axis

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

'''def major(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player_1.note_on(letter_code, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 4, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 7, 127)
def minor(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player_1.note_on(letter_code, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 3, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 7, 127)
def felt(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player_1.note_on(letter_code, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 0, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 4, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 5, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 9, 127)

def play(base_letter, octave, delay=0):
    player_1.note_on(to_note(base_letter, octave), 127)
'''
def long_major(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    midiout.send_message([0x90, letter_code, 112])
    #player_1.note_on(letter_code, 127)
    time.sleep(delay)
    midiout.send_message([0x90, letter_code+7, 112])
    #player_1.note_on(letter_code + 7, 127)
    time.sleep(delay)
    midiout.send_message([0x90, letter_code+16, 112])
    #player_1.note_on(letter_code + 16, 127)
def long_minor(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    midiout.send_message([0x90, letter_code, 112])
    #player_1.note_on(letter_code, 127)
    time.sleep(delay)
    midiout.send_message([0x90, letter_code+7, 112])
    #player_1.note_on(letter_code + 7, 127)
    time.sleep(delay)
    midiout.send_message([0x90, letter_code+15, 112])
    #player_1.note_on(letter_code + 15, 127)

def point_to_arbitrary(point, segments):
    angle = 0.5 * (1 - (math.atan2( point[0], point[1] ) / math.pi)) # 1 to -1
    magnitude = math.sqrt(point[0]**2 + point[1]**2)

    if magnitude > 0.8:
        seg_size = 1.0 / segments
        # The top case is weird, but everything else should be fine.
        first_range = [(1-seg_size/2.0, 1), (0, seg_size/2.0)]
        other_ranges = [(seg_size/2.0 + n * seg_size, seg_size/2.0 + (n+1) * seg_size) for n in range(0, segments-1)]
        if any([r[0] < angle < r[1] for r in first_range]):
            return 0
        for n in range(len(other_ranges)):
           if other_ranges[n][0] < angle < other_ranges[n][1]:
                #print('segment ', n+1)
                return n+1
    else:
        return -1

octave = 0
old_LP = "CENTER"
old_RP = "CENTER"
old_left_trigger = False
old_right_trigger = False

bs = 100
left_offset = (150, 150)
right_offset = (300, 150)
current_note = None

def draw_arbitrary_pad(screen, color, offset, stick_position, regions):
    circle_size = 20
    pygame.draw.circle(screen, color, offset, 50, 1)
    #pygame.draw.circle(screen, color, offset, int(50 * 0.8), 1)
    angle_offset = - math.pi / 2.0
    to_xy = lambda q:([(int(50*math.cos(a)), int(50*math.sin(a))) for a in [angle_offset+q*(math.pi*2.0)/float(regions)]])
    for n in range(regions):
        x,y = to_xy(n)[0]
        lx, ly = to_xy(n+0.5)[0]
        pygame.draw.circle(screen, (0,0,0), (offset[0]+x, offset[1]+y), circle_size, 0)
        #pygame.draw.rect(screen, (0,0,0), (offset[0]+x-circle_size/2, offset[1]+y-circle_size/2, circle_size, circle_size), 0)
        pygame.draw.circle(screen, color, (offset[0]+x, offset[1]+y), circle_size-2, 0 if stick_position == n else 1)
        #pygame.draw.rect(screen, color, (offset[0]+x-circle_size/2, offset[1]+y-circle_size/2, circle_size, circle_size), 0 if stick_position==n else 1)
        #pygame.draw.line(screen, color, offset, (offset[0]+lx, offset[1]+ly), 1)
    pygame.draw.circle(screen, (0,0,0), offset, circle_size, 0)
    pygame.draw.circle(screen, color, offset, circle_size-2, 0 if stick_position == -1 else 1)

    #rax, ray = right_analog_stick()
    #pygame.draw.circle(screen, (255,255,255), (int(offset[0]+rax*50), int(offset[1]+ray*50)), 5, 0)

SEGMENTS = 6
while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,1000,1000))

    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=False)
    input_manager.keys_down['right_trigger'] = get_left_trigger() > 0.5
    input_manager.keys_down['left_trigger'] = get_right_trigger() > 0.5

    current_LP = point_to_arbitrary(left_analog_stick(), SEGMENTS)
    current_RP = point_to_arbitrary(right_analog_stick(), SEGMENTS)

    current_left_trigger = get_left_trigger() > 0.5
    current_right_trigger = get_right_trigger() > 0.5

    if current_left_trigger:
        left_color = (255, 150, 0)
    else:
        left_color = (150, 255, 0)

    if current_right_trigger:
        right_color = (0, 255, 150)
    else:
        right_color = (255, 0, 150)

    draw_arbitrary_pad(s, left_color, left_offset, current_LP, SEGMENTS)
    draw_arbitrary_pad(s, right_color, right_offset, current_RP, SEGMENTS)

    right_normal_notes = {
        "3": [('D', 0)],
        "4": [('E', 0)],
        "5": [('F', 0)],
        "0": [('G', 0)],
        "1": [('A', 0)],
        "2": [('Bb', 0)]
    }
    right_alternate_notes = {
        #"3": [('D', 0)],
        #"4": [('E', 0)],
        #"5": [('F#', 0)],
        #"0": [('G', 0)],
        #"1": [('A', 0)],
        #"2": [('B', 0)]
         "3": [('D', 0)],
         "4": [('D#', 0)],
         "5": [('F#', 0)],
         "0": [('G', 0)],
         "1": [('A', 0)],
         "2": [('Bb', 0)]
    }

    left_normal_notes = {
        "BOTTOM"    :   [('D', -2), ('D', -1), ('A', -1)],
        "LEFT"      :   [('F#', -2), ('F#', -1), ('C#', -1)],
        "TOP"       :   [('G', -2), ('G', -1), ('D', -1)],
        "RIGHT"     :   [('A', -2), ('A', -1), ('E', -1)]
    }
    left_alternate_notes = {}
    right_notes = right_normal_notes if get_right_trigger() < 0.5 else right_alternate_notes

    current_RP = str(current_RP)
    current_LP = str(current_LP)

    for key in right_notes.keys():
        if current_RP == key:
            if old_RP != key:
                for note in right_notes[key]:
                    midiout.send_message([0x90, to_note(note[0], note[1]), 112])
                    current_note = key
        else:
            if old_RP == key:
                for note in right_notes[key]:
                    midiout.send_message([0x80, to_note(note[0], note[1]), 112])
                current_note = None

    left_notes = left_normal_notes if get_left_trigger() < 0.5 else left_alternate_notes
    for key in left_notes.keys():
        if current_LP == key:
            if old_LP != key or (current_left_trigger and not current_left_trigger):
                for note in left_notes[key]:
                    midiout.send_message([0x90, to_note(note[0], note[1]), 112])
        else:
            if old_LP == key:
                for note in left_notes[key]:
                    midiout.send_message([0x80, to_note(note[0], note[1]), 112])

    old_LP = current_LP
    old_RP = current_RP
    old_left_trigger = current_left_trigger
    old_right_trigger = current_right_trigger

    j.dispatch_events()
    p_clock.tick(60)


