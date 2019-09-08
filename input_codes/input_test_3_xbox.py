import input_codes.input_manager as im
import input_codes.xbox_interface as xbi
import input_codes.controller as controller
import pygame

pygame.init()
s = pygame.display.set_mode((500,500))
p_clock = pygame.time.Clock()

xbox_joysticks = controller.XInputJoystick.enumerate_devices()
pygame_joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for p in pygame_joysticks: p.init()

xbc_1 = xbi.xbox_controller( 0 )

while True:

    pygame.display.flip()
    pygame.draw.rect(s, (0,0,0), (0,0,500,500))
    

    im.update_inputs(pygame.event.get())

    # Read left analog.
    left_analog = xbc_1.get_stick(xbc_1.LEFT_ANALOG)
    pygame.draw.circle(s, (150, 255, 0),
                       (220 + int( left_analog[0] * 30 ),
                        250 + int( left_analog[1] * 30 )), 5, 0)

    # Read right analog.
    right_analog = xbc_1.get_stick(xbc_1.RIGHT_ANALOG)
    pygame.draw.circle(s, (150, 255, 0),
                       (300 + int( right_analog[0] * 30 ),
                        250 + int( right_analog[1] * 30 )), 5, 0)

    # Draw directional pad.
    for x in range(-1,2):
        for y in range(-1,2):
            d_pad = xbc_1.get_hat(xbc_1.D_PAD)
            fill = 0 if all([a==b for (a,b) in zip(d_pad, (x,-1 * y))]) else 1
            pygame.draw.rect(s, (80,80,80), (350 + (11*x),220 + (11*y), 10, 10), fill)

    # Draw buttons (presses, releases, sustained presses)
    pygame.draw.circle(s, (80, 255, 80), (220, 370), 10, 0 if xbc_1.is_button_down(xbc_1.A) else 1)
    pygame.draw.circle(s, (255, 80, 80), (245, 350), 10, 0 if xbc_1.is_button_down(xbc_1.B) else 1)
    pygame.draw.circle(s, (80, 80, 255), (195, 350), 10, 0 if xbc_1.is_button_down(xbc_1.X) else 1)
    pygame.draw.circle(s, (255, 255, 80), (220, 330), 10, 0 if xbc_1.is_button_down(xbc_1.Y) else 1)

    if xbc_1.is_button_pressed(xbc_1.A): pygame.draw.circle(s, (255, 255, 255), (220, 370), 14, 0)
    if xbc_1.is_button_pressed(xbc_1.B): pygame.draw.circle(s, (255, 255, 255), (245, 350), 14, 0)
    if xbc_1.is_button_pressed(xbc_1.X): pygame.draw.circle(s, (255, 255, 255), (195, 350), 14, 0)
    if xbc_1.is_button_pressed(xbc_1.Y): pygame.draw.circle(s, (255, 255, 255), (220, 330), 14, 0)

    if xbc_1.is_button_released(xbc_1.A): pygame.draw.circle(s, (255, 0, 255), (220, 370), 14, 2)
    if xbc_1.is_button_released(xbc_1.B): pygame.draw.circle(s, (255, 0, 255), (245, 350), 14, 2)
    if xbc_1.is_button_released(xbc_1.X): pygame.draw.circle(s, (255, 0, 255), (195, 350), 14, 2)
    if xbc_1.is_button_released(xbc_1.Y): pygame.draw.circle(s, (255, 0, 255), (220, 330), 14, 2)

    p_clock.tick(60)