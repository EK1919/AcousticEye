import numpy as np
from constants import *
from Localization.f0_methods.HPS_method import hps_on_one_channel
from Localization.Power.power_around_frequencies import find_power_around_frequencies
from Localization.Power.total_power_of_node import find_total_power_of_node
from Localization.f0_methods.SHC_method import SHC_on_one_channel
from Localization.f0_methods.Erez_method import perform_erez_method_on_one_channel

def find_ratio_between_two_nodes(power_array, max_pair):
    """
    This function finds the ratio between two nodes
    :param power_array:
    :param max_pair:
    :return:
    """
    left = np.sqrt(power_array[max_pair[0]])
    right = np.sqrt(power_array[max_pair[1]])
    return (left-right)/(left+right)




def calculate_ratio_of_lobes(max_pair, amplitudes, frequencies, power_array):
    """
    This function calculates the ratio of the lobes
    :param max_pair: the pair of lobes
    :return: the ratio of the lobes
    """
    if RATIO_CALCULATION_METHOD == SELECTED_LOBE_METHOD:
        power_of_left_lobe = power_array[max_pair[0]]
        power_of_right_lobe = power_array[max_pair[1]]


    elif RATIO_CALCULATION_METHOD == "F0":
        if F0_METHOD == 'HPS':
            f0 = hps_on_one_channel(amplitudes[max_pair[0]], 'frequency', frequencies[max_pair[0]])
        elif F0_METHOD == 'SHC':
            f0 = SHC_on_one_channel(amplitudes[max_pair[0]], 'frequency', frequencies[max_pair[0]])
        elif F0_METHOD == 'EREZ':
            f0 = perform_erez_method_on_one_channel(amplitudes[max_pair[0]], 'frequency', frequencies[max_pair[0]])
        else:
            raise ValueError("Invalid F0 method")

        power_of_left_lobe = find_power_around_frequencies(amplitudes[max_pair[0]], f0, 'frequency', WIDTH_OF_PEAK, frequencies)
        power_of_right_lobe = find_power_around_frequencies(amplitudes[max_pair[1]], f0, 'frequency', WIDTH_OF_PEAK, frequencies)

    elif RATIO_CALCULATION_METHOD == "TOTAL":
        power_of_left_lobe = find_total_power_of_node(amplitudes[max_pair[0]], 'frequency', frequencies[max_pair[0]])
        power_of_right_lobe = find_total_power_of_node(amplitudes[max_pair[1]], 'frequency', frequencies[max_pair[1]])

    else:
        raise ValueError("Invalid ratio calculation method")


    ratio = find_ratio_between_two_nodes(power_of_left_lobe, power_of_right_lobe)
    return ratio
