from constants import *
def set_beam_position(horizontal_postion, mic_class, horizontal_angle=0):
    """
    This function sets the beam position to the horizontal position if true and to the vertical position if false
    :param horizontal_postion: true if horizontal position, false if vertical position
    :return:
    """
    if horizontal_postion:
        for id, phi in enumerate(HORIZONTAL_ARRANGEMENT):
            # mic_class.mic.set_beam_direction(id, phi, 90)
            pass

    else:
        for id, theta in enumerate(VERTICAL_ARRANGEMENT):
            # mic_class.mic.set_beam_direction(id, horizontal_angle, theta)
            pass
