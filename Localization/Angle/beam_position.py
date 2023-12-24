from constants import *
def set_beam_position(horizontal_postion, horizontal_angle=0):
    """
    This function sets the beam position to the horizontal position if true and to the vertical position if false
    :param horizontal_postion: true if horizontal position, false if vertical position
    :return:
    """
    if horizontal_postion:
        for id, phi in enumerate(HORIZONTAL_ARRANGEMENT):
            # self.mic.set_beam_direction(id, phi, 90)
            pass

    else:
        for id, theta in enumerate(VERTICAL_ARRANGEMENT):
            # self.mic.set_beam_direction(id, horizontal_angle, theta)
            pass