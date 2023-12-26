from constants import *
previous_max_pair = None
max_ratio = 0
intial_angle_coefficient = 85  # angle = ratio * angle_coefficient


def return_constant_coefficient():
    return 85


def dynamic_coefficient(max_pair, ratio):
    global max_ratio, previous_max_pair, intial_angle_coefficient
    if abs(ratio) > max_ratio:
        max_ratio = abs(ratio)
    if max_pair != previous_max_pair:
        previous_max_pair = max_pair
        intial_angle_coefficient = 7.5 / max_ratio
        max_ratio = 0
    print(intial_angle_coefficient)
    return intial_angle_coefficient


def angle_coefficient(max_pair, ratio):
    if USE_DYNAMIC_ANGLE_COEFFICIENT:
        coeff = dynamic_coefficient(max_pair, ratio)
    else:
        coeff = return_constant_coefficient()
    return coeff
