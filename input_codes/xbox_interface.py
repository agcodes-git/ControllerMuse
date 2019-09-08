import input_codes.input_manager as im

# A nice interface for the xbox controller.
class xbox_controller:

    def __init__(self, joystick_number):
        self.joystick_number = joystick_number

    A = '0'
    B = '1'
    X = '2'
    Y = '3'
    LB = '4'
    RB = '5'
    OPTIONS = '6'
    START = '7'
    LEFT_ANALOG = (0,1)
    RIGHT_ANALOG = (4,3)
    LEFT_TRIGGER = 100
    RIGHT_TRIGGER = 101
    D_PAD = '0'

    def is_button_pressed(self, button_code):
        return im.pressed('bt'+str(self.joystick_number)+str(button_code))

    def is_button_released(self, button_code):
        return im.released('bt'+str(self.joystick_number)+str(button_code))

    def is_button_down(self, button_code):
        return im.down('bt'+str(self.joystick_number)+str(button_code))

    def get_stick(self, axes):


        return [self.get_axis(axis) for axis in axes]

    def get_axis(self, axis_number):
        axis_name = 'ax'+str(self.joystick_number)+str(axis_number)
        return im.axes[axis_name] if axis_name in im.axes else 0

    def get_hat(self, hat_number):
        hat_name = 'ht'+str(self.joystick_number)+str(hat_number)
        return im.hats[hat_name] if hat_name in im.hats else (0,0)