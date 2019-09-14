import pygame
import pygame.midi as md
from input_codes import controller, input_manager

from note_mapping import to_note
from note_mapping import RIGHT_STICK_NOTES
from note_mapping import LEFT_STICK_NOTES
from note_mapping import RIGHT_STICK_COMPANY
from note_mapping import LEFT_STICK_COMPANY

import math
pygame.init()
pygame.midi.init()
s = pygame.display.set_mode((600,300))
p_clock = pygame.time.Clock()

joysticks = controller.XInputJoystick.enumerate_devices()
j = joysticks[0]
pjs = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pjs: p.init()

import rtmidi

midiout_1 = rtmidi.MidiOut()
available_ports = midiout_1.get_ports()

if available_ports:
    midiout_1.open_port(1)
else:
    midiout_1.open_virtual_port("My virtual output")
    print("This ran, honestly don't know if it works though.")

axis_values = {}

@j.event
def on_axis(axis, value):
    axis_values[axis] = value
    if axis == "left_trigger":
        input_manager.left[0] = value
    elif axis == "right_trigger":
        input_manager.right[0] = value
    #j.set_vibration(input_manager.left[0]/3.0, input_manager.left[0]/5.0)

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
        return 'C' # For center.

octave = 0
old_LP = "CENTER"
old_RP = "CENTER"
old_left_trigger = False
old_right_trigger = False

bs = 100
left_offset = (175, 150)
right_offset = (425, 150)
current_right_note = None
current_left_note = None

def draw_arbitrary_pad(screen, color, offset, current_sp, old_sp, regions):
    circle_size = 20
    frame_size = 80
    pygame.draw.circle(screen, color, offset, frame_size, 3)
    #pygame.draw.circle(screen, color, offset, int(50 * 0.8), 1)
    angle_offset = - math.pi / 2.0
    to_xy = lambda q:([(int(frame_size*math.cos(a)), int(frame_size*math.sin(a))) for a in [angle_offset+q*(math.pi*2.0)/float(regions)]])
    for n in range(regions):
        x,y = to_xy(n)[0]
        lx, ly = to_xy(n+0.5)[0]
        pygame.draw.circle(screen, (0,0,0), (offset[0]+x, offset[1]+y), circle_size, 0)
        #pygame.draw.rect(screen, (0,0,0), (offset[0]+x-circle_size/2, offset[1]+y-circle_size/2, circle_size, circle_size), 0)
        #pygame.draw.circle(screen, color if current_sp == n else (255,255,255), (offset[0]+x, offset[1]+y), circle_size-2, 0 if current_sp == n else 1)

        if current_sp == n:
            pygame.draw.circle(screen, color, (offset[0]+x, offset[1]+y), circle_size-2, 0)

        pygame.draw.circle(screen, (200,200,200), (offset[0]+x, offset[1]+y), circle_size-2, 1)

        if str(current_sp) != str(old_sp) and current_sp == n:
            pygame.draw.circle(screen, (255,255,255), (offset[0]+x, offset[1]+y), circle_size-2, 0 if current_sp == n else 1)
        #pygame.draw.rect(screen, color, (offset[0]+x-circle_size/2, offset[1]+y-circle_size/2, circle_size, circle_size), 0 if stick_position==n else 1)
        #pygame.draw.line(screen, color, offset, (offset[0]+lx, offset[1]+ly), 1)
    pygame.draw.circle(screen, (0,0,0), offset, circle_size, 0)
    pygame.draw.circle(screen, color, offset, circle_size-2, 0 if current_sp == 'C' else 1)
    #rax, ray = right_analog_stick()
    #pygame.draw.circle(screen, (255,255,255), (int(offset[0]+rax*50), int(offset[1]+ray*50)), 5, 0)

current_left_company_key = None
old_left_company_key = None
current_right_company_key = None
old_right_company_key = None

left_color = (150, 255, 0)
right_color = (255, 0, 150)
harmony = None
accompany = None

