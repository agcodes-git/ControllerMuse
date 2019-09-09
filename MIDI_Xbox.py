import pygame
import pygame.midi as md
from input_codes import controller, input_manager
import time
import math
pygame.init()
pygame.midi.init()
s = pygame.display.set_mode((500,500))
p_clock = pygame.time.Clock()
import numpy as np

joysticks = controller.XInputJoystick.enumerate_devices()
j = joysticks[0]
pjs = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pjs: p.init()

player = pygame.midi.Output(0)
#player.set_instrument(12) # bells
player.set_instrument(15)

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

def get_right_trigger(): return input_manager.left[0]
def get_left_trigger(): return input_manager.right[0]

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
    player.note_on(letter_code, 127)
    time.sleep(delay)
    player.note_on(letter_code+4, 127)
    time.sleep(delay)
    player.note_on(letter_code+7, 127)
def minor(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player.note_on(letter_code, 127)
    time.sleep(delay)
    player.note_on(letter_code + 3, 127)
    time.sleep(delay)
    player.note_on(letter_code + 7, 127)
def felt(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player.note_on(letter_code, 127)
    time.sleep(delay)
    player.note_on(letter_code + 0, 127)
    time.sleep(delay)
    player.note_on(letter_code + 4, 127)
    time.sleep(delay)
    player.note_on(letter_code + 5, 127)
    time.sleep(delay)
    player.note_on(letter_code + 9, 127)

def play(base_letter, octave, delay=0):
    player.note_on(to_note(base_letter, octave), 127)

def long_major(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player.note_on(letter_code, 127)
    time.sleep(delay)
    player.note_on(letter_code + 7, 127)
    time.sleep(delay)
    player.note_on(letter_code + 16, 127)
def long_minor(base_letter, octave, delay=0.05):
    letter_code = to_note(base_letter, octave)
    player.note_on(letter_code, 127)
    time.sleep(delay)
    player.note_on(letter_code + 7, 127)
    time.sleep(delay)
    player.note_on(letter_code + 15, 127)

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

while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,500,500))

    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=False)
    input_manager.keys_down['right_trigger'] = get_left_trigger() > 0.5
    input_manager.keys_down['left_trigger'] = get_right_trigger() > 0.5

    left_stick = left_analog_stick()
    right_stick = right_analog_stick()

    left_quadrant = point_to_quadrant(left_stick)
    bs = 30
    offset = (50, 20)
    color = (150, 0, 255)
    pygame.draw.rect(s, color, (bs + offset[0], bs + offset[1], bs, bs), 0 if left_quadrant == "UP" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 2 + offset[1], bs, bs), 0 if left_quadrant == "CENTER" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 3 + offset[1], bs, bs), 0 if left_quadrant == "DOWN" else 1)
    pygame.draw.rect(s, color, (0 + offset[0], bs * 2 + offset[1], bs, bs), 0 if left_quadrant == "LEFT" else 1)
    pygame.draw.rect(s, color, (bs * 2 + offset[0], bs * 2 + offset[1], bs, bs), 0 if left_quadrant == "RIGHT" else 1)

    left_delay = 0
    if input_manager.pressed('left_trigger'):
       if left_quadrant == "CENTER": play('A', octave-1, delay = left_delay)
       if left_quadrant == "DOWN": play('F', octave-1, delay = left_delay)
       if left_quadrant == "UP": play('C', octave, delay = left_delay)
       if left_quadrant == "LEFT": play('G', octave-1, delay = left_delay)
       if left_quadrant == "RIGHT": play('D', octave-1, delay = left_delay)

    right_quadrant = point_to_quadrant(right_stick)
    bs = 30
    offset = (200, 20)
    color = (150, 255, 0)
    pygame.draw.rect(s, color, (bs + offset[0], bs + offset[1], bs, bs), 0 if right_quadrant == "UP" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 2 + offset[1], bs, bs), 0 if right_quadrant == "CENTER" else 1)
    pygame.draw.rect(s, color, (bs + offset[0], bs * 3 + offset[1], bs, bs), 0 if right_quadrant == "DOWN" else 1)
    pygame.draw.rect(s, color, (0 + offset[0], bs * 2 + offset[1], bs, bs), 0 if right_quadrant == "LEFT" else 1)
    pygame.draw.rect(s, color, (bs * 2 + offset[0], bs * 2 + offset[1], bs, bs), 0 if right_quadrant == "RIGHT" else 1)

    # Depending on the quadrant I would like different responses.
    #
    right_delay = 0
    if input_manager.pressed('right_trigger'):

        if left_quadrant == "CENTER":
            if right_quadrant == "CENTER": long_major('A', octave-2, delay = right_delay)
            if right_quadrant == "DOWN": long_minor('A', octave-2, delay = right_delay)
            if right_quadrant == "UP": felt('A', octave-1, delay = right_delay)
            if right_quadrant == "LEFT": major('A', octave-2, delay = right_delay)
            if right_quadrant == "RIGHT": play('A', octave-2, delay = right_delay)

        if left_quadrant == "LEFT":
            if right_quadrant == "CENTER": long_major('F', octave-2, delay = right_delay)
            if right_quadrant == "DOWN": long_minor('F', octave-2, delay = right_delay)
            if right_quadrant == "UP": felt('F', octave-1, delay = right_delay)
            if right_quadrant == "LEFT": major('F', octave-2, delay = right_delay)
            if right_quadrant == "RIGHT": play('F', octave-2, delay = right_delay)

        if left_quadrant == "RIGHT":
            if right_quadrant == "CENTER": long_major('C', octave - 2, delay=right_delay)
            if right_quadrant == "DOWN": long_minor('C', octave - 2, delay=right_delay)
            if right_quadrant == "UP": felt('C', octave - 1, delay=right_delay)
            if right_quadrant == "LEFT": major('C', octave - 2, delay=right_delay)
            if right_quadrant == "RIGHT": play('C', octave - 2, delay=right_delay)

        if left_quadrant == "UP":
            if right_quadrant == "CENTER": long_major('G', octave-2, delay = right_delay)
            if right_quadrant == "DOWN": long_minor('G', octave-2, delay = right_delay)
            if right_quadrant == "UP": felt('G', octave-1, delay = right_delay)
            if right_quadrant == "LEFT": major('G', octave-2, delay = right_delay)
            if right_quadrant == "RIGHT": play('G', octave-2, delay = right_delay)

        if left_quadrant == "DOWN":
            if right_quadrant == "CENTER": long_major('D', octave-2, delay = right_delay)
            if right_quadrant == "DOWN": long_minor('D', octave-2, delay = right_delay)
            if right_quadrant == "UP": felt('D', octave-1, delay = right_delay)
            if right_quadrant == "LEFT": major('D', octave-2, delay = right_delay)
            if right_quadrant == "RIGHT": play('D', octave-2, delay = right_delay)


    j.dispatch_events()
    p_clock.tick(60)


