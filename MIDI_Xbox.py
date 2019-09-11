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

def point_to_octant(point):
    angle = math.atan2(point[0], point[1]) * 2.0 / (2.0*math.pi)
    magnitude = math.sqrt(point[0]**2 + point[1]**2)

    CE = 0.0 # Cardinal expansion. I thought this would be nice because it's harder to hit diagonals from center,
            # but it also means spinning the stick won't produce even spacing, which I definitely would like to keep.

    if magnitude < 0.8: return "CENTER"
    else:
        if (1.0 > angle > 0.875 + CE) or (-0.875 - CE > angle > -1.0): return "TOP"
        if (0.125 - CE > angle > 0) or (0 > angle > -0.125 + CE): return "BOTTOM"

        if 0.875 + CE > angle > 0.625 - CE: return "TOP_RIGHT"
        if 0.625 - CE > angle > 0.375 + CE: return "RIGHT"
        if 0.375 + CE > angle > 0.125 - CE: return "BOTTOM_RIGHT"

        if -0.125 + CE > angle > -0.375 - CE: return "BOTTOM_LEFT"
        if -0.375 - CE > angle > -0.625 + CE: return "LEFT"
        if -0.625 + CE > angle > -0.875 - CE: return "TOP_LEFT"

def point_to_quadrant(point):

    angle = math.atan2(point[0], point[1]) * (360.0 / (2.0 * math.pi))
    magnitude = math.sqrt(point[0]**2 + point[1]**2)

    if magnitude < 0.3: return "CENTER"
    else:
        if (180 > angle > 135) or (-135 > angle > -180): return "TOP"
        if (45 > angle > 0) or (0 > angle > -45): return "BOTTOM"
        if 135 > angle > 45: return "RIGHT"
        if -45 > angle > -135: return "LEFT"

octave = 0
old_LP = "CENTER"
old_RP = "CENTER"
old_left_trigger = False
old_right_trigger = False

def draw_pad(screen, color, bs, offset, stick_position, regions):
    pygame.draw.rect(screen, color, (bs + offset[0], bs + offset[1], bs, bs), 0 if stick_position == "TOP" else 1)
    pygame.draw.rect(screen, color, (bs + offset[0], bs * 2 + offset[1], bs, bs), 0 if stick_position == "CENTER" else 1)
    pygame.draw.rect(screen, color, (bs + offset[0], bs * 3 + offset[1], bs, bs), 0 if stick_position == "BOTTOM" else 1)
    pygame.draw.rect(screen, color, (0 + offset[0], bs * 2 + offset[1], bs, bs), 0 if stick_position == "LEFT" else 1)
    pygame.draw.rect(screen, color, (bs * 2 + offset[0], bs * 2 + offset[1], bs, bs), 0 if stick_position == "RIGHT" else 1)

    if regions == 8:
        pygame.draw.rect(screen, color, (bs*2 + offset[0], bs + offset[1], bs, bs), 0 if stick_position == "TOP_RIGHT" else 1)
        pygame.draw.rect(screen, color, (bs*2 + offset[0], bs * 3 + offset[1], bs, bs), 0 if stick_position == "BOTTOM_RIGHT" else 1)
        pygame.draw.rect(screen, color, (bs*0 + offset[0], bs * 3 + offset[1], bs, bs), 0 if stick_position == "BOTTOM_LEFT" else 1)
        pygame.draw.rect(screen, color, (bs*0 + offset[0], bs + offset[1], bs, bs), 0 if stick_position == "TOP_LEFT" else 1)

bs = 100
left_offset = (50, 20)
right_offset = (400, 20)
while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,1000,1000))

    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=False)
    input_manager.keys_down['right_trigger'] = get_left_trigger() > 0.5
    input_manager.keys_down['left_trigger'] = get_right_trigger() > 0.5

    left_stick = left_analog_stick()
    right_stick = right_analog_stick()

    if get_right_trigger() > 0.5: right_color = (0, 255, 150)
    else: right_color = (150, 0, 255)

    if get_left_trigger() > 0.5: left_color = (255, 150, 0)
    else: left_color = (255, 0, 150)

    current_LP = point_to_quadrant(left_stick)
    current_RP = point_to_quadrant(right_stick)
    current_left_trigger = get_left_trigger() > 0.5
    current_right_trigger = get_right_trigger() > 0.5

    draw_pad(s, left_color, bs, left_offset, current_LP, 4)
    draw_pad(s, right_color, bs, right_offset, current_RP, 4)

    right_normal_notes = {
        "BOTTOM"    :   [('A', 0), ('C', 1)],
        "LEFT"      :   [('B', 0)],
        "TOP"       :   [('C', 1)],
        "RIGHT"     :   [('D', 1)]
    }
    right_alternate_notes = {}

    left_normal_notes = {
        "BOTTOM"    :   [('E', 1)],
        "LEFT"      :   [('F', 1)],
        "TOP"       :   [('G', 1)],
        "RIGHT"     :   [('A', 1)]
    }
    left_alternate_notes = {}

    right_notes = right_normal_notes if get_right_trigger() < 0.5 else right_alternate_notes
    for key in right_notes.keys():
        if current_RP == key:
            if old_RP != key or (current_right_trigger and not old_right_trigger):
                for note in right_notes[key]:
                    midiout.send_message([0x90, to_note(note[0], note[1]), 112])
        else:
            if old_RP == key:
                for note in right_notes[key]:
                    midiout.send_message([0x80, to_note(note[0], note[1]), 112])

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


