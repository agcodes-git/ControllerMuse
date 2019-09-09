import pygame
import pygame.midi as md
from input_codes import controller, input_manager
import time
import math
pygame.init()
pygame.midi.init()
s = pygame.display.set_mode((350,250))
p_clock = pygame.time.Clock()
import numpy as np

joysticks = controller.XInputJoystick.enumerate_devices()
j = joysticks[0]
pjs = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pjs: p.init()

player_1 = pygame.midi.Output(0)
#player.set_instrument(12) # bells
#player.set_instrument(15) # bells
#player.set_instrument(40) # violin
# 78 is a whistle.
player_1.set_instrument(15)

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
    }
    return 60 + 12 * octave + letter_code[letter]
def major(base_letter, octave, delay=0.05):
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

def long_major(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player_1.note_on(letter_code, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 7, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 16, 127)
def long_minor(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player_1.note_on(letter_code, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 7, 127)
    time.sleep(delay)
    player_1.note_on(letter_code + 15, 127)

def point_to_quadrant(point):

    angle = math.atan2(point[0], point[1]) * (360.0 / (2.0 * math.pi))
    magnitude = math.sqrt(point[0]**2 + point[1]**2)

    if magnitude < 0.3: return "CENTER"
    else:
        if (180 > angle > 135) or (-135 > angle > -180): return "UP"
        if (45 > angle > 0) or (0 > angle > -45): return "DOWN"
        if 135 > angle > 45: return "RIGHT"
        if -45 > angle > -135: return "LEFT"

octave = 0
maj_chord_function = lambda : long_major if get_left_trigger() < 0.1 else major
min_chord_function = lambda : long_minor if get_left_trigger() < 0.1 else minor

old_LQ = "CENTER"
old_RQ = "CENTER"

while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,500,500))

    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=False)
    input_manager.keys_down['right_trigger'] = get_left_trigger() > 0.5
    input_manager.keys_down['left_trigger'] = get_right_trigger() > 0.5

    r_sttck = left_analog_stick()
    right_stick = right_analog_stick()

    current_LQ = point_to_quadrant(r_sttck)
    bs = 30
    offset = (50, 20)
    color = (150, 0, 255)
    pygame.draw.rect(s, color, (bs + offset[0], bs + offset[1], bs, bs), 0 if current_LQ == "UP" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_LQ == "CENTER" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 3 + offset[1], bs, bs), 0 if current_LQ == "DOWN" else 1)
    pygame.draw.rect(s, color, (0 + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_LQ == "LEFT" else 1)
    pygame.draw.rect(s, color, (bs * 2 + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_LQ == "RIGHT" else 1)

    left_delay = 0

    if current_LQ == "DOWN":
        if old_LQ != "DOWN": player_1.note_on(to_note('A', 0), 127)
        left_note = ('A', 0)
    #else: player_1.note_off(to_note('A', 0))

    if current_LQ == "LEFT":
        if old_LQ != "LEFT": player_1.note_on(to_note('B', 0), 127)
        left_note = ('B', 0)
    #else: player_1.note_off(to_note('B', 0))

    if current_LQ == "UP":
        if old_LQ != "UP": player_1.note_on(to_note('C', 1), 127)
        left_note = ('C#', 0)
   # else: player_1.note_off(to_note('C', 1))

    if current_LQ == "RIGHT":
        if old_LQ != "RIGHT": player_1.note_on(to_note('E', 1), 127)
        left_note = ('Ab', 0)
    #else: player_1.note_off(to_note('E', 0))

    old_LQ = current_LQ

    current_RQ = point_to_quadrant(right_stick)
    bs = 30
    offset = (200, 20)
    color = (150, 255, 0)
    pygame.draw.rect(s, color, (bs + offset[0], bs + offset[1], bs, bs), 0 if current_RQ == "UP" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_RQ == "CENTER" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 3 + offset[1], bs, bs), 0 if current_RQ == "DOWN" else 1)
    pygame.draw.rect(s, color, (0 + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_RQ == "LEFT" else 1)
    pygame.draw.rect(s, color, (bs * 2 + offset[0], bs * 2 + offset[1], bs, bs), 0 if current_RQ == "RIGHT" else 1)

    # Depending on the quadrant I would like different responses.
    # The symmetry between the two sticks should provide the harmony here.
    # i.e. if you're playing the two in the same way, expect them to follow each other.
    # Opposing symmetry should harmonize and in-betweens should be just that.
    right_delay = 0

    if current_LQ == "CENTER": continue

    if current_RQ == "DOWN":
        if old_RQ != "DOWN":
            if current_LQ == 'DOWN':
                long_minor("A", -2, delay = 0)
            if current_LQ == 'LEFT':
                long_major("C", -2, delay=0)  # I don't have a match on B exactly.
            if current_LQ == 'UP':
                long_major("F", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'RIGHT':
                long_major("G", -2, delay = 0) # I don't have a match on B exactly.

    if current_RQ == "LEFT":
        if old_RQ != "LEFT":
            if current_LQ == 'LEFT':
                long_major("G", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'DOWN':
                long_major("G", -2, delay = 0)
            if current_LQ == 'UP':
                long_major("G", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'RIGHT':
                long_major("A", -2, delay = 0) # I don't have a match on B exactly.

    if current_RQ == "UP":
        if old_RQ != "UP":
            if current_LQ == 'UP':
                long_major("C", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'DOWN':
                long_major("E", -1, delay = 0)
            if current_LQ == 'LEFT':
                long_minor("E", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'RIGHT':
                long_major("B", -2, delay = 0) # I don't have a match on B exactly.

    if current_RQ == "RIGHT":
        if old_RQ != "RIGHT":
            if current_LQ == 'RIGHT':
                long_major("E", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'DOWN':
                long_major("F", -2, delay = 0)
            if current_LQ == 'LEFT':
                long_major("D", -2, delay = 0) # I don't have a match on B exactly.
            if current_LQ == 'UP':
                long_major("D", -2, delay = 0) # I don't have a match on B exactly.

    old_RQ = current_RQ


    j.dispatch_events()
    p_clock.tick(60)