SEGMENTS = 4
while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,1000,1000))

    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=False)
    input_manager.keys_down['right_trigger'] = get_left_trigger() > 0.5
    input_manager.keys_down['left_trigger'] = get_right_trigger() > 0.5
    current_COMBINED_P = point_to_arbitrary(left_analog_stick(), SEGMENTS)
    current_RP = point_to_arbitrary(right_analog_stick(), SEGMENTS)
    current_LP = point_to_arbitrary(left_analog_stick(), SEGMENTS)
    current_left_trigger = get_left_trigger() > 0.5
    current_right_trigger = get_right_trigger() > 0.5
    draw_arbitrary_pad(s, left_color, left_offset, current_COMBINED_P, old_LP, SEGMENTS)
    draw_arbitrary_pad(s, right_color, right_offset, current_RP, old_RP, SEGMENTS)

    current_RP = str(current_RP)
    current_LP = str(current_LP)

    for key in RIGHT_STICK_NOTES.keys():
        if current_RP == key:
            if old_RP != key:

                for note in RIGHT_STICK_NOTES[key]:
                    midiout_1.send_message([0x90, to_note(note[0], note[1]), note[2]])
                    current_right_note = key

                if current_right_trigger:

                    old_right_company_key = current_right_company_key
                    current_right_company_key = key

                    # First, turn off all the old company notes.
                    if old_right_company_key is not None:
                        for note in RIGHT_STICK_COMPANY[old_right_company_key]:
                            midiout_1.send_message([0x80, to_note(note[0], note[1]), note[2]])

                    # Then turn on the new accompanying notes.
                    for note in RIGHT_STICK_COMPANY[key]:
                        midiout_1.send_message([0x90, to_note(note[0], note[1]), note[2]])

            if current_right_trigger:
                if not old_right_trigger:
                    # Then turn on the new ones.
                    for note in RIGHT_STICK_COMPANY[key]:
                        midiout_1.send_message([0x90, to_note(note[0], note[1]), note[2]])
            else:
                if old_right_trigger:
                    for note in RIGHT_STICK_COMPANY[key]:
                        midiout_1.send_message([0x80, to_note(note[0], note[1], 112)])
        else:
            if old_RP == key:
                for note in RIGHT_STICK_NOTES[key]:
                    midiout_1.send_message([0x80, to_note(note[0], note[1]), note[2]])
                    current_right_note = None
                # for note in right_company[key]:
                #     midiout.send_message([0x80, to_note(note[0], note[1]), note[2]])
            if not current_right_trigger and old_right_trigger:
                for note in RIGHT_STICK_COMPANY[key]:
                    midiout_1.send_message([0x80, to_note(note[0], note[1], 112)])

    # Turning off notes for the left stick.
    for key in LEFT_STICK_NOTES.keys():

        if old_LP != current_LP:
            if key == harmony:
                for note in LEFT_STICK_NOTES[key]:
                    midiout_1.send_message([0x80, to_note(note[0], note[1]), note[2]])
                harmony = None

    # Having trigger state determine if 1, 2, or 3 notes are played could be cool.
    # Turning off notes for the left trigger.
    for key in LEFT_STICK_COMPANY.keys():

        if (old_LP != current_LP and current_LP != 'C') or (old_left_trigger and not current_left_trigger):
            if key == accompany:
                for note in LEFT_STICK_COMPANY[key]:
                    midiout_1.send_message([0x80, to_note(note[0], note[1]), note[2]])
                accompany = None

    # Turning on notes for the left stick.
    for key in LEFT_STICK_NOTES.keys():

        # Turning on the right notes.
        if key[0] != current_RP: continue # Don't activate any notes not associated with right position.
        if key[1] != current_LP: continue # Don't activate notes not associated with the left position.
        if current_LP == old_LP and (harmony is not None and harmony[0]!='C'): continue # Don't play new harmony if the harmony stick didn't move.

        harmony = key # Record what the currently held harmony is.
        for note in LEFT_STICK_NOTES[key]:
            midiout_1.send_message([0x90, to_note(note[0], note[1]), note[2]])

    # Turning on notes for the left trigger.
    # Something buggy here still - if you change the right note it will change the accompaniment,
    # even if the left note is still playing.
    for key in LEFT_STICK_COMPANY.keys():

        # Turning on the right notes.
        if key[0] != current_RP: continue # Don't activate any notes not associated with right position.
        if key[1] != current_LP: continue # Don't activate notes not associated with the left position.
        if not current_left_trigger: continue # Don't activate if the trigger isn't held down.
        if old_left_trigger and current_LP == old_LP and (accompany is not None and accompany[0] != 'C'): continue # Don't activate if not pressed again
                                                               # and there's no stick change.
        if  not (current_left_trigger and not old_left_trigger) and key[0] != harmony[0] and harmony[0] != 'C': continue

        accompany = key # Record what the currently held accompaniment is.
        for note in LEFT_STICK_COMPANY[key]:
            midiout_1.send_message([0x90, to_note(note[0], note[1]), note[2]])

    old_LP = current_LP
    old_RP = current_RP
    old_left_trigger = current_left_trigger
    old_right_trigger = current_right_trigger

    j.dispatch_events()
    p_clock.tick(60)


