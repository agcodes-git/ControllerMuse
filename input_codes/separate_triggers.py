import pygame
from input_codes import controller, input_manager

pygame.init()
s = pygame.display.set_mode((500,500))
p_clock = pygame.time.Clock()

joysticks = controller.XInputJoystick.enumerate_devices()
j = joysticks[0]

pjs = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pjs: p.init()

axis_values = {}
@j.event
def on_axis(axis, value):
    axis_values[axis] = value
    if axis == "left_trigger":
        input_manager.left[0] = value
    elif axis == "right_trigger":
        input_manager.right[0] = value
    #j.set_vibration(left[0], right[0])


while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,500,500))

    # ---- Draw analog sticks. -----
    pygame.draw.circle(s, (150,255,0), (220, 250), 30, 1)
    if 'ax00' in input_manager.axes and 'ax01' in input_manager.axes:
        pygame.draw.circle(s, (150,255,0), (int(input_manager.axes['ax00'] * 30 + 220), int(
            input_manager.axes['ax01'] * 30 + 250)), 4, 0)
    pygame.draw.circle(s, (0,150,255), (300,250), 30, 1)
    if 'ax03' in input_manager.axes and 'ax04' in input_manager.axes:
        pygame.draw.circle(s, (0,150,255), (int(input_manager.axes['ax04'] * 30 + 300), int(
            input_manager.axes['ax03'] * 30 + 250)), 4, 0)

    # ---- Draw triggers. ----
    pygame.draw.rect(s, (150,255,0), (220, 300, 80, 10), 2)
    pygame.draw.rect(s, (150,255,0), (220, 300, input_manager.left[0]*80, 10), 0)

    pygame.draw.rect(s, (0,150,255), (220, 320, 80, 10), 2)
    pygame.draw.rect(s, (0,150,255), (220, 320, input_manager.right[0]*80, 10), 0)

    # ---- Draw hat. -----
    if 'ht00' in input_manager.hats:
        pygame.draw.rect(s, (255,0,150), (350 + input_manager.hats['ht00'][0] * 10, 250 -
                                          input_manager.hats['ht00'][1] * 10, 10, 10), 0)
    # --- Respond to button presses.
    input_manager.update_inputs(pygame.event.get(), debug=True)
    if input_manager.pressed("bt00"):
        print("Hit A button")

    j.dispatch_events()
    p_clock.tick(60)


